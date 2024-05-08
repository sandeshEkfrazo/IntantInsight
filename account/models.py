from django.db import models
from django.contrib.auth.models import User

class Company(models.Model):
    name                   = models.CharField(max_length=150, blank=True, null=True)
    website                = models.CharField(max_length=150, blank=True, null=True)
    create_timestamp =   models.DateTimeField(auto_now_add=True,verbose_name="Create_TimeStamp",blank=True,null=True)
    last_update_timestamp =   models.DateTimeField(auto_now_add=True,verbose_name="Last_update_timestamp",blank=True,null=True)

    def __str__(self):
        return self.name

class RoleAccessControl(models.Model):
    role_name = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    create_timestamp = models.DateTimeField(auto_now_add=True,verbose_name="Create_TimeStamp",blank=True,null=True)
    last_update_timestamp =   models.DateTimeField(auto_now_add=True,verbose_name="Last_update_timestamp",blank=True,null=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, blank=True, null=True)

class CustomUser(models.Model):
    username = models.CharField(max_length=100, null=True, blank=True)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    phone_number = models.CharField(max_length=150, blank=True, null=True)
    password = models.CharField(max_length=100)
    isAdmin = models.BooleanField(default=False)
    create_timestamp =   models.DateTimeField(auto_now_add=True,verbose_name="Create_TimeStamp",blank=True,null=True)
    last_update_timestamp =   models.DateTimeField(auto_now_add=True,verbose_name="Last_update_timestamp",blank=True,null=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, blank=True, null=True, related_name="company_detail")
    role = models.ForeignKey(RoleAccessControl, on_delete=models.CASCADE, null=True, blank=True, related_name="role_access")

    def __str__(self):
        return self.first_name

class UserAccess(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    access = models.JSONField(null=True, blank=True)





