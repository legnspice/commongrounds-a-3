from django.contrib import admin

from .models import Commission, CommissionType, Job, JobApplication


class CommissionAdmin(admin.ModelAdmin):
    model = Commission


class CommissionTypeAdmin(admin.ModelAdmin):
    model = CommissionType

class JobAdmin(admin.ModelAdmin):
    model = Job

class JobApplicationAdmin(admin.ModelAdmin):
    model = JobApplication



admin.site.register(Commission, CommissionAdmin)
admin.site.register(CommissionType, CommissionTypeAdmin)
admin.site.register(Job, JobAdmin)
admin.site.register(JobApplication, JobApplicationAdmin)
