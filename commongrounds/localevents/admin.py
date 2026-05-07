from django.contrib import admin

from .models import Event, EventSignup, EventType


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'start_time', 'status')
    list_filter = ('status', 'category')
    search_fields = ('title', 'description')


@admin.register(EventType)
class EventTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)


admin.site.register(EventSignup)
