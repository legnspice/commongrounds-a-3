from django.db import models

class CommissionType(models.Model):
    name=models.CharField(max_length=255)
    description=models.TextField()

class Commission(models.Model):
    title=models.CharField(max_length=255)
    description=models.TextField()
    people_required=models.IntegerField()
    created_on=models.DateTimeField(auto_now_add=True)
    updated_on=models.DateTimeField(auto_now=True)
    commission_type = models.ForeignKey(CommissionType, on_delete=models.CASCADE)
