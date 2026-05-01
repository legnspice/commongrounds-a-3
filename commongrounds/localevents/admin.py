from django.contrib import admin
from .models import Event, EventSignup

admin.site.register(Event)
admin.site.register(EventSignup)