from django.urls import path

from .views import EventListView, EventDetailView, EventCreateView, EventSignUpView

app_name = 'localevents'

urlpatterns = [
    path('events/', EventListView.as_view(), name='event_list'),
    path('events/new/', EventCreateView.as_view(), name='event_create'),
    path('events/<int:pk>/', EventDetailView.as_view(), name='event_detail'),
    path('events/<int:pk>/signup/', EventSignUpView.as_view(), name='event_signup'),
]