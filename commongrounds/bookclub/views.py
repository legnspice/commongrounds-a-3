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
        reviewed_books = Book.objects.filter(reviews__user_reviewer=profile).distinct()

        all_books =  Book.objects.exclude(
            Q(contributor=profile)
            |Q(bookmarks__profile=profile)
            |Q(reviews__user_reviewer=profile)
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

    review_form = BookFormFactory.get_form('review')

    if request.method == 'POST':
        form = review_form(request.POST, user=request.user)
        if form.is_valid():
            review = form.save(commit=False)
            review.book = book   
            review.save()
            return redirect('bookclub:book_detail', pk=book.pk)
    else:
        form = review_form(user=request.user)

    bookmark_count = book.bookmarks.count()
    context = {
        'book': book,
        'bookmark_count': bookmark_count,
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
    book_form = BookFormFactory.get_form('contribute')

    if request.method == 'POST':
        form = book_form(request.POST,  user=request.user)
        if form.is_valid():
            book = form.save()
            return redirect(book)
    else:
        form = book_form(user=request.user)

    context = {
        'form': form,
        'heading': "Add A Book"
    }

    return render(request, "book_form.html", context)

@role_required('Book Contributor')
def book_update(request, pk):
    book = Book.objects.get(pk=pk)  
    book_form = BookFormFactory.get_form('update')

    if request.method == 'POST':
        form = book_form(request.POST, instance=book)
        if form.is_valid():
            book = form.save(commit=False)
            book.save()
            return redirect(book)
    else:
        form = book_form(instance=book)

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
            
            borrow.date_to_return = borrow.date_borrowed + timedelta(days=14)

            borrow.save()
            return redirect(book)  
    else:
        form = BookBorrowForm(user=request.user)
    
    context = {
        'book': book, 
        'form': form
    }
    return render(request, 'book_borrow.html', context)
