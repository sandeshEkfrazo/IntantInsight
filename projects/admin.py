from django.contrib import admin
from projects.models import *

# @admin.register(Service)
# class Service(admin.ModelAdmin):
#     list_display = ['id','name', 'create_timestamp', 'last_update_timestamp']

# @admin.register(ProjectType)
# class ProjectType(admin.ModelAdmin):
#     list_display = ['id', 'name', 'create_timestamp', 'last_update_timestamp']

# @admin.register(Category)
# class Category(admin.ModelAdmin):
#     list_display = ['id', 'name', 'detail']

# @admin.register(Currency)
# class Currency(admin.ModelAdmin):
#     list_display = ['id', 'name', 'symbol']

# @admin.register(Quotas)
# class Quotas(admin.ModelAdmin):
#     list_display = ['id', 'name']

# @admin.register(B2B)
# class B2B(admin.ModelAdmin):
#     list_display = ['id', 'name']

# @admin.register(B2C)
# class B2C(admin.ModelAdmin):
#     list_display = ['id', 'name']

# @admin.register(SurveyTopic)
# class SurveyTopic(admin.ModelAdmin):
#     list_display = ['id', 'name']

# @admin.register(Country)
# class Country(admin.ModelAdmin):
#     list_display = ['id', 'name', 'symbol']

@admin.register(ProjectDashboard)
class ProjectDashboard(admin.ModelAdmin):
    list_display = ['total_clicks','response_rate', 'total_spent','completion_rate','total_invite_sent','snc','complete','quotas_full','terminated','quality_fail','panel_duplicate', 'ie', 'project', 'supplier_name', 'supplier_id']

@admin.register(Project)
class Project(admin.ModelAdmin):
    list_display = ['id', 'name' ,'incentive_cost' ,'cpi' ,'total_complete' ,'remove_targeted_audience' ,'bidding_manager' ,'study_type' ,'length_of_interview' ,'status' ,'market_type' ,'country' ,'bidding_id' ,'device_compatibility' ,'enable_geo_location'  ,'requires_webcam' ,'collects_pii' ,'estimated_incidence_rate_percentage' ,'project_manager' ,'company' ,'client' ,'project_type' ,'service' ,'currency', 'start_date', 'end_date', 'quotas_details', 'created_date','updated_dateTime', 'copy', 'created_by', 'updated_by', 'is_deleted']



@admin.register(RequirementForm)
class RequirementForm(admin.ModelAdmin):
    list_display = ['id', 'survey_topic' ,'subject_line' ,'actual_survey_length' ,'target_audience_type' ,'b2b_b2c_dropdowns' ,'target_audience_textbox' ,'de_dupe_needed' ,'project' ,'live_survey_link' ,'test_survey_link', 'masked_url_with_unique_id', 'de_dupe_project']

@admin.register(Template)
class Template(admin.ModelAdmin):
    list_display = ['id', 'name', 'design', 'company', 'type']

# @admin.register(SurveyStatus)
# class SurveyStatus(admin.ModelAdmin):
#     list_display = ['id', 'name' ,'message' ,'company']

@admin.register(ExternalSampling)
class ExternalSampling(admin.ModelAdmin):
    list_display = ['id', 'complete_link' ,'quotas_full_link' ,'terminated_link' ,'client_quality_fail_link' ,'panel_duplicate_link','project', 'supplier']

@admin.register(ProjectRedirects)
class ProjectRedirects(admin.ModelAdmin):
    list_display = ['id', 'link' ,'template' ,'survey_status' ,'project']

@admin.register(TrackPanel)
class TrackPanel(admin.ModelAdmin):
    list_display = ['id', 'user' ,'project_redirect']

@admin.register(Client)
class Client(admin.ModelAdmin):
    list_display = ['id', 'clientname' ,'address' ,'email' ,'website' ,'company' ,'create_timestamp' ,'last_update_timestamp']

@admin.register(Supplier)
class Supplier(admin.ModelAdmin):
    list_display = ['id', 'Supplier_Name' ,'Contact_Person' ,'Methodology' ,'Email' ,'Billing_Email' ,'Website' ,'Phone' ,'Status' ,'Total_Projects' ,'Total_Completes' ,'Avg_Vendor_Rating' ,'Payment_Term' ,'MSA' ,'NDA' ,'GDPR' ,'Vendor_Remarks' ,'Avg_CPC' ,'Audience', 'is_for_project']

@admin.register(EmailTemplate)
class EmailTemplate(admin.ModelAdmin):
    list_display = ['id','name' ,'subject' ,'media_type' ,'sender' ,'category' ,'event_type' ,'portal_name' ,'content' ,'placeholder']

@admin.register(Theme)
class Theme(admin.ModelAdmin):
    list_display = ['id','name' ,'language' ,'portal_name' ,'upload_css' ,'upload_image' ,'default_theme']

@admin.register(ProjectScheduler)
class ProjectScheduler(admin.ModelAdmin):
    list_display = ['id','project' ,'clock', 'task']

@admin.register(SupplierMaskedLink)
class SupplierMaskedLink(admin.ModelAdmin):
    list_display = ['id', 'supplier' ,'masked_link', 'project']


@admin.register(IESamplingStatus)
class IESamplingStatus(admin.ModelAdmin):
    list_display = ['id', 'user_id','project' ,'project_id', 'status', 'IE', 'campaign_id', 'survey_start_time', 'survey_end_time', 'browser', 'os', 'ip_adress', 'user_country', 'supplier', 'client_id', 'vendor_tid']

