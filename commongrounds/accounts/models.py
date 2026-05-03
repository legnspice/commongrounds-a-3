from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    displayName = models.CharField(max_length=63)
    emailAddress = models.EmailField()

    def __str__(self):
        return self.displayName

