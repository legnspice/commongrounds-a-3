from django.urls import path
from .views import ItemListView, ItemDetailView, ProductCreateView, ProductUpdateView, CartView, TransactionListView, CompletePurchaseView

urlpatterns = [
    path('items', ItemListView.as_view(), name='item_list'),
    path('item/add', ProductCreateView.as_view(), name='item_create'),
    path('cart', CartView.as_view(), name='cart'),
    path('transactions', TransactionListView.as_view(), name='transaction_list'),
    path('complete-purchase', CompletePurchaseView.as_view(), name='complete_purchase'),
    path('item/<int:pk>', ItemDetailView.as_view(), name='item_detail'),
    path('item/<int:pk>/edit', ProductUpdateView.as_view(), name='item_update'),
]

app_name = "merchstore"
