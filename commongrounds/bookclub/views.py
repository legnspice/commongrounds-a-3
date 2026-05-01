from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from accounts.decorators import role_required
from .models import Book, Bookmark
from .forms import BookFormFactory, BookBorrowForm

from django.db.models import Q
from datetime import timedelta


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
        form = reviewForm(request.POST, user=request.user)
        if form.is_valid():
            review = form.save(commit=False)
            review.book = book   
            review.save()
            return redirect('bookclub:book_detail', pk=book.pk)
    else:
        form = reviewForm(user=request.user)

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
        form = bookForm(request.POST,  user=request.user)
        if form.is_valid():
            book = form.save()
            return redirect(book)
    else:
        form = bookForm(user=request.user)

    context = {
        'form': form,
        'heading': "Add A Book"
    }

    return render(request, "book_form.html", context)

@role_required('Book Contributor')
def book_update(request, pk):
    book = Book.objects.get(pk=pk)  
    bookForm = BookFormFactory.get_form('update')

    if request.method == 'POST':
        form = bookForm(request.POST, instance=book)
        if form.is_valid():
            book = form.save(commit=False)
            book.save()
            return redirect(book)
    else:
        form = bookForm(instance=book)

    context = {
        'form': form,
        'heading': "Edit A Book: " + book.title
    }

    return render(request, "book_form.html", context)

def book_borrow(request, pk):
    book = Book.objects.get(pk=pk)

    if request.method == 'POST':
        form = BookBorrowForm(request.POST, user=request.user)
        if form.is_valid():
            borrow = form.save(commit=False)
            borrow.book = book

            if request.user.is_authenticated:
                borrow.borrower = request.user.profile
            
            borrow.dateToReturn = borrow.dateBorrowed + timedelta(days=14)

            borrow.save()
            return redirect(book)  
    else:
        form = BookBorrowForm(user=request.user)
    
    context = {
        'book': book, 
        'form': form
    }
    return render(request, 'book_borrow.html', context)
