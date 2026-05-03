from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import Profile, Role
from django.contrib import admin

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False

class RoleAdmin(admin.ModelAdmin):
    model = Role

class UserAdmin(BaseUserAdmin):
    inlines = [ProfileInline]

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Role, RoleAdmin)