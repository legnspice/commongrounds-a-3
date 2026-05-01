from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy, reverse

from .forms import EventForm

from django.views.generic import ListView, DetailView

from .models import Event, EventSignup


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
    
class BaseSignupView(View):
    """
    Abstract base CBV defining the Template Method skeleton.
    """
    def post(self, request, pk):
        # The Skeleton Algorithm
        event = get_object_or_404(Event, pk=pk)
        
        # Only create the signup if capacity allows and they aren't the organizer
        if self.check_capacity(event) and self.check_ownership(event, request.user):
            self.create_signup(event, request.user)
            
        return redirect(self.get_redirect_url(event))

    # --- Abstract Methods to be overridden ---
    def check_capacity(self, event):
        raise NotImplementedError

    def check_ownership(self, event, user):
        raise NotImplementedError

    def create_signup(self, event, user):
        raise NotImplementedError

    def get_redirect_url(self, event):
        raise NotImplementedError


class EventSignupView(BaseSignupView):
    """
    Concrete subclass implementing the Local Events specific logic.
    """
    def check_capacity(self, event):
        # Returns True if signup is still allowed
        return event.signups.count() < event.capacity

    def check_ownership(self, event, user):
        # Returns True if the user is NOT the organizer
        if user.is_authenticated and hasattr(user, 'profile'):
            return user.profile != event.organizer
        return True 

    def create_signup(self, event, user):
        # Creates the signup record, preventing duplicates
        if user.is_authenticated and hasattr(user, 'profile'):
            profile = user.profile
            if not EventSignup.objects.filter(user_registrant=profile, event=event).exists():
                EventSignup.objects.create(user_registrant=profile, event=event)

    def get_redirect_url(self, event):
        # Demonstrably overriding the method as required by the spec
        return reverse('localevents:event_detail', kwargs={'pk': event.pk})
    
class EventUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Event
    form_class = EventForm
    template_name = 'localevents/event_form.html'
    
    # Send them back to the detail page after editing
    def get_success_url(self):
        return reverse_lazy('localevents:event_detail', kwargs={'pk': self.object.pk})

    # SECURITY: Only let the organizer edit this event
    def test_func(self):
        event = self.get_object()
        try:
            return self.request.user.profile == event.organizer
        except AttributeError:
            return False

class EventDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Event
    template_name = 'localevents/event_confirm_delete.html'
    success_url = reverse_lazy('localevents:event_list')

    # SECURITY: Only let the organizer delete this event
    def test_func(self):
        event = self.get_object()
        try:
            return self.request.user.profile == event.organizer
        except AttributeError:
            return False

class EventCancelSignUpView(LoginRequiredMixin, View):
    def post(self, request, pk):
        # 1. Fetch the exact event
        event = get_object_or_404(Event, pk=pk)
        profile = request.user.profile

        # 2. Find the specific signup record for this user and event
        signup = EventSignup.objects.filter(user_registrant=profile, event=event).first()
        
        # 3. If the record exists, delete it!
        if signup:
            signup.delete()

        # 4. Refresh the detail page
        return redirect('localevents:event_detail', pk=pk)
    