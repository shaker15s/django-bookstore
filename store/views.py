from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.core.mail import send_mail
from django.contrib import messages
from django.template.loader import render_to_string
from django.conf import settings
from django.urls import reverse
import stripe

from .models import category, product, slider, order, orderproduct


# ── helpers ────────────────────────────────────────────────────────────────

def _load_cart(request):
    """Return (cart_items list, cart_total) from session, skipping dead PIDs."""
    cart_session = request.session.get('cart', {})
    cart_items, cart_total, stale = [], 0, []

    for pid, quantity in cart_session.items():
        try:
            p = product.objects.get(pk=pid)
            total_price = p.price * quantity
            cart_total += total_price
            cart_items.append({
                'product': p,
                'quantity': quantity,
                'price': total_price,
            })
        except product.DoesNotExist:
            stale.append(pid)

    if stale:
        for pid in stale:
            del cart_session[pid]
        request.session['cart'] = cart_session

    return cart_items, cart_total


def _send_order_email(new_order, cart_items, cart_total, email, first_name, last_name, payment_method):
    subject = f'✅ تأكيد طلبك رقم #{new_order.id} - متجر كتب'
    lines = [
        f'مرحباً {first_name} {last_name}،',
        '',
        f'تم استلام وتأكيد طلبك رقم #{new_order.id} بنجاح! 🎉',
        '',
        '📚 تفاصيل الطلب:',
    ]
    for item in cart_items:
        lines.append(
            f'  • {item["product"].name} × {item["quantity"]} '
            f'= {item["price"]}$'
        )
    lines += [
        '',
        f'💰 الإجمالي: {cart_total}$',
        f'💳 وسيلة الدفع: {payment_method}',
        f'📌 حالة الطلب: {new_order.get_status_display()}',
        '',
        'شكراً لتسوقك معنا! سيتم تجهيز طلبك في أقرب وقت.',
        '',
        '— فريق متجر كتب',
    ]
    message = '\n'.join(lines)
    html_message = None
    try:
        html_message = render_to_string('emails/order_confirmation.html', {
            'new_order': new_order,
            'cart_items': cart_items,
            'cart_total': cart_total,
            'email': email,
            'first_name': first_name,
            'last_name': last_name,
            'payment_method': payment_method,
        })
    except Exception:
        pass

    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            html_message=html_message,
            fail_silently=True,
        )
    except Exception:
        pass


# ── views ──────────────────────────────────────────────────────────────────

def index(request):
    products = product.objects.select_related('author').filter(featured=True)
    slides = slider.objects.order_by('order').all()
    return render(request, 'index.html', {
        'products': products,
        'sliders': slides,
    })


def cart(request):
    cart_items, cart_total = _load_cart(request)
    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'cart_total': cart_total,
    })


def add_to_cart(request, pid):
    cart_session = request.session.get('cart', {})
    pid_str = str(pid)
    cart_session[pid_str] = cart_session.get(pid_str, 0) + 1
    request.session['cart'] = cart_session
    
    try:
        p = product.objects.get(pk=pid)
        messages.success(request, f'تمت إضافة "{p.name}" إلى السلة بنجاح 🛒')
    except product.DoesNotExist:
        pass

    next_url = request.META.get('HTTP_REFERER', 'store:cart')
    return redirect(next_url)


def decrement_cart(request, pid):
    """Decrease quantity by 1, remove if 0."""
    cart_session = request.session.get('cart', {})
    pid_str = str(pid)
    if pid_str in cart_session:
        if cart_session[pid_str] > 1:
            cart_session[pid_str] -= 1
        else:
            del cart_session[pid_str]
        request.session['cart'] = cart_session
        try:
            p = product.objects.get(pk=pid)
            messages.info(request, f'تم تعديل كمية "{p.name}" في السلة')
        except product.DoesNotExist:
            pass

    next_url = request.META.get('HTTP_REFERER', 'store:cart')
    return redirect(next_url)


