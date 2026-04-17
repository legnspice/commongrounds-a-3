from django.urls import path, include
from views import profile_update_view

urlpatterns = [
    path('', include('django.contrib.auth.urls')),  
    path('<username>/', profile_update_view, name='profile_update'),
]

app_name = 'accounts'