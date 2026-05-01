from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from accounts.decorators import role_required
from .models import Book, Bookmark
from .forms import BookFormFactory

from django.db.models import Q


def book_list(request):
    context = {}

    if request.user.is_authenticated:
        profile = request.user.profile

        contributed_books = Book.objects.filter(contributor=profile)
        bookmarked_books = Book.objects.filter(bookmarks__profile=profile)
        reviewed_books = Book.objects.filter(reviews__userReviewer=profile).distinct()

        all_books =  Book.objects.exclude(
            Q(contributor=profile)
            |Q(bookmarks__profile=profile)
            |Q(reviews__userReviewer=profile)
        ).distinct()

        context = {
            "contributed_books": contributed_books,
            "bookmarked_books": bookmarked_books,
            "reviewed_books": reviewed_books,
            "all_books": all_books
        }
    else:
        all_books = Book.objects.all()
        context = {"all_books": all_books}
    return render(request, "book_list.html", context)


def book_detail(request, pk):
    book = Book.objects.get(pk=pk)

    reviewForm = BookFormFactory.get_form('review')

    if request.method == 'POST':
        form = reviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.book = book

            if request.user.is_authenticated:
                review.userReviewer = request.user.profile
            else:
                review.anonReviewer = 'Anonymous'
            
            review.save()
            return redirect('bookclub:book_detail', pk=book.pk)
    else:
        form = reviewForm()

    bookmarkCount = book.bookmarks.count()
    context = {
        'book': book,
        'bookmarkCount': bookmarkCount,
        'form': form
    }
    return render(request, 'book_detail.html', context)

@login_required
def bookmark_book(request, pk):
    book = Book.objects.get(pk=pk)
    Bookmark.objects.get_or_create(profile=request.user.profile, book=book)
    return redirect('bookclub:book_detail', pk=book.pk)

@role_required('Book Contributor')
def book_add(request):
    bookForm = BookFormFactory.get_form('contribute')

    if request.method == 'POST':
        form = bookForm(request.POST)
        if form.is_valid():
            book = form.save(commit=False)
            book.contributor = request.user.profile
            book.save()
            return redirect(book)
    else:
        form = bookForm()

    context = {
        'form': form,
    }

    return render(request, "book_create.html", context)

@role_required('Book Contributor')
def book_update(request, pk):
    book = Book.objects.get(pk=pk)  
    bookForm = BookFormFactory.get_form('contribute')

    if request.method == 'POST':
        form = bookForm(instance=book)
        if form.is_valid():
            book = form.save(commit=False)
            book.contributor = request.user.profile
            book.save()
            return redirect(book)
    else:
        form = bookForm(instance=book)

    context = {
        'form': form,
    }

    return render(request, "book_create.html", context)