from django.urls import path
from .views import ItemListView, ItemDetailView

urlpatterns = [
    path('items', ItemListView.as_view(), name='ItemList'),
    path('item/<int:pk>',
         ItemDetailView.as_view(), name='ItemDetail'),
]

app_name = "merchstore"
