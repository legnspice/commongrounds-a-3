from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import Profile, Role
from django.contrib import admin

class RoleInLine(admin.StackedInline):
    model = Role
    can_delete = False

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False

class UserAdmin(BaseUserAdmin):
    inlines = [ProfileInline, RoleInLine ]

admin.site.unregister(User)
admin.site.register(User, UserAdmin)