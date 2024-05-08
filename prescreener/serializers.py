from django.db.models import fields
from rest_framework import serializers
from prescreener.models import *

class QuestionTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionType
        fields = '__all__'

class QuestionCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionCategory
        fields = '__all__'

class QuestionchoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionChoice
        fields = ['id', 'name' ,'text' ,'question_library']
    
class QuestLibrarySerializer(serializers.ModelSerializer):
    question_type = QuestionTypeSerializer(read_only=False, allow_null=True)
    question_category = QuestionCategorySerializer(read_only=False, allow_null=True)
    question_choice = QuestionchoiceSerializer(read_only=False, many=True, allow_null=True)
    class Meta:
        model = QuestionLibrary
        fields = ['id','language' ,'question_name' ,'question_text' ,'instruction' ,'question_type' ,'question_category', 'question_choice']


class UserSurveySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSurvey
        fields = ['id', 'status' ,'first_name' ,'last_name' ,'email' ,'dob' ,'gender' ,'is_email_verified']

class Prescreenerserializer(serializers.ModelSerializer):
    class Meta:
        model = Prescreener
        fields = ['id','name' ,'link' ,'enable_otp_verification' ,'project']

class PrescreenerQuestionLibrarySerializer(serializers.ModelSerializer): 
     
    class Meta:
        model = PrescreenerQuestionLibrary
        fields = ['id', 'prescreener', 'question_library']
        depth=1

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = '__all__'

class QuestionOperatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionOperator
        fields = '__all__'
