from django.shortcuts import redirect
from django.urls import reverse
from .models import Transaction


class BaseTransactionStrategy:
    def execute(self, request, product, form):
        raise NotImplementedError


class AuthenticatedPurchaseStrategy(BaseTransactionStrategy):
    def execute(self, request, product, form):
        transaction = form.save(commit=False)
        transaction.buyer = request.user.profile
        transaction.product = product
        transaction.save()
        return redirect('merchstore:cart')


class GuestPurchaseStrategy(BaseTransactionStrategy):
    def execute(self, request, product, form):
        request.session['pending_transaction'] = {
            'product_id': product.pk,
            'amount': form.cleaned_data['amount'],
        }
        return redirect(f"{reverse('login')}?next={reverse('merchstore:complete_purchase')}")
