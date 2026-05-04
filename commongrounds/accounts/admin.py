from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Profile, Role

# 1. Register Role so you can add the predefined roles to the database
admin.site.register(Role)

# 2. Keep the ProfileInline exactly as is
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False

# 3. Attach it to the User
class UserAdmin(BaseUserAdmin):
    inlines = [ProfileInline] 

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
