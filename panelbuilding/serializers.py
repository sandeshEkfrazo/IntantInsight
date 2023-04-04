from django.db import models
from django.db.models import fields
from rest_framework import serializers
from panelbuilding.models import *

class CampaignTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CampaignType
        fields = '__all__'

class CommissionModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommissionModel
        fields = '__all__'

class CampaignSerializer(serializers.ModelSerializer):
    campaign_type = serializers.StringRelatedField()
    company = serializers.StringRelatedField()
    market_type = serializers.StringRelatedField()
    created_by = serializers.StringRelatedField()
    updated_by = serializers.StringRelatedField()
    class Meta:
        model = Campaign
        fields = ['id','market_type', 'market_type_id' ,'campaign_name' ,'lead_required' ,'start_date' ,'length_of_interview' ,'is_quality_follow_up' ,'description' ,'is_relevantld_check' ,'cpa' ,'end_data' ,'recruitment_type' ,'campaign_link' , 'surveyTemplate_link','token' ,'status' ,'company_id', 'company' ,'campaign_type' ,'commision_model', 'live_survey_link_for_custom_panel_builidng', 'created_by', 'updated_by',
        'live_survey_link_for_custom_panel_builidng','background_color','camapign_image', 'camapign_logo', 'text_color', 'campaign_title', 'is_deleted']

class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = '__all__'

class SupplierCampaignLinkSerializer(serializers.ModelSerializer):
    supplier = serializers.StringRelatedField()
    campaign =  serializers.StringRelatedField()
    class Meta:
        model = SupplierCampaignLink
        fields = ['id', 'supplier', 'campaign', 'campaign_supplier_link', 'supplier_id', 'campaign_id']

class CampaignDashboardSerializer(serializers.ModelSerializer):
    supplier = serializers.StringRelatedField()
    campaign =  serializers.StringRelatedField()
    class Meta:
        model = CampaignDashboard
        fields = ['id','supplier_id','total_clicks', 'total_soi', 'total_doi', 'total_conversion_rate', 'total_spent', 'total_response_rate', 'total_completion_rate', 'campaign', 'supplier', 'campaign_id', 'supplier_id', 'total_invite_sent']
    