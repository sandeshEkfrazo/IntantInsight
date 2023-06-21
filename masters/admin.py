from django.contrib import admin
from .models import *
from import_export.admin import ImportExportModelAdmin

# Register your models here.
@admin.register(Service)
class Service(ImportExportModelAdmin):
    list_display = ['id','name', 'create_timestamp', 'last_update_timestamp']

@admin.register(ProjectType)
class ProjectType(ImportExportModelAdmin):
    list_display = ['id', 'name', 'create_timestamp', 'last_update_timestamp']

@admin.register(Category)
class Category(ImportExportModelAdmin):
    list_display = ['id', 'name', 'detail']

@admin.register(Currency)
class Currency(ImportExportModelAdmin):
    list_display = ['id', 'name', 'symbol']

@admin.register(Quotas)
class Quotas(ImportExportModelAdmin):
    list_display = ['id', 'name']

@admin.register(Country)
class Country(ImportExportModelAdmin):
    list_display = ['id', 'name', 'symbol']

@admin.register(B2B)
class B2B(ImportExportModelAdmin):
    list_display = ['id', 'name']

@admin.register(B2C)
class B2C(ImportExportModelAdmin):
    list_display = ['id', 'name']

@admin.register(SurveyTopic)
class SurveyTopic(ImportExportModelAdmin):
    list_display = ['id', 'name']

@admin.register(SurveyStatus)
class SurveyStatus(ImportExportModelAdmin):
    list_display = ['id', 'name' ,'message' ,'company']

@admin.register(CampaignType)
class CompanyType(ImportExportModelAdmin):
    list_display = ['id', 'name']
    
@admin.register(CommissionModel)
class CommissionModel(ImportExportModelAdmin):
    list_display = ['id', 'name']

