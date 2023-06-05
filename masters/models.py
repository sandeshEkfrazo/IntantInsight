from django.db import models

class Service(models.Model):
    name                   = models.CharField(max_length=150, blank=True, null=True)
    create_timestamp       = models.DateTimeField(auto_now_add=True,verbose_name="Create_TimeStamp",blank=True,null=True)
    last_update_timestamp  = models.DateTimeField(auto_now_add=True,verbose_name="last_update_timestamp",blank=True,null=True)
    company = models.CharField(max_length=100, null=True, blank=True)

class ProjectType(models.Model):
    name                   = models.CharField(max_length=150, blank=True, null=True)
    create_timestamp       = models.DateTimeField(auto_now_add=True,verbose_name="Create_TimeStamp",blank=True,null=True)
    last_update_timestamp  = models.DateTimeField(auto_now_add=True,verbose_name="Create_TimeStamp",blank=True,null=True)
    company = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    detail = models.CharField(max_length=100, null=True, blank=True)

class Currency(models.Model):
    name      = models.CharField(max_length=150, blank=True, null=True)
    symbol    = models.CharField(max_length=150, blank=True, null=True)    

class Quotas(models.Model):
    name     = models.CharField(max_length=150, blank=True, null=True)

    def __str__(self):
        return self.name

class Country(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    symbol = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name

class B2B(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)

class B2C(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)

class SurveyTopic(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name

class Client(models.Model):
    clientname             = models.CharField(max_length=150, blank=True, null=True)
    address                = models.CharField(max_length=150, blank=True, null=True)
    email                  = models.EmailField(verbose_name="email",max_length=150, blank=True, null=True)
    website                = models.CharField(max_length=150, blank=True, null=True)
    company                = models.CharField(max_length=100, null=True, blank=True)
    create_timestamp       = models.CharField(max_length=100, null=True, blank=True)
    last_update_timestamp  = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.clientname

class SurveyStatus(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    message = models.CharField(max_length=100, null=True, blank=True)
    company = models.CharField(max_length=100, null=True, blank=True)

class CampaignType(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name

class CommissionModel(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)

class PeCampaignType(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name

class PeCategory(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name


