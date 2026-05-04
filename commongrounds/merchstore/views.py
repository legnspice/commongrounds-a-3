from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from django.views.generic import DetailView, ListView, View
from django.views.generic.edit import CreateView, UpdateView, FormMixin
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Product, Transaction
from .forms import ProductForm, ProductUpdateForm, TransactionForm
from .strategies import AuthenticatedPurchaseStrategy, GuestPurchaseStrategy


class ItemListView(ListView):
    model = Product
    template_name = 'merchstore/items_list.html'
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            profile = self.request.user.profile
            context['my_products'] = Product.objects.filter(owner=profile)
            context['products'] = Product.objects.exclude(owner=profile)
        return context


class ItemDetailView(FormMixin, DetailView):
    model = Product
    template_name = 'merchstore/item_detail.html'
    context_object_name = 'product'
    form_class = TransactionForm

    def get_success_url(self):
        return reverse('merchstore:cart')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        return self.form_invalid(form)

    def form_valid(self, form):
        if self.request.user.is_authenticated and self.object.owner == self.request.user.profile:
            return self.form_invalid(form)
        if form.cleaned_data['amount'] > self.object.stock:
            return self.form_invalid(form)
        if self.request.user.is_authenticated:
            strategy = AuthenticatedPurchaseStrategy()
        else:
            strategy = GuestPurchaseStrategy()
        return strategy.execute(self.request, self.object, form)


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'merchstore/product_form.html'

    def form_valid(self, form):
        form.instance.owner = self.request.user.profile
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductUpdateForm
    template_name = 'merchstore/product_form.html'

    def form_valid(self, form):
        product = form.save(commit=False)
        if product.stock == 0:
            product.status = 'Out of stock'
        else:
            product.status = 'Available'
        product.save()
        return redirect(product.get_absolute_url())


class CartView(LoginRequiredMixin, ListView):
    model = Transaction
    template_name = 'merchstore/cart.html'
    context_object_name = 'transactions'

    def get_queryset(self):
        return Transaction.objects.filter(buyer=self.request.user.profile)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        grouped = {}
        for t in self.get_queryset():
            owner = t.product.owner
            grouped.setdefault(owner, []).append(t)
        context['grouped'] = grouped
        return context


class TransactionListView(LoginRequiredMixin, ListView):
    model = Transaction
    template_name = 'merchstore/transactions.html'
    context_object_name = 'transactions'

    def get_queryset(self):
        products = Product.objects.filter(owner=self.request.user.profile)
        return Transaction.objects.filter(product__in=products)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        grouped = {}
        for t in context['transactions']:
            grouped.setdefault(t.buyer, []).append(t)
        context['grouped'] = grouped
        return context


class CompletePurchaseView(LoginRequiredMixin, View):
    def get(self, request):
        pending = request.session.pop('pending_transaction', None)
        if pending:
            product = get_object_or_404(Product, pk=pending['product_id'])
            amount = pending['amount']
            if amount >= 1 and amount <= product.stock:
                Transaction.objects.create(
                    buyer=request.user.profile,
                    product=product,
                    amount=amount,
                )
                return redirect('merchstore:cart')
        return redirect('merchstore:item_list')
