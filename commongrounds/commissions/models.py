from django.db import models
from django.urls import reverse

class CommissionType(models.Model):
    name=models.CharField(max_length=255)
    description=models.TextField()

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('commissions_type_name', args=[str(self.name)])


class Commission(models.Model):
    title=models.CharField(max_length=255)
    description=models.TextField()
    people_required=models.IntegerField()
    created_on=models.DateTimeField(auto_now_add=True)
    updated_on=models.DateTimeField(auto_now=True)
    commission_type = models.ForeignKey(CommissionType, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('commissions_name', args=[str(self.title)])
    
