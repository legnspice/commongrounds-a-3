from django.urls import path

from .views import EventListView, EventDetailView, EventCreateView, EventSignupView, EventUpdateView, EventDeleteView, EventCancelSignUpView

app_name = 'localevents'

urlpatterns = [
    path('events/', EventListView.as_view(), name='event_list'),
    path('events/new/', EventCreateView.as_view(), name='event_create'),
    path('events/<int:pk>/', EventDetailView.as_view(), name='event_detail'),
    path('events/<int:pk>/signup/', EventSignupView.as_view(), name='event_signup'),
    path('events/<int:pk>/edit/', EventUpdateView.as_view(), name='event_update'),
    path('events/<int:pk>/delete/', EventDeleteView.as_view(), name='event_delete'),
    path('events/<int:pk>/cancel/', EventCancelSignUpView.as_view(), name='event_cancel'),
]