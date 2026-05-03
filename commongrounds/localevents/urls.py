from django.urls import path

from .views import EventListView, EventDetailView, EventCreateView, EventSignupView, EventUpdateView, EventDeleteView, EventCancelSignUpView

app_name = 'localevents'

urlpatterns = [
    # Plural for the list
    path('events/', EventListView.as_view(), name='event_list'),
    
    # Singular for specific actions (as per rubric)
    path('event/add/', EventCreateView.as_view(), name='event_create'),
    path('event/<int:pk>/', EventDetailView.as_view(), name='event_detail'),
    path('event/<int:pk>/edit/', EventUpdateView.as_view(), name='event_update'),
    path('event/<int:pk>/signup/', EventSignupView.as_view(), name='event_signup'),
    path('event/<int:pk>/delete/', EventDeleteView.as_view(), name='event_delete'),
    path('event/<int:pk>/cancel/', EventCancelSignUpView.as_view(), name='event_cancel'),
]
