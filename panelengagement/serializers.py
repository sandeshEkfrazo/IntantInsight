from django.db.models import fields
from comman.models import *
from rest_framework import serializers

# class PeCampaignTypeSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = PeCampaignType
#         fields = '__all__'

# class PeCategorySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = PeCategory
#         fields = '__all__'

class PageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = '__all__'

class PageRoutingLogicSerializer(serializers.ModelSerializer):
    class Meta:
        model = PageRoutingLogic
        fields = '__all__'

class PageMaskingLogicSerializer(serializers.ModelSerializer):
    class Meta:
        model = PageMaskingLogic
        fields = '__all__'

class PagePipingLogicSerializer(serializers.ModelSerializer):
    class Meta:
        model = PagePipingLogic
        fields = '__all__'

class PeCampaignSerializer(serializers.ModelSerializer):
    pe_category = serializers.StringRelatedField(many=False, read_only=True)
    created_by = serializers.StringRelatedField(many=False, read_only=True)
    updated_by = serializers.StringRelatedField(many=False, read_only=True)
    pe_campaign_type = serializers.StringRelatedField(many=False, read_only=True)
    market = serializers.StringRelatedField(many=False, read_only=True)
    class Meta:
        model = PeCampaign
        fields = ['id', 'market', 'market_id' ,'campaign_name' ,'points' ,'status' ,'pe_category' ,'pe_campaign_type' ,'profile_type' ,'external_profile_link', 'created_by', 'updated_by', 'is_deleted']

class RedemptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Redemption
        fields = '__all__'

