from django.urls import path
from .views import CommissionListView

urlpatterns = [
    path('commissions/requests',CommissionListView.as_view(), name='commissionlist'),
]

app_name = "commissions"