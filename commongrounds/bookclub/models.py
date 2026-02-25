from django.db import models
from django.urls import reverse

class Genre(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()