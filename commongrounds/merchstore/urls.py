from django.urls import path
from .views import ItemListView, ItemDetailView

urlpatterns = [
    path('items', ItemListView.as_view(), name='item_list'),
    path('item/<int:pk>',
         ItemDetailView.as_view(), name='item_detail'),
]

app_name = "merchstore"
