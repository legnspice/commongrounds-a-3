from django.contrib import admin

from .models import Book, Genre, Bookmark, BookReview, Borrow


class GenreAdmin(admin.ModelAdmin):
    model = Genre

class BookAdmin(admin.ModelAdmin):
    model = Book
    
    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return []
        return ['genre']

class BookmarkAdmin(admin.ModelAdmin):
    model = Bookmark

class BookReviewAdmin(admin.ModelAdmin):
    model = BookReview

class BorrowAdmin(admin.ModelAdmin):
    model = Borrow


admin.site.register(Book, BookAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Bookmark, BookmarkAdmin)
admin.site.register(BookReview, BookReviewAdmin)
admin.site.register(Borrow, BorrowAdmin)

