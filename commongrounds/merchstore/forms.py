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

    def clean_amount(self):
        amount = self.cleaned_data['amount']
        if amount < 1:
            raise forms.ValidationError("Amount must be at least 1.")
        return amount
