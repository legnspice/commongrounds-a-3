from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .models import Product


class ItemListView(ListView):
    model = Product
    template_name = 'merchstore/items_list.html'
    context_object_name = 'products'


class ItemDetailView(DetailView):
    model = Product
    template_name = 'merchstore/item_detail.html'
    context_object_name = 'product'
