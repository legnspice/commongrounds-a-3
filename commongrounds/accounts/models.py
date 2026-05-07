from django.db import models
from django.contrib.auth.models import User


class Role(models.Model):
    ROLE_CHOICES = [
        ("Market Seller", "Market Seller"),
        ("Event Organizer", "Event Organizer"),
        ("Book Contributor", "Book Contributor"),
        ("Project Creator", "Project Creator"),
        ("Commission Maker", "Commission Maker"),
    ]
    name = models.CharField(max_length=50, choices=ROLE_CHOICES, unique=True)

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    display_name = models.CharField(max_length=63)
    email_address = models.EmailField()
    roles = models.ManyToManyField(Role, related_name="profiles", blank=True)

    def has_role(self, role_name):
        return self.roles.filter(name=role_name).exists()

    def __str__(self):
        return self.display_name