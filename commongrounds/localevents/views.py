from django.views.generic import ListView

from .models import Event


class EventListView(ListView):
    model = Event
    template_name = 'localevents/event_list.html'
    context_object_name = 'all_events'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        if self.request.user.is_authenticated:
            # Retrieve the user's profile from the newly linked accounts app
            profile = self.request.user.profile
            
            # 1. Events organized by the logged-in user
            events_created = Event.objects.filter(organizer=profile)
            
            # 2. Events the user has registered for
            events_signed_up = Event.objects.filter(
                eventsignup__user_registrant=profile
            )
            
            # 3. All remaining events
            all_events = Event.objects.exclude(
                id__in=events_created.values('id')
            ).exclude(
                id__in=events_signed_up.values('id')
            )
            
            # Pass the groups to the template
            context['events_created'] = events_created
            context['events_signed_up'] = events_signed_up
            context['all_events'] = all_events
            
        return context