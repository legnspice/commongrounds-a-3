from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Profile, Role

# --- COMMENTED OUT TO FIX admin.E202 ERROR ---
# class RoleInLine(admin.StackedInline):
#     model = Role
#     can_delete = False

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False

class UserAdmin(BaseUserAdmin):
    # Removed RoleInLine from here to unblock the system
    inlines = [ProfileInline] 

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
