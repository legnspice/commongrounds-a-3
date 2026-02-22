from django.urls import path
from .views import CommissionListView,CommissionDetailView

urlpatterns = [
    path('commissions/requests',CommissionListView.as_view(), name='commissionlist'),
    path('commissions/request/<int:pk>',CommissionDetailView.as_view(), name='commissiondetail'),
]

app_name = "commissions"