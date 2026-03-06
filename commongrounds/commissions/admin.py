from django.contrib import admin

from .models import Commission, CommissionType


class CommissionAdmin(admin.ModelAdmin):
    model = Commission


class CommissionTypeAdmin(admin.ModelAdmin):
    model = CommissionType


admin.site.register(Commission, CommissionAdmin)
admin.site.register(CommissionType, CommissionTypeAdmin)
