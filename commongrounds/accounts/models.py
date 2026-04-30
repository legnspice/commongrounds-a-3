from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    roleChoices = [
        ("Reader", "Reader"), #REMOVE THIS LATER!!! (value - 4 database, label 4 frontend ?? )
        ("Book Contributor", "Book Contributor")
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    displayName = models.CharField(max_length=63)
    emailAddress = models.EmailField()
    role = models.CharField(
        max_length=50,
        choices=roleChoices,
        default="Reader"
    )

    def __str__(self):
        return self.displayName

