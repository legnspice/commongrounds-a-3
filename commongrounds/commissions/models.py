from django.db import models
from django.db.models import Case, Value, When, IntegerField
from accounts.models import Profile 
from django.urls import reverse


class CommissionType(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Commission(models.Model):
    STATUS_CHOICES = [
        ("open", "Open"),
        ("full", "Full"),
        ("completed", "Completed"),       
        ("discontinued", "Discontinued"), 
    ]
    title = models.CharField(max_length=255)
    description = models.TextField()
    people_required = models.PositiveIntegerField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    commission_type = models.ForeignKey(
        CommissionType,
        on_delete=models.SET_NULL,
        related_name="commissions",
        null=True
    )
    maker = models.ForeignKey(
        Profile,
        on_delete = models.CASCADE,
        related_name = "commissions_profile",
        null = True
    )
    status = models.CharField(
        max_length = 20,
        choices = STATUS_CHOICES,
        default = "open"
    )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('commissions:commissiondetail', args=[str(self.pk)])

    class Meta:
        ordering = ['created_on']


class Job(models.Model):
    STATUS_CHOICES = [
        ("open", "Open"),
        ("full", "Full"),
    ]
    commission = models.ForeignKey(
        Commission,
        on_delete=models.CASCADE,
        related_name="jobs"
    )
    role = models.CharField(max_length=255)
    manpower_required = models.PositiveIntegerField()
    status = models.CharField(
        max_length = 20,
        choices = STATUS_CHOICES,
        default = "open"
    )

    def __str__(self):
        return self.role

    class Meta:
        ordering = [
            Case(
                When(status="open", then=Value(0)),
                When(status="full", then=Value(1)),
                output_field=IntegerField()
            ), 
        '-manpower_required',
        'role'
        ]

class JobApplication(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("accepted", "Accepted"),
        ("rejected","Rejected")
    ]
    job = models.ForeignKey(
        Job,
        on_delete = models.CASCADE,
        related_name = "jobapplications"
    )
    applicant = models.ForeignKey(
        Profile,
        on_delete = models.CASCADE,
        related_name = "jobapplications_profile"
    )
    status = models.CharField(
        max_length = 20,
        choices = STATUS_CHOICES,
        default = "pending"
    )
    applied_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = [
            Case(
                When(status="pending", then=Value(0)),
                When(status="accepted", then=Value(1)),
                When(status="rejected", then=Value(2)),
                output_field=IntegerField()
            ), 
            '-applied_on'
        ]
