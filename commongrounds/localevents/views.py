from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy

from .forms import EventForm

from django.views.generic import ListView, DetailView

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
                events_signed_up = Event.objects.filter(signups__user_registrant=profile)
                
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
    
class EventDetailView(DetailView):
        model = Event
        template_name = 'localevents/event_detail.html'
        context_object_name = 'event'

        def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            
            # Check if the user is logged in and already signed up
            if self.request.user.is_authenticated:
                try:
                    profile = self.request.user.profile
                    # .exists() returns True if a signup record matches this user and event
                    is_registered = EventSignup.objects.filter(
                        user_registrant=profile, 
                        event=self.object
                    ).exists()
                    context['is_registered'] = is_registered
                except AttributeError:
                    context['is_registered'] = False
            else:
                context['is_registered'] = False
                
            return context
        
class EventCreateView(LoginRequiredMixin, CreateView):
        model = Event
        form_class = EventForm
        template_name = 'localevents/event_form.html'
        success_url = reverse_lazy('localevents:event_list')

        def form_valid(self, form):
            # Automatically set the organizer to the logged-in user's profile
            form.instance.organizer = self.request.user.profile
            return super().form_valid(form)