from django import forms
from .models import Commission,Job, JobApplication
from django.forms import inlineformset_factory

class CommissionForm(forms.ModelForm):
    class Meta:
        model = Commission
        fields = ['title', 'description', 'commission_type', 'people_required', 'status']
        widgets = {
            'status': forms.Select(),
        }

JobFormSet = inlineformset_factory(
    Commission,         
    Job,                
    fields=['role', 'manpower_required', 'status'],
    extra=5,            
    can_delete=True,  
)

class JobApplicationStatusForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = ['status']