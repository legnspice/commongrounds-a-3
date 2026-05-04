from django.urls import path
from .views import CommissionListView, CommissionDetailView, CommissionCreateView, CommissionUpdateView

urlpatterns = [
    path('requests', CommissionListView, name='commissionlist'),
    path('request/<int:pk>', CommissionDetailView,
         name='commissiondetail'),
    path('requests/create', CommissionCreateView, name='commissioncreate'),
    path('request/<int:pk>/update', CommissionListView, name='commissionupdate'),
]

app_name = "commissions"
