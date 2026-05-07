from django import forms
from .models import Book, BookReview, Borrow

class BookReviewForm(forms.ModelForm):
    class Meta:
        model = BookReview
        fields = ['user_reviewer', 'title', 'comment', 'anon_reviewer']
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user and user.is_authenticated:
            self.fields.pop('anon_reviewer')
            self.fields['user_reviewer'].initial = user.profile
            self.fields['user_reviewer'].disabled = True
        else:
            self.fields.pop('user_reviewer')
            self.fields['anon_reviewer'].initial = 'Anonymous'
            self.fields['anon_reviewer'].disabled = True


class BookContributeForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'genre', 'author', 'synopsis', 'publication_year', 'available_to_borrow' , 'contributor']
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user:
            self.fields['contributor'].initial = user.profile
            self.fields['contributor'].disabled = True

class BookUpdateForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'genre', 'author', 'synopsis', 'publication_year', 'available_to_borrow']

class BookFormFactory:
    @classmethod
    def get_form(cls, context):
        if context == 'review':
            return BookReviewForm
        elif context == 'contribute':
            return BookContributeForm
        elif context == 'update':
            return BookUpdateForm
        
class BookBorrowForm(forms.ModelForm):
    class Meta:
        model = Borrow
        fields = ['name', 'date_borrowed']
        labels = {
            'date_borrowed': 'Date Borrowed',
        }
        widgets = {
            'date_borrowed': forms.DateInput(attrs={'type': 'date'}),
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user and user.is_authenticated:
            self.fields['name'].initial = user.profile.display_name
            self.fields['name'].disabled = True
