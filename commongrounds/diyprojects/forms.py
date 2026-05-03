from django import forms
from .models import Project, ProjectCategory, ProjectReview, ProjectRating


class ProjectForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset=ProjectCategory.objects.all(),
        required=False,
    )

    class Meta:
        model = Project
        fields = ['title', 'category', 'description', 'materials', 'steps']


class ProjectReviewForm(forms.ModelForm):
    class Meta:
        model = ProjectReview
        fields = ['comment', 'image']


class ProjectRatingForm(forms.ModelForm):
    class Meta:
        model = ProjectRating
        fields = ['score']