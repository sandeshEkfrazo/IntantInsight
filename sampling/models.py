from django.db import models
from projects.models import *

# Create your models here.
class Sampling(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    complete = models.CharField(max_length=100, null=True, blank=True)
    bonus_points = models.CharField(max_length=100, null=True, blank=True)
    is_custom_panel = models.BooleanField(default=False, null=True, blank=True)
    quotas        = models.ForeignKey(Quotas,on_delete=models.CASCADE, blank=True, null=True)
    # is_exclusive = models.BooleanField(default=False)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='sampling',null=True, blank=True)

class Person(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField(blank=True)
    birth_date = models.DateField()
    location = models.CharField(max_length=100, blank=True)