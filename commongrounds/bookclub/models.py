from django.db import models
from django.urls import reverse
from accounts.models import Profile

class Genre(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]


class Book(models.Model):
    title = models.CharField(max_length=255)
    genre = models.ForeignKey(
        Genre, on_delete=models.SET_NULL, related_name="books", null=True, blank=True
    )
    contributor = models.ForeignKey(
        Profile, on_delete=models.SET_NULL, related_name="contributed_books", null = True, blank=True
    )
    author = models.CharField(max_length=255)
    synopsis = models.TextField()
    publicationYear = models.IntegerField()
    availableToBorrow = models.BooleanField(default=True)
    createdOn = models.DateTimeField(auto_now_add=True)
    updatedOn = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("bookclub:book_detail", args=[str(self.id)])

    class Meta:
        ordering = ["-publicationYear"]

class BookReview(models.Model):
    userReviewer = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="reviews", null=True, blank=True
    )
    anonReviewer = models.TextField(blank=True)
    book = models.ForeignKey(
        Book, on_delete=models.CASCADE, related_name="reviews"
    )
    title = models.CharField(max_length=255)
    comment = models.TextField()

    def __str__(self):
        return f"{self.title} - {self.book.title}"

class Bookmark(models.Model):
    profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="bookmarks"
    )
    book = models.ForeignKey(
        Book, on_delete=models.CASCADE, related_name="bookmarks"
    )
    dateBookmarked = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.profile} bookmarked {self.book}"

class Borrow(models.Model):
    book = models.ForeignKey(
        Book, on_delete=models.CASCADE, related_name="borrows"
    )
    borrower = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="books_borrowed", null=True, blank=True
    )
    name = models.CharField(max_length=255, blank=True)
    dateBorrowed = models.DateField()
    dateToReturn = models.DateField()
    
    def __str__(self):
        return f"{self.book} borrowed by {self.borrower or self.name}"
