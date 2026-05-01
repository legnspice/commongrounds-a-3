from django.views.generic import ListView

from .models import Event


class EventListView(ListView):
    model = Event
    template_name = 'localevents/event_list.html'
    context_object_name = 'all_events'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Check if user is authenticated AND has a profile
        if self.request.user.is_authenticated:
            try:
                profile = self.request.user.profile
                
                events_created = Event.objects.filter(organizer=profile)
                events_signed_up = Event.objects.filter(eventsignup__user_registrant=profile)
                
                # Exclude specific events from the main list
                all_events = Event.objects.exclude(
                    id__in=events_created.values('id')
                ).exclude(
                    id__in=events_signed_up.values('id')
                )
                
                context['events_created'] = events_created
                context['events_signed_up'] = events_signed_up
                context['all_events'] = all_events
            except AttributeError:
                # Fallback if profile doesn't exist for this user
                context['all_events'] = Event.objects.all()
        else:
            context['all_events'] = Event.objects.all()
            
        return context