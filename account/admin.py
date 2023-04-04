from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(CustomUser)
class CustomUser(admin.ModelAdmin):
    list_display = ['id','username' ,'first_name' ,'last_name' ,'email' ,'phone_number' ,'password' ,'isAdmin' ,'create_timestamp' ,'last_update_timestamp' ,'company' ,'role']

@admin.register(Company)
class Company(admin.ModelAdmin):
    list_display = ['id','name' ,'website' ,'create_timestamp' ,'last_update_timestamp']

@admin.register(RoleAccessControl)
class RoleAccessControl(admin.ModelAdmin):
    list_display = ['id','role_name' ,'create_timestamp' ,'last_update_timestamp' ,'company']

@admin.register(UserAccess)
class UserAccess(admin.ModelAdmin):
    list_display = ['id','user_id' ,'access']

# model_list = [CustomUser, Company, RoleAccessControl, Client, Supplier]
# admin.site.register(model_list)






    


