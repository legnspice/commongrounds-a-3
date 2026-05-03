from django.db import models

from accounts.models import Profile


class EventType(models.Model):
    """Model representing the category of an event."""

    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name


class Event(models.Model):
    """Model representing a community event."""

    STATUS_CHOICES = (
        ('Available', 'Available'),
        ('Full', 'Full'),
        ('Done', 'Done'),
        ('Cancelled', 'Cancelled'),
    )

    title = models.CharField(max_length=255)
    category = models.ForeignKey(
        EventType, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='events'
    )
    organizer = models.ManyToManyField(Profile, related_name='organized_events')
    location = models.CharField(max_length=200)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    description = models.TextField()
    event_capacity = models.PositiveIntegerField(default=50)
    event_image = models.ImageField(upload_to='events/', null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Available')
    
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title


class EventSignup(models.Model):
    """Model representing a user or guest registration for an event."""

    user_registrant = models.ForeignKey(
        Profile, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True, 
        related_name='event_signups'
    )
    new_registrant = models.CharField(max_length=200, null=True, blank=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='signups')
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Prevents logged-in users from signing up for the same event twice
        constraints = [
            models.UniqueConstraint(
                fields=['user_registrant', 'event'], 
                name='unique_user_event_signup'
            )
        ]

    def __str__(self):
        registrant = self.user_registrant if self.user_registrant else self.new_registrant
        return f"{registrant} signed up for {self.event.title}"
    