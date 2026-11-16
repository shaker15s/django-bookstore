from django.db import models

# Create your models here.
class category(models.Model):
    """
    Represents a product category.
    """
    name = models.CharField(max_length=255, unique=True)
    featured = models.BooleanField(default=False)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
class Author(models.Model):
    """
    Represents an author of a product.
    """
    name = models.CharField(max_length=255)
    bio = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
class product(models.Model):
    """
    Represents a product item in the store.
    """
    name = models.CharField(max_length=255)
    short_description = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    featured = models.BooleanField(default=False)
    stock = models.IntegerField(default=0)
    image = models.ImageField(upload_to='product_images', blank=True, null=True)
    category = models.ForeignKey(category, on_delete=models.PROTECT)
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

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
    customer = models.JSONField(default=dict)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_method = models.CharField(max_length=50, default='cash')
    stripe_session_id = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"طلب #{self.id} - {self.get_status_display()}"

class orderproduct(models.Model):
    order = models.ForeignKey(order, on_delete=models.PROTECT)
    product = models.ForeignKey(product, on_delete=models.PROTECT)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.order.id) + " " + self.product.name
class slider(models.Model):
    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=500)
    image = models.ImageField(upload_to='slider_images', blank=True, null=True)
    order = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title