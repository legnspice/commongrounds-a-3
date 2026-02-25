from django.db import models
from django.urls import reverse

class Genre(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

class Book(models.Model):
    title = models.CharField(max_length=255)
    genre = models.ForeignKey(
        Genre,
        on_delete=models.SET_NULL,
        related_name='books'
    )
    author = models.CharField()
    publicationYear = models.IntegerField()
    createdOn = models.DateTimeField()
    updatedOn = models.DateTimeField()
