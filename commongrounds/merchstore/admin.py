from django.contrib import admin
from .models import Product, ProductType, Transaction


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'product_type', 'owner', 'price', 'stock', 'status')


class ProductTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)


class TransactionAdmin(admin.ModelAdmin):
    list_display = ('buyer', 'product', 'amount', 'status', 'created_on')


admin.site.register(Product, ProductAdmin)
admin.site.register(ProductType, ProductTypeAdmin)
admin.site.register(Transaction, TransactionAdmin)
