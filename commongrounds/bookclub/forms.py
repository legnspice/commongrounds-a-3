from django import forms
from .models import Book, BookReview

class BookReviewForm(forms.ModelForm):
    class Meta:
        model = BookReview
        fields = ['title', 'comment']

class BookContributeForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'genre', 'author', 'synopsis', 'publicationYear']


class BookFormFactory:
    @classmethod
    def get_form(cls, context):
        if context == "review":
            return BookReviewForm
        elif context == "contribute":
            return BookContributeForm