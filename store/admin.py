from django.contrib import admin
from . import models
# Register your models here.

@admin.register(models.category)
class categoryAdmin(admin.ModelAdmin):
    list_per_page = 20

@admin.register(models.Author)
class AuthorAdmin(admin.ModelAdmin):
    list_per_page = 20

@admin.register(models.product)
class productAdmin(admin.ModelAdmin):
    list_per_page = 20

@admin.register(models.order)
class orderAdmin(admin.ModelAdmin):
    list_per_page = 20

@admin.register(models.orderproduct)
class orderproductAdmin(admin.ModelAdmin):
    list_per_page = 20

@admin.register(models.slider)
class sliderAdmin(admin.ModelAdmin):
    list_per_page = 20