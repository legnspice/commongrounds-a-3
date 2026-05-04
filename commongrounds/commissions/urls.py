from django.urls import path
from .views import CommissionListView, CommissionDetailView, CommissionCreateView, CommissionUpdateView, JobApplicationCreateView

urlpatterns = [
    path('requests', CommissionListView, name='commissionlist'),
    path('request/<int:pk>', CommissionDetailView,
         name='commissiondetail'),
    path('request/add', CommissionCreateView, name='commissioncreate'),
    path('request/<int:pk>/edit', CommissionUpdateView, name='commissionupdate'),
    path('request/job/<int:job_pk>/apply', JobApplicationCreateView, name='jobapply'),
]

app_name = "commissions"
