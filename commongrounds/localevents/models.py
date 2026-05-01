from django.db import models
# The official link to your groupmate's Accounts app!
from accounts.models import Profile 

class Event(models.Model):
    STATUS_CHOICES = (
        ('upcoming', 'Upcoming'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
    )

    name = models.CharField(max_length=200)
    organizer = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='organized_events')
    location = models.CharField(max_length=200)
    date = models.DateTimeField()
    description = models.TextField()
    capacity = models.PositiveIntegerField(default=50)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='upcoming')

    def __str__(self):
        return self.name

class EventSignup(models.Model):
    user_registrant = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='event_signups')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='signups')
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        # This ensures a user can only sign up for a specific event once
        unique_together = ('user_registrant', 'event')

    def __str__(self):
        return f"{self.user_registrant} signed up for {self.event.name}"