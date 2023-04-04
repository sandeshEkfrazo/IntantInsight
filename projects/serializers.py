from django.db.models import fields
from rest_framework import serializers
from projects.models import *
from masters.serializers import *
from sampling.serializers import *
from comman.models import *

class ProjectDashboardSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectDashboard
        fields = '__all__'

class RequirementFormSerializer(serializers.ModelSerializer):
    client_name = ClientSerializer(read_only=True)
    survey_topic = serializers.StringRelatedField()
    class Meta:
        model = RequirementForm
        fields = '__all__'  

class ProjectRedirectsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectRedirects
        fields = '__all__'

class TemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Template
        fields = '__all__'

class TrackPanelSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrackPanel
        fields = '__all__'

class EnableRdSerializer(serializers.ModelSerializer):
    class Meta:
        model = EnableRd
        fields = '__all__'

class ProjectSerializer(serializers.ModelSerializer):
    client = serializers.StringRelatedField()
    quotas = serializers.StringRelatedField()
    company = serializers.StringRelatedField()
    requirement_form = RequirementFormSerializer(read_only=True, many=True)
    sampling = SamplingSerializer(read_only=True, many=True)
    enable_rd = EnableRdSerializer(read_only=True)
    created_by = serializers.StringRelatedField()
    updated_by = serializers.StringRelatedField()
    class Meta:
        model = Project
        fields = '__all__'

class ExternalSamplingSerializer(serializers.ModelSerializer):
    project = serializers.StringRelatedField(many=False, read_only=True)
    class Meta:
        model = ExternalSampling
        fields = ['id', 'complete_link' ,'quotas_full_link' ,'terminated_link' ,'client_quality_fail_link' ,'panel_duplicate_link','project']

class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = '__all__'

class EmailTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailTemplate
        fields = '__all__'
    
class ThemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Theme
        fields = '__all__'

class SupplierMaskedLinkSerializer(serializers.ModelSerializer):
    suppliers = serializers.StringRelatedField(many=False, read_only=True)
    class Meta:
        model = SupplierMaskedLink
        fields = ['supplier', 'masked_link', 'suppliers']