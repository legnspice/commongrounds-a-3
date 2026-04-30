from django.shortcuts import render
from django.db.models import Q

from .models import Book


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
    bookmarkCount = book.bookmarks.count()
    context = {
        "book": book,
        "bookmarkCount": bookmarkCount
    }
    return render(request, "book_detail.html", context)
