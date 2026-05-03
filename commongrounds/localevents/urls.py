from django.urls import path

from .views import (
    EventCancelSignUpView,
    EventCreateView,
    EventDeleteView,
    EventDetailView,
    EventListView,
    EventSignupView,
    EventUpdateView,
)

app_name = 'localevents'

urlpatterns = [
    # Plural for the main list view
    path('events/', EventListView.as_view(), name='event_list'),
    
    # Singular for specific actions (Rubric Requirement)
    path('event/add/', EventCreateView.as_view(), name='event_create'),
    path('event/<int:pk>/', EventDetailView.as_view(), name='event_detail'),
    path('event/<int:pk>/edit/', EventUpdateView.as_view(), name='event_update'),
    path('event/<int:pk>/signup/', EventSignupView.as_view(), name='event_signup'),
    
    # Additional lifecycle views
    path('event/<int:pk>/delete/', EventDeleteView.as_view(), name='event_delete'),
    path('event/<int:pk>/cancel/', EventCancelSignUpView.as_view(), name='event_cancel'),
]
