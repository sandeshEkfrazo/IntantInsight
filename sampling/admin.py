from django.contrib import admin
from sampling.models import *
from import_export.admin import ImportExportModelAdmin
# Register your models here.
@admin.register(Sampling)
class Sampling(admin.ModelAdmin):
    list_display = ['id', 'name' ,'complete' ,'bonus_points'  ,'quotas' ,'is_custom_panel','project']

@admin.register(Person)
class Person(ImportExportModelAdmin):
    list_display = ['id', 'name' ,'email' ,'birth_date' ,'location' ]