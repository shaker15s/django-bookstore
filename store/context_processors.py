from store.models import category, product


def global_context(request):
    """
    Injects global data into every template:
    - all_categories: for the nav and search bar
    - cart_count: number of *unique valid* products in cart (not total qty)
    """
    cart = request.session.get('cart', {})

    # Only count products that still exist in the DB
    # This also auto-cleans orphaned session entries from seed resets
    if cart:
        valid_pids = set(
            str(p) for p in
            product.objects.filter(pk__in=list(cart.keys()))
                           .values_list('id', flat=True)
        )
        # Remove any stale product IDs silently
        stale = [pid for pid in cart if pid not in valid_pids]
        if stale:
            for pid in stale:
                del cart[pid]
            request.session['cart'] = cart

        cart_count = sum(
            qty for pid, qty in cart.items() if pid in valid_pids
        )
    else:
        cart_count = 0

    return {
        'all_categories': category.objects.all(),
        'cart_count': cart_count,
    }
