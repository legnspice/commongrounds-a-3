from django.urls import path

from .views import book_detail, book_list

urlpatterns = [
    path("books", book_list, name="books"),
    path("book/<int:pk>", book_detail, name="book_detail"),
]

app_name = "bookclub"
