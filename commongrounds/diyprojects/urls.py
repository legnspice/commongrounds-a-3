from django.urls import path
from . import views

app_name = 'diyprojects'

urlpatterns = [
    path('projects', views.project_list, name='project_list'),
    path('project/add', views.project_create, name='project_create'),
    path('project/<int:pk>', views.project_detail, name='project_detail'),
    path('project/<int:pk>/edit', views.project_update, name='project_update'),
]