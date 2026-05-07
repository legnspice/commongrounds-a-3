from django import forms

from .models import Event


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = [
            'title',
            'category',
            'location',
            'start_time',
            'end_time',
            'description',
            'event_capacity',
            'event_image',
            'status',
        ]

        widgets = {
            'start_time': forms.DateTimeInput(
                attrs={'type': 'datetime-local'},
                format='%Y-%m-%dT%H:%M'
            ),
            'end_time': forms.DateTimeInput(
                attrs={'type': 'datetime-local'},
                format='%Y-%m-%dT%H:%M'
            ),
            'description': forms.Textarea(
                attrs={'rows': 4, 'placeholder': 'Tell us about your event...'}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Adds Bootstrap classes to every field for a consistent look
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

    class GuestSignupForm(forms.Form):

        new_registrant = forms.CharField(
            max_length=200,
            label="Your Name",
            widget=forms.TextInput(attrs={
                'placeholder': 'Enter your full name',
                'class': 'form-control'
            })
        )
