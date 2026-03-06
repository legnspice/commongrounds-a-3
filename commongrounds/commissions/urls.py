from django.urls import path
from .views import CommissionListView, CommissionDetailView

urlpatterns = [
    path('requests', CommissionListView.as_view(), name='commissionlist'),
    path('request/<int:pk>', CommissionDetailView.as_view(), name='commissiondetail'),
]

app_name = "commissions"
