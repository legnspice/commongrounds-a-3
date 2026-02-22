from django.contrib import admin

from .models import Commission,CommissionType

admin.site.register(Commission)
admin.site.register(CommissionType)