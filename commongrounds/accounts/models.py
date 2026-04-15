from django.db import models
from django.contrib.auth.models import User

class Profile(User):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    displayName = models.TextField(max_length=63)
    emailAddress = models.EmailField()