def remove_from_cart(request, pid):
    cart_session = request.session.get('cart', {})
    if str(pid) in cart_session:
        cart_session.pop(str(pid), None)
        request.session['cart'] = cart_session
        try:
            p = product.objects.get(pk=pid)
            messages.info(request, f'تم حذف "{p.name}" من السلة 🗑️')
        except product.DoesNotExist:
            pass

    next_url = request.META.get('HTTP_REFERER', 'store:cart')
    return redirect(next_url)


def checkout(request):
    cart_items, cart_total = _load_cart(request)
    if not cart_items:
        return redirect('store:cart')
    return render(request, 'checkout.html', {
        'cart_items': cart_items,
        'cart_total': cart_total,
        'stripe_public_key': getattr(settings, 'STRIPE_PUBLISHABLE_KEY', ''),
    })


def process_checkout(request):
    """POST handler: validate form, create order, handle Stripe or COD, send email."""
    if request.method != 'POST':
        return redirect('store:checkout')

    cart_items, cart_total = _load_cart(request)
    if not cart_items:
        return redirect('store:cart')

    # ── form validation ────────────────────────────────────────────────────
    first_name = request.POST.get('first_name', '').strip()
    last_name  = request.POST.get('last_name', '').strip()
    email      = request.POST.get('email', '').strip()
    phone      = request.POST.get('phone', '').strip()
    payment    = request.POST.get('payment_method', '').strip()

    errors = {}
    if not first_name:
        errors['first_name'] = 'الاسم الأول مطلوب.'
    if not last_name:
        errors['last_name'] = 'الاسم الأخير مطلوب.'
    if not email or '@' not in email:
        errors['email'] = 'بريد إلكتروني صحيح مطلوب.'
    if not payment:
        errors['payment'] = 'اختر وسيلة الدفع.'

    if errors:
        return render(request, 'checkout.html', {
            'cart_items': cart_items,
            'cart_total': cart_total,
            'errors': errors,
            'form_data': {
                'first_name': first_name,
                'last_name': last_name,
                'email': email,
                'phone': phone,
                'payment': payment,
            },
            'stripe_public_key': getattr(settings, 'STRIPE_PUBLISHABLE_KEY', ''),
        })

    # Determine status & method
    initial_status = 'pending'
    payment_display = 'الدفع عند الاستلام' if payment in ('cod', 'الدفع عند الاستلام') else 'بطاقة ائتمانية (Stripe)'

    # ── create order in DB ──────────────────────────────────────────────────
    new_order = order.objects.create(
        customer={
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'phone': phone,
            'payment_method': payment_display,
        },
        total_price=cart_total,
        status=initial_status,
        payment_method=payment,
    )
    for item in cart_items:
        orderproduct.objects.create(
            order=new_order,
            product=item['product'],
            quantity=item['quantity'],
            price=item['price'],
        )

    # ── Stripe Checkout Flow ────────────────────────────────────────────────
    stripe_key = getattr(settings, 'STRIPE_SECRET_KEY', '')
    is_real_stripe_key = stripe_key and stripe_key.startswith('sk_') and 'placeholder' not in stripe_key

    if payment in ('stripe', 'بطاقة ائتمانية'):
        if is_real_stripe_key:
            try:
                stripe.api_key = stripe_key
                line_items = []
                for item in cart_items:
                    line_items.append({
                        'price_data': {
                            'currency': 'usd',
                            'unit_amount': int(item['product'].price * 100),
                            'product_data': {
                                'name': item['product'].name,
                            },
                        },
                        'quantity': item['quantity'],
                    })

                success_url = request.build_absolute_uri(reverse('store:stripe-success')) + f'?session_id={{CHECKOUT_SESSION_ID}}&order_id={new_order.id}'
                cancel_url = request.build_absolute_uri(reverse('store:stripe-cancel')) + f'?order_id={new_order.id}'

                session = stripe.checkout.Session.create(
                    payment_method_types=['card'],
                    line_items=line_items,
                    mode='payment',
                    success_url=success_url,
                    cancel_url=cancel_url,
                    customer_email=email,
                    client_reference_id=str(new_order.id),
                )
                new_order.stripe_session_id = session.id
                new_order.save()
                return redirect(session.url, code=303)
            except Exception as e:
                errors['payment'] = f'حدث خطأ أثناء الاتصال ببوابة Stripe: {str(e)}'
                new_order.status = 'failed'
                new_order.save()
                return render(request, 'checkout.html', {
                    'cart_items': cart_items,
                    'cart_total': cart_total,
                    'errors': errors,
                    'form_data': {
                        'first_name': first_name,
                        'last_name': last_name,
                        'email': email,
                        'phone': phone,
                        'payment': payment,
                    },
                })
        else:
            # Simulated sandbox mode when placeholder key is in use
            new_order.status = 'paid'
            new_order.save()
            _send_order_email(new_order, cart_items, cart_total, email, first_name, last_name, payment_display + ' (وضع المحاكاة التجريبي)')
            request.session['cart'] = {}
            request.session['last_order_id'] = new_order.id
            messages.info(request, 'تمت معالجة الدفع بنجاح في وضع الاختبار التجريبي لـ Stripe.')
            return redirect(reverse('store:checkout-complete') + f'?order_id={new_order.id}')

    # ── Cash On Delivery (COD) Flow ─────────────────────────────────────────
    _send_order_email(new_order, cart_items, cart_total, email, first_name, last_name, payment_display)
    request.session['cart'] = {}
    request.session['last_order_id'] = new_order.id
    return redirect(reverse('store:checkout-complete') + f'?order_id={new_order.id}')


