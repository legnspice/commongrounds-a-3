from django.db import models

# Import Profile from the accounts app managed by your teammate
from accounts.models import Profile


class EventType(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    class Meta:
        # Types sorted by name in ascending order
        ordering = ['name']

    def __str__(self):
        return self.name


class Event(models.Model):
    STATUS_CHOICES = [
        ('Available', 'Available'),
        ('Full', 'Full'),
        ('Done', 'Done'),
        ('Cancelled', 'Cancelled'),
    ]

    title = models.CharField(max_length=255)
    # Category cannot be modified by regular users[cite: 2]
    category = models.ForeignKey(
        EventType,
        on_delete=models.SET_NULL,
        null=True
    )
    # Linked to Profile; set to NULL when deleted[cite: 2]
    organizer = models.ForeignKey(
        Profile,
        on_delete=models.SET_NULL,
        null=True
    )
    event_image = models.ImageField(upload_to='events/', blank=True, null=True)
    description = models.TextField()
    location = models.CharField(max_length=255)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    event_capacity = models.PositiveIntegerField()
    status = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES,
        default='Available'
    )
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        # Sorted by created date, descending order[cite: 2]
        ordering = ['-created_on']

    def __str__(self):
        return self.title


class EventSignup(models.Model):
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE
    )
    # Set when registrant is a logged-in user[cite: 2]
    user_registrant = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    # Set when registrant is not logged in[cite: 2]
    new_registrant = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        registrant = self.user_registrant or self.new_registrant
        return f"{registrant} - {self.event.title}"