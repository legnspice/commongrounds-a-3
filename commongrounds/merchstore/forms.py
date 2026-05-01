from django import forms
from .models import Product, Transaction


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'product_type', 'image', 'description', 'price', 'stock', 'status']
        widgets = {
            'product_type': forms.Select,
            'status': forms.Select,
        }


class ProductUpdateForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'product_type', 'image', 'description', 'price', 'stock', 'status']
        widgets = {
            'product_type': forms.Select,
            'status': forms.Select,
        }


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['amount']
