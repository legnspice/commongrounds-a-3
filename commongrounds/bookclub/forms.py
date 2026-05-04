from django import forms
from .models import Book, BookReview, Borrow

class BookReviewForm(forms.ModelForm):
    class Meta:
        model = BookReview
        fields = ['userReviewer', 'title', 'comment', 'anonReviewer']
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user and user.is_authenticated:
            self.fields.pop('anonReviewer')
            self.fields['userReviewer'].initial = user.profile
            self.fields['userReviewer'].disabled = True
        else:
            self.fields.pop('userReviewer')
            self.fields['anonReviewer'].initial = 'Anonymous'
            self.fields['anonReviewer'].disabled = True


class BookContributeForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'genre', 'author', 'synopsis', 'publicationYear', 'availableToBorrow' , 'contributor']
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user:
            self.fields['contributor'].initial = user.profile
            self.fields['contributor'].disabled = True

class BookUpdateForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'genre', 'author', 'synopsis', 'publicationYear', 'availableToBorrow']

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
        fields = ['name', 'dateBorrowed']
        labels = {
            'dateBorrowed': 'Date Borrowed',
        }
        widgets = {
            'dateBorrowed': forms.DateInput(attrs={'type': 'date'}),
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user and user.is_authenticated:
            self.fields['name'].initial = user.profile.displayName
            self.fields['name'].disabled = True
