from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
    path('', views.index, name='home'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('checkout/process/', views.process_checkout, name='process-checkout'),
    path('checkout-complete/', views.checkout_complete, name='checkout-complete'),
    path('stripe/success/', views.stripe_success, name='stripe-success'),
    path('stripe/cancel/', views.stripe_cancel, name='stripe-cancel'),
    path('product/<int:pid>/', views.product_view, name='product'),
    path('category/', views.category_view, name='category'),
    path('category/<int:cid>/', views.category_view, name='category-detail'),
    path('search/', views.search_view, name='search'),
    path('add-to-cart/<int:pid>/', views.add_to_cart, name='add-to-cart'),
    path('decrement-cart/<int:pid>/', views.decrement_cart, name='decrement-cart'),
    path('remove-from-cart/<int:pid>/', views.remove_from_cart, name='remove-from-cart'),
]
