from django.contrib import admin
from .models import Event, EventSignup, EventType

admin.site.register(Event)
admin.site.register(EventSignup)
admin.site.register(EventType)