from django.contrib import admin
from .models import *

@admin.register(Campaign)
class Campaign(admin.ModelAdmin):
    list_display = ['id','market_type' ,'campaign_name' ,'lead_required' ,'start_date' ,'length_of_interview' ,'is_quality_follow_up' ,'description' ,'is_relevantld_check' ,'cpa' ,'end_data' ,'recruitment_type' ,'campaign_link' , 'surveyTemplate_link','token' ,'status' ,'company_id' ,'campaign_type' ,'commision_model', 'live_survey_link_for_custom_panel_builidng', 'background_color', 'camapign_image', 'camapign_logo', 'campaign_title', 'text_color', 'created_by', 'updated_by', 'is_deleted', 'p_created_date_time', 'p_updated_date_time']

@admin.register(SupplierCampaignLink)
class SupplierCampaignLink(admin.ModelAdmin):
    list_display = ['id', 'supplier', 'campaign', 'campaign_supplier_link']

@admin.register(PixcelCode)
class PixcelCode(admin.ModelAdmin):
    list_display=['id','pixel_code_screen' ,'s2s_postback_pixel_code' ,'google_pixel_code' ,'facebook_pixel_code', 'campaign']

@admin.register(GeneratedPixcelCodeForCustomPanelBuilding)
class GeneratedPixcelCodeForCustomPanelBuilding(admin.ModelAdmin):
    list_display=['id','pixel_code_screen' ,'s2s_postback_pixel_code' ,'google_pixel_code' ,'facebook_pixel_code', 'campaign']

# @admin.register(CommissionModel)
# class CommissionModel(admin.ModelAdmin):
#     list_display = ['id', 'name']

@admin.register(Vendor)
class Vendor(admin.ModelAdmin):
    list_display = ['name' ,'market' ,'cpa' ,'cpi' ,'cpc' ,'cps' ,'cpl' ,'compaign']

@admin.register(PrescreenerSurvey)
class PrescreenerSurvey(admin.ModelAdmin):
    list_display = ['id', 'panelist_id', 'prescreener', 'question_id', 'option_id']

@admin.register(CampaignSurvey)
class CampaignSurvey(admin.ModelAdmin):
    list_display = ['id', 'panelist_id', 'campaign_id']

@admin.register(PeCampaignSurvey)
class PeCampaignSurvey(admin.ModelAdmin):
    list_display = ['id', 'panelist_id', 'pecampaign']

@admin.register(TransactionIds)
class TransactionIds(admin.ModelAdmin):
    list_display = ['id', 'transaction_id', 'supplier_id', 'campaign_id']

@admin.register(UserQuery)
class UserQuery(admin.ModelAdmin):
    list_display = ['id', 'panelist_id', 'panelist_email', 'subject', 'query', 'reply_data', 'is_solved']

@admin.register(CampaignDashboard)
class CampaignDashboard(admin.ModelAdmin):
    list_display = ['id', 'total_clicks', 'total_soi', 'total_doi', 'total_conversion_rate', 'total_spent', 'total_response_rate', 'total_completion_rate', 'campaign', 'supplier', 'total_invite_sent']

# @admin.register(CampaignQuestionLibrary)
# class CampaignQuestionLibrary(admin.ModelAdmin):
#     list_display = ['id', 'campaign', 'question_library']

@admin.register(UserClicks)
class UserClicks(admin.ModelAdmin):
    list_display = ['id', 'panelist_id' ,'project_id', 'campaign_id', 'is_clicked']

@admin.register(VerifiedUserClicks)
class VerifiedUserClicks(admin.ModelAdmin):
    list_display = ['id', 'panelist_id' , 'campaign_id', 'is_clicked']


