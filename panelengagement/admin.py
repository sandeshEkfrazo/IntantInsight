from django.contrib import admin
from panelengagement.models import *
from import_export.admin import ImportExportModelAdmin

@admin.register(PeCampaignType)
class PeCampaignType(ImportExportModelAdmin):
    list_display = ['id', 'name']

@admin.register(PeCategory)
class PeCategory(ImportExportModelAdmin):
    list_display = ['id', 'name']

@admin.register(PeCampaign)
class PeCampaign(admin.ModelAdmin):
    list_display = ['id', 'market' ,'campaign_name' ,'points' ,'status' ,'pe_category' ,'pe_campaign_type' ,'profile_type' ,'external_profile_link', 'internal_campaign_generated_link', 'created_date','updated_dateTime', 'created_by', 'updated_by', 'is_deleted']

@admin.register(Redemption)
class Redemption(admin.ModelAdmin):
    list_display = ['id', 'market' ,'name' ,'threshold_value' ,'description' ,'image' ,'is_instant_redemption' ,'is_edenred_redemption']

@admin.register(PanelistIncentive)
class PanelistIncentive(admin.ModelAdmin):
    list_display = ['id', 'redemption_id', 'user_survey_id', 'date_of_redemption', 'timestamp_date', 'redemption_value', 'redemption_status' ,'ps_catelog_id', 'redeem_choice' ,'country' ,'source' ,'membership_status' ,'first_name' ,'last_name' ,'house_number' ,'street' ,'city' ,'postal_code' ,'state' ,'mobile_number' ,'earned_points' ,'spent_points' ,'points' ,'voucher_code' ,'pin' ,'amount' ,'expiry_date' ,'paypal_id' ,'paytm_id' ,'redemption_source'] 


@admin.register(MarketWiseRedemption)
class MarketWiseRedemption(admin.ModelAdmin):
    list_display = ['id', 'redemption', 'market']