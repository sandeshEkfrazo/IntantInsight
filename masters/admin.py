from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(Service)
class Service(admin.ModelAdmin):
    list_display = ['id','name', 'create_timestamp', 'last_update_timestamp']

@admin.register(ProjectType)
class ProjectType(admin.ModelAdmin):
    list_display = ['id', 'name', 'create_timestamp', 'last_update_timestamp']

@admin.register(Category)
class Category(admin.ModelAdmin):
    list_display = ['id', 'name', 'detail']

@admin.register(Currency)
class Currency(admin.ModelAdmin):
    list_display = ['id', 'name', 'symbol']

@admin.register(Quotas)
class Quotas(admin.ModelAdmin):
    list_display = ['id', 'name']

@admin.register(Country)
class Country(admin.ModelAdmin):
    list_display = ['id', 'name', 'symbol']

@admin.register(B2B)
class B2B(admin.ModelAdmin):
    list_display = ['id', 'name']

@admin.register(B2C)
class B2C(admin.ModelAdmin):
    list_display = ['id', 'name']

@admin.register(SurveyTopic)
class SurveyTopic(admin.ModelAdmin):
    list_display = ['id', 'name']

@admin.register(SurveyStatus)
class SurveyStatus(admin.ModelAdmin):
    list_display = ['id', 'name' ,'message' ,'company']

@admin.register(CampaignType)
class CompanyType(admin.ModelAdmin):
    list_display = ['id', 'name']
    
@admin.register(CommissionModel)
class CommissionModel(admin.ModelAdmin):
    list_display = ['id', 'name']

