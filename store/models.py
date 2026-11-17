from django.db import models

# Create your models here.
class category(models.Model):
    """
    Represents a product category.
    """
    name = models.CharField(max_length=255, unique=True, verbose_name="اسم القسم")
    featured = models.BooleanField(default=False, verbose_name="مميز")
    order = models.IntegerField(default=0, verbose_name="الترتيب")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإنشاء")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاريخ التحديث")

    class Meta:
        verbose_name = "قسم"
        verbose_name_plural = "الأقسام"
        ordering = ['order', 'name']

    def __str__(self):
        return self.name


class Author(models.Model):
    """
    Represents an author of a product.
    """
    name = models.CharField(max_length=255, verbose_name="اسم المؤلف")
    bio = models.TextField(blank=True, null=True, verbose_name="نبذة عن المؤلف")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإنشاء")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاريخ التحديث")

    class Meta:
        verbose_name = "مؤلف"
        verbose_name_plural = "المؤلفون"
        ordering = ['name']

    def __str__(self):
        return self.name


class product(models.Model):
    """
    Represents a product item in the store.
    """
    name = models.CharField(max_length=255, verbose_name="اسم الكتاب / المنتج")
    short_description = models.TextField(blank=True, null=True, verbose_name="وصف مختصر")
    description = models.TextField(blank=True, null=True, verbose_name="الوصف الكامل")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="السعر ($)")
    featured = models.BooleanField(default=False, verbose_name="مميز في الصفحة الرئيسية")
    stock = models.IntegerField(default=0, verbose_name="المخزون")
    image = models.ImageField(upload_to='product_images', blank=True, null=True, verbose_name="الصورة")
    category = models.ForeignKey(category, on_delete=models.PROTECT, verbose_name="القسم")
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="المؤلف")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإضافة")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاريخ التحديث")

    class Meta:
        verbose_name = "كتاب"
        verbose_name_plural = "الكتب"
        ordering = ['-created_at']

    def __str__(self):
        return self.name    


class order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'قيد الانتظار'),
        ('paid', 'تم الدفع بنجاح'),
        ('failed', 'فشلت العملية'),
        ('delivered', 'تم التوصيل'),
        ('cancelled', 'ملغي'),
    ]
    customer = models.JSONField(default=dict, verbose_name="بيانات العميل")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="الإجمالي ($)")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="حالة الطلب")
    payment_method = models.CharField(max_length=50, default='cash', verbose_name="وسيلة الدفع")
    stripe_session_id = models.CharField(max_length=255, blank=True, null=True, verbose_name="معرف جلسة Stripe")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الطلب")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاريخ التحديث")

    class Meta:
        verbose_name = "طلب"
        verbose_name_plural = "الطلبات"
        ordering = ['-created_at']

    def __str__(self):
        return f"طلب #{self.id} - {self.get_status_display()}"


class orderproduct(models.Model):
    order = models.ForeignKey(order, on_delete=models.PROTECT, related_name='items', verbose_name="الطلب")
    product = models.ForeignKey(product, on_delete=models.PROTECT, verbose_name="المنتج")
    quantity = models.IntegerField(default=1, verbose_name="الكمية")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="السعر الإجمالي للكمية ($)")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإضافة")

    class Meta:
        verbose_name = "عنصر بالطلب"
        verbose_name_plural = "عناصر الطلبات"

    def __str__(self):
        return f"{self.product.name} × {self.quantity}"


class slider(models.Model):
    title = models.CharField(max_length=255, verbose_name="العنوان الرئيسي")
    subtitle = models.CharField(max_length=500, verbose_name="العنوان الفرعي")
    image = models.ImageField(upload_to='slider_images', blank=True, null=True, verbose_name="صورة الشريحة")
    order = models.IntegerField(default=1, verbose_name="الترتيب")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإنشاء")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاريخ التحديث")

    class Meta:
        verbose_name = "شريحة عرض (Slider)"
        verbose_name_plural = "شرائح العرض (Sliders)"
        ordering = ['order']

    def __str__(self):
        return self.title