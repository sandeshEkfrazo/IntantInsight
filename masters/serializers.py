from .models import *
from django.db.models import fields
from rest_framework import serializers

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'

class ProjectTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectType
        fields = '__all__'

class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = '__all__'

class Categoryserializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class QuotesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quotas
        fields = '__all__'

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'

class B2BSerializer(serializers.ModelSerializer):
    class Meta:
        model = B2B
        fields = '__all__'

class B2CSerializer(serializers.ModelSerializer):
    class Meta:
        model = B2C
        fields = '__all__'

class SurveyTopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = SurveyTopic
        fields = '__all__'

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'

class SurveyStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = SurveyStatus
        fields = '__all__'

class CampaignTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CampaignType
        fields = '__all__'

class CommissionModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommissionModel
        fields = '__all__'

class PeCampaignTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PeCampaignType
        fields = '__all__'

class PeCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PeCategory
        fields = '__all__'
