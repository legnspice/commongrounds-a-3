from django.contrib import admin
from .models import Product, ProductType


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'product_type', 'price')


class ProductTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)


admin.site.register(Product, ProductAdmin)
admin.site.register(ProductType, ProductTypeAdmin)
