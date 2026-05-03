from django import forms
from .models import Event

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        # Include the new field names from the rubric
        fields = [
            'title', 
            'category', 
            'location', 
            'start_time', 
            'end_time', 
            'description', 
            'event_capacity', 
            'event_image', 
            'status'
        ]
        
        # We use widgets so the browser shows a proper calendar/time picker
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
            'description': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Tell us about your event...'}),
        }

    def __init__(self, *args, **kwargs):
        super(EventForm, self). __init__(*args, **kwargs)
        # Optional: Add Bootstrap classes if you're using it for styling
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})