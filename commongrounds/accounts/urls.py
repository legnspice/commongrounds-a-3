from django.urls import path, include
from .views import profile_update_view, permission_denied, dashboard

urlpatterns = [
    path("dashboard/", dashboard, name="dashboard"),
    path('permission_denied/', permission_denied, name='permission_denied'),
    path('<username>/', profile_update_view, name='profile_update'),
]

app_name = 'accounts'