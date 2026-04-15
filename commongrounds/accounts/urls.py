from django.urls import path, include
from . import views

app_name = 'accounts'

urlpatterns = [
    path('', include('django.contrib.auth.urls')),  
    path('<username>/', views.profile_update, name='profile_update'),
]