from django import forms
from .models import Book, BookReview

class BookReviewForm(forms.ModelForm):
    class Meta:
        model = BookReview
        fields = ['title', 'comment']

class BookFormFactory:
    @classmethod
    def get_form(cls, context):
        if context =="review":
            return BookReviewForm