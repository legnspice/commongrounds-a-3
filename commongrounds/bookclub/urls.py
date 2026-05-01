from django.urls import path

from .views import book_detail, book_list, bookmark_book, book_add, book_update, book_borrow

urlpatterns = [
    path("books/", book_list, name="books"),
    path("book/<int:pk>", book_detail, name="book_detail"),
    path("book/<int:pk>/bookmark", bookmark_book, name="bookmark_book"),
    path("book/add", book_add, name="book_create"),
    path("book/<int:pk>/edit", book_update ,name="book_edit"),
    path("book/<int:pk>/borrow", book_borrow, name="book_borrow")
]

app_name = "bookclub"
