from django.contrib import admin
from . import models

# Admin Branding
admin.site.site_header = "لوحة تحكم متجر كتب"
admin.site.site_title = "متجر كتب"
admin.site.index_title = "إدارة المتجر والمحتوى"


@admin.register(models.category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'featured', 'order', 'created_at')
    list_filter = ('featured',)
    search_fields = ('name',)
    list_editable = ('featured', 'order')
    list_per_page = 20


@admin.register(models.Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name', 'bio')
    list_per_page = 20


@admin.register(models.product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'author', 'price', 'stock', 'featured', 'created_at')
    list_filter = ('featured', 'category', 'author')
    search_fields = ('name', 'short_description', 'description')
    list_editable = ('price', 'stock', 'featured')
    list_per_page = 20


class OrderProductInline(admin.TabularInline):
    model = models.orderproduct
    extra = 0
    readonly_fields = ('product', 'quantity', 'price', 'created_at')
    can_delete = False


@admin.register(models.order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer_name', 'customer_email', 'total_price', 'status', 'payment_method', 'created_at')
    list_filter = ('status', 'payment_method', 'created_at')
    search_fields = ('id', 'stripe_session_id', 'customer')
    readonly_fields = ('total_price', 'created_at', 'updated_at', 'stripe_session_id')
    inlines = [OrderProductInline]
    list_per_page = 20

    @admin.display(description="اسم العميل")
    def customer_name(self, obj):
        first = obj.customer.get('first_name', '')
        last = obj.customer.get('last_name', '')
        return f"{first} {last}".strip() or "غير محدد"

    @admin.display(description="البريد الإلكتروني")
    def customer_email(self, obj):
        return obj.customer.get('email', '-')


@admin.register(models.orderproduct)
class OrderProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'product', 'quantity', 'price', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('order__id', 'product__name')
    list_per_page = 20


@admin.register(models.slider)
class SliderAdmin(admin.ModelAdmin):
    list_display = ('title', 'subtitle', 'order', 'created_at')
    list_editable = ('order',)
    search_fields = ('title', 'subtitle')
    list_per_page = 20
