from django.db.models import fields
from surveyQuestionare.models import *
from rest_framework import serializers

class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = "__all__"

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Questions
        fields = "__all__"

class ElementSerializer(serializers.ModelSerializer):
    options = OptionSerializer(read_only=False, allow_null=True)
    class Meta:
        model = Element
        fields = ['id', 'name', 'options']

class SurveyGoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = SurveyGoal
        fields = '__all__'

class IndustryTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = IndustryType
        fields = '__all__'

class SurveyCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SurveyCategory
        fields = '__all__'

class SurveySerializer(serializers.ModelSerializer):
    class Meta:
        model = Survey
        fields = '__all__'

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = '__all__'

class QuotasSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuotasSQ
        fields = '__all__'

class AttributesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attributes
        fields = '__all__'
