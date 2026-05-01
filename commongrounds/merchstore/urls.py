from django.urls import path
from .views import ItemListView, ItemDetailView, ProductCreateView, ProductUpdateView, CartView, TransactionListView

urlpatterns = [
    path('items', ItemListView.as_view(), name='item_list'),
    path('item/add', ProductCreateView.as_view(), name='item_create'),
    path('item/<int:pk>', ItemDetailView.as_view(), name='item_detail'),
    path('item/<int:pk>/edit', ProductUpdateView.as_view(), name='item_update'),
    path('cart', CartView.as_view(), name='cart'),
    path('transactions', TransactionListView.as_view(), name='transaction_list'),
]

app_name = "merchstore"
