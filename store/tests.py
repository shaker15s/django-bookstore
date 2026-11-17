from django.test import TestCase, Client
from django.urls import reverse
from store.models import category, Author, product, order, orderproduct, slider


class ModelSmokeTests(TestCase):
    def setUp(self):
        self.cat = category.objects.create(name="بايثون", featured=True, order=1)
        self.author = Author.objects.create(name="طارق علي", bio="خبير برمجيات")
        self.prod = product.objects.create(
            name="كتاب بايثون المتقدم",
            price=29.99,
            category=self.cat,
            author=self.author,
            featured=True,
            stock=10
        )
        self.slider = slider.objects.create(title="شريحة تجريبية", subtitle="وصف", order=1)

    def test_string_representations(self):
        self.assertEqual(str(self.cat), "بايثون")
        self.assertEqual(str(self.author), "طارق علي")
        self.assertEqual(str(self.prod), "كتاب بايثون المتقدم")
        self.assertEqual(str(self.slider), "شريحة تجريبية")

    def test_order_creation_and_status(self):
        new_order = order.objects.create(
            customer={"first_name": "أحمد", "last_name": "محمد", "email": "ahmed@example.com"},
            total_price=29.99,
            status="pending",
            payment_method="cod"
        )
        item = orderproduct.objects.create(
            order=new_order,
            product=self.prod,
            quantity=1,
            price=29.99
        )
        self.assertIn("طلب #", str(new_order))
        self.assertEqual(new_order.status, "pending")
        self.assertEqual(item.quantity, 1)


class StoreViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.cat = category.objects.create(name="تطوير الويب", featured=True)
        self.author = Author.objects.create(name="محمد سالم")
        self.prod = product.objects.create(
            name="كتاب Django الشامل",
            price=35.00,
            category=self.cat,
            author=self.author,
            featured=True,
            stock=5
        )

    def test_index_page(self):
        response = self.client.get(reverse('store:home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "كتاب Django الشامل")

    def test_category_views(self):
        response = self.client.get(reverse('store:category'))
        self.assertEqual(response.status_code, 200)
        response_detail = self.client.get(reverse('store:category-detail', args=[self.cat.id]))
        self.assertEqual(response_detail.status_code, 200)

    def test_product_detail_and_404(self):
        response = self.client.get(reverse('store:product', args=[self.prod.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.prod.name)

        # Invalid PID should return 404
        response_404 = self.client.get(reverse('store:product', args=[9999]))
        self.assertEqual(response_404.status_code, 404)

    def test_search_view(self):
        response = self.client.get(reverse('store:search') + '?q=Django')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "كتاب Django الشامل")

        response_empty = self.client.get(reverse('store:search') + '?q=غير_موجود')
        self.assertEqual(response_empty.status_code, 200)
        self.assertNotContains(response_empty, "كتاب Django الشامل")

    def test_cart_operations(self):
        pid = self.prod.id

        # 1. Add to cart
        self.client.get(reverse('store:add-to-cart', args=[pid]))
        session = self.client.session
        self.assertEqual(session.get('cart', {}).get(str(pid)), 1)

        # 2. Add second item
        self.client.get(reverse('store:add-to-cart', args=[pid]))
        session = self.client.session
        self.assertEqual(session.get('cart', {}).get(str(pid)), 2)

        # 3. Decrement cart
        self.client.get(reverse('store:decrement-cart', args=[pid]))
        session = self.client.session
        self.assertEqual(session.get('cart', {}).get(str(pid)), 1)

        # 4. Decrement again -> should remove from cart
        self.client.get(reverse('store:decrement-cart', args=[pid]))
        session = self.client.session
        self.assertNotIn(str(pid), session.get('cart', {}))

        # 5. Remove directly
        self.client.get(reverse('store:add-to-cart', args=[pid]))
        self.client.get(reverse('store:remove-from-cart', args=[pid]))
        session = self.client.session
        self.assertNotIn(str(pid), session.get('cart', {}))

    def test_checkout_validation_and_cod(self):
        # Empty cart redirects
        response = self.client.get(reverse('store:checkout'))
        self.assertEqual(response.status_code, 302)

        # Add item to cart
        self.client.get(reverse('store:add-to-cart', args=[self.prod.id]))

        # Checkout page loads
        response = self.client.get(reverse('store:checkout'))
        self.assertEqual(response.status_code, 200)

        # Missing required fields returns validation errors
        invalid_post = self.client.post(reverse('store:process-checkout'), {
            'first_name': '',
            'last_name': '',
            'email': 'invalid-email',
            'payment_method': ''
        })
        self.assertEqual(invalid_post.status_code, 200)
        self.assertContains(invalid_post, 'الاسم الأول مطلوب')

        # Valid COD order
        valid_post = self.client.post(reverse('store:process-checkout'), {
            'first_name': 'عمر',
            'last_name': 'شريف',
            'email': 'omar@example.com',
            'phone': '+201000000000',
            'payment_method': 'cod'
        })
        self.assertEqual(valid_post.status_code, 302)
        self.assertIn('checkout-complete', valid_post.url)

        # Cart should be cleared after order
        session = self.client.session
        self.assertEqual(session.get('cart'), {})

    def test_stripe_cancel_callback(self):
        new_order = order.objects.create(
            customer={"first_name": "خالد"},
            total_price=50.00,
            status="pending"
        )
        response = self.client.get(reverse('store:stripe-cancel') + f'?order_id={new_order.id}')
        self.assertEqual(response.status_code, 302)
        new_order.refresh_from_db()
        self.assertEqual(new_order.status, "cancelled")
