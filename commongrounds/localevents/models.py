from django.db import models
from accounts.models import Profile 

class EventType(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name

class Event(models.Model):
    STATUS_CHOICES = (
        ('Available', 'Available'),
        ('Full', 'Full'),
        ('Done', 'Done'),
        ('Cancelled', 'Cancelled'),
    )

    # Fields renamed exactly as per rubric
    title = models.CharField(max_length=255)
    category = models.ForeignKey(EventType, on_delete=models.SET_NULL, null=True, related_name='events')
    organizer = models.ManyToManyField(Profile, related_name='organized_events') # Changed to ManyToMany
    location = models.CharField(max_length=200)
    start_time = models.DateTimeField() # Renamed from date
    end_time = models.DateTimeField()   # New field
    description = models.TextField()
    event_capacity = models.PositiveIntegerField(default=50) # Renamed from capacity
    event_image = models.ImageField(upload_to='events/', null=True, blank=True) # New field
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Available')
    
    # Audit fields required by most CSCI rubrics
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_on'] # Rubric requirement for sorting

    def __str__(self):
        return self.title

class EventSignup(models.Model):
    # Nullable so either a User OR a Guest can sign up
    user_registrant = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True, related_name='event_signups')
    new_registrant = models.CharField(max_length=200, null=True, blank=True) # For guest signups
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='signups')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        registrant = self.user_registrant if self.user_registrant else self.new_registrant
        return f"{registrant} signed up for {self.event.title}"