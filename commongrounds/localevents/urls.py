from django.urls import path

from .views import EventListView, EventDetailView

app_name = 'localevents'

urlpatterns = [
    path('events/', EventListView.as_view(), name='event_list'),
    path('events/<int:pk>/', EventDetailView.as_view(), name='event_detail'),
]