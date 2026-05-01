from django.urls import path

from .views import EventListView

app_name = 'localevents'

urlpatterns = [
    path('events/', EventListView.as_view(), name='event_list'),
]