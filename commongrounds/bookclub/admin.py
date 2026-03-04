from django.contrib import admin

from .models import Book, Genre


class GenreAdmin(admin.ModelAdmin):
    model = Genre


class BookAdmin(admin.ModelAdmin):
    model = Book


admin.site.register(Book, BookAdmin)
admin.site.register(Genre, GenreAdmin)
