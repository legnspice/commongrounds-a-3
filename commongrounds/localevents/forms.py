from django import forms
from .models import Event

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        # We exclude 'organizer' and 'status' because we will handle those automatically
        fields = ['name', 'location', 'date', 'description', 'capacity']
        
        # This adds a nice calendar/clock popup for the date field
        widgets = {
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }