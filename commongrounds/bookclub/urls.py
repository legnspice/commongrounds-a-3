from django.urls import path

from .views import book_detail, book_list

urlpatterns = [
    path("books", book_list, name="books"),
    path("book/<int:pk>", book_detail, name="book_detail"),
    # path("book/add", name="book_create"),
    # path("book/<int:pk>/edit", name="book_edit"),
    # path("book/<int:pk>/borrow", name="book_borrow")
]

app_name = "bookclub"