def stripe_success(request):
    """Callback from Stripe after successful checkout."""
    order_id = request.GET.get('order_id')
    session_id = request.GET.get('session_id')

    target_order = None
    if order_id:
        try:
            target_order = order.objects.get(pk=order_id)
            target_order.status = 'paid'
            if session_id:
                target_order.stripe_session_id = session_id
            target_order.save()
        except order.DoesNotExist:
            pass

    # Clear cart
    request.session['cart'] = {}
    messages.success(request, 'تمت عملية الدفع بنجاح عبر Stripe! 🎉')
    return redirect(reverse('store:checkout-complete') + (f'?order_id={order_id}' if order_id else ''))


def stripe_cancel(request):
    """Callback from Stripe if user cancelled checkout."""
    order_id = request.GET.get('order_id')
    if order_id:
        try:
            cancelled_order = order.objects.get(pk=order_id)
            cancelled_order.status = 'cancelled'
            cancelled_order.save()
        except order.DoesNotExist:
            pass

    messages.warning(request, 'تم إلغاء عملية الدفع عبر Stripe. يمكنك المحاولة مجدداً أو اختيار الدفع عند الاستلام.')
    return redirect('store:checkout')


def checkout_complete(request):
    order_id = request.GET.get('order_id') or request.session.get('last_order_id')
    current_order = None
    if order_id:
        current_order = order.objects.filter(pk=order_id).first()
    return render(request, 'checkout-complete.html', {
        'order': current_order,
    })


def product_view(request, pid):
    p = get_object_or_404(product, pk=pid)
    related_products = (
        product.objects
               .filter(category=p.category)
               .exclude(id=p.id)[:3]
    )
    return render(request, 'product.html', {
        'product': p,
        'related_products': related_products,
    })


def category_view(request, cid=None):
    if cid:
        c = get_object_or_404(category, pk=cid)
        products = product.objects.filter(category=c).select_related('author')
    else:
        c = None
        products = product.objects.all().select_related('author')

    categories = category.objects.all()
    return render(request, 'category.html', {
        'products': products,
        'category': c,
        'categories': categories,
    })


def search_view(request):
    query  = request.GET.get('q', '')
    cat_id = request.GET.get('category', '')

    results = product.objects.all().select_related('author', 'category')
    if query:
        results = results.filter(
            Q(name__icontains=query) | Q(short_description__icontains=query)
        )
    if cat_id:
        results = results.filter(category_id=cat_id)

    return render(request, 'search.html', {
        'query': query,
        'products': results,
    })
