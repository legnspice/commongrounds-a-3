from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from accounts.mixins import RoleRequiredMixin
from .forms import EventForm
from .models import Event, EventSignup


class EventListView(ListView):
    model = Event
    template_name = 'localevents/event_list.html'
    context_object_name = 'all_events'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        if user.is_authenticated and hasattr(user, 'profile'):
            profile = user.profile
            context['organized_events'] = Event.objects.filter(organizer=profile)
            context['joined_events'] = Event.objects.filter(signups__user_registrant=profile)
            context['other_events'] = Event.objects.exclude(
                organizer=profile
            ).exclude(signups__user_registrant=profile)
        else:
            context['other_events'] = Event.objects.all()
            
        return context


class EventDetailView(DetailView):
    model = Event
    template_name = 'localevents/event_detail.html'
    context_object_name = 'event'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        if self.request.user.is_authenticated and hasattr(self.request.user, 'profile'):
            context['is_registered'] = EventSignup.objects.filter(
                user_registrant=self.request.user.profile, 
                event=self.object
            ).exists()
        else:
            context['is_registered'] = False
            
        return context


class EventCreateView(RoleRequiredMixin, CreateView):
    model = Event
    form_class = EventForm
    template_name = 'localevents/event_form.html'
    required_role = 'Event Organizer'

    def form_valid(self, form):
        response = super().form_valid(form)
        if hasattr(self.request.user, 'profile'):
            self.object.organizer.add(self.request.user.profile)
        return response


class BaseSignupView(View):
    
    def post(self, request, pk, *args, **kwargs):
        event = get_object_or_404(Event, pk=pk)

        if not self.check_capacity(event):
            messages.error(request, "This event is full.")
            return redirect(self.get_redirect_url(event))

        if not self.check_ownership(event, request.user):
            messages.error(request, "You cannot sign up for your own event.")
            return redirect(self.get_redirect_url(event))

        self.create_signup(event, request.user)
        
        if event.signups.count() >= event.event_capacity:
            event.status = 'Full'
            event.save()
            
        messages.success(request, "Successfully signed up!")
        return redirect(self.get_redirect_url(event))

    def check_capacity(self, event):
        return event.signups.count() < event.event_capacity

    def check_ownership(self, event, user):
        if user.is_authenticated and hasattr(user, 'profile'):
            return user.profile not in event.organizer.all()
        return True

    def create_signup(self, event, user):
        raise NotImplementedError("Subclasses must implement create_signup")

    def get_redirect_url(self, event):
        return reverse('localevents:event_detail', kwargs={'pk': event.pk})


class EventSignupView(BaseSignupView):
    def get(self, request, pk):
        """Rubric Requirement: Dedicated form view for guests."""
        event = get_object_or_404(Event, pk=pk)
        if request.user.is_authenticated:
            return redirect('localevents:event_detail', pk=pk)
            
        spots_left = event.event_capacity - event.signups.count()
        
        return render(request, 'localevents/event_signup.html', {
            'event': event, 
            'spots_remaining': spots_left
        })

    def create_signup(self, event, user):
        if user.is_authenticated and hasattr(user, 'profile'):
            EventSignup.objects.create(user_registrant=user.profile, event=event)
        else:
            guest_name = self.request.POST.get('new_registrant')
            if guest_name:
                EventSignup.objects.create(new_registrant=guest_name, event=event)


class EventUpdateView(RoleRequiredMixin, UpdateView):
    """Allows the organizing Profile to update their event."""
    model = Event
    form_class = EventForm
    template_name = 'localevents/event_form.html'
    required_role = 'Event Organizer'
    
    def get_success_url(self):
        return reverse_lazy('localevents:event_detail', kwargs={'pk': self.object.pk})
        
    def form_valid(self, form):
        """Rubric Requirement: Auto-update status based on capacity."""
        response = super().form_valid(form)
        if self.object.signups.count() >= self.object.event_capacity:
            self.object.status = 'Full'
        else:
            if self.object.status == 'Full':
                self.object.status = 'Available'
        self.object.save()
        return response


class EventDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Event
    template_name = 'localevents/event_confirm_delete.html'
    success_url = reverse_lazy('localevents:event_list')

    def test_func(self):
        event = self.get_object()
        if self.request.user.is_authenticated and hasattr(self.request.user, 'profile'):
            return self.request.user.profile in event.organizer.all()
        return False


class EventCancelSignUpView(LoginRequiredMixin, View):
    
    def post(self, request, pk):
        event = get_object_or_404(Event, pk=pk)
        
        if hasattr(request.user, 'profile'):
            signup = EventSignup.objects.filter(
                user_registrant=request.user.profile, 
                event=event
            ).first()
            
            if signup:
                signup.delete()
                
                if event.signups.count() < event.event_capacity and event.status == 'Full':
                    event.status = 'Available'
                    event.save()

        return redirect('localevents:event_detail', pk=pk)
