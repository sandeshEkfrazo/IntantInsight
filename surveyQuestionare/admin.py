from django.contrib import admin
from surveyQuestionare.models import *
# Register your models here.
@admin.register(SurveyGoal)
class SurveyGoal(admin.ModelAdmin):
    list_display = ['id', 'name' ,'description' ,'create_timestamp' ,'last_update_timestamp']

@admin.register(IndustryType)
class IndustryType(admin.ModelAdmin):
    list_display = ['id', 'name' ,'description' ,'create_timestamp' ,'last_update_timestamp']

@admin.register(SurveyCategory)
class SurveyCategory(admin.ModelAdmin):
    list_display = ['id', 'name' ,'description' ,'create_timestamp' ,'last_update_timestamp']

@admin.register(Survey)
class Survey(admin.ModelAdmin):
    list_display = ['id', 'name' ,'surveycategory' ,'type_of_responses' ,'survey_format' ,'number_of_responses' ,'estimate_cost' ,'estimated_completion_date' ,'create_timestamp' ,'last_update_timestamp' ,'state' ,'user' ,'live_survey_link' ,'test_survey_link' ,'description' ,'tags' ,'directory' ,'primary_language' ,'surveygoal' ,'industrytype']

@admin.register(Document)
class Document(admin.ModelAdmin):
    list_display = ['id', 'doc_1' ,'doc_2' ,'doc_3' ,'survey']

@admin.register(QuotasSQ)
class Quotas(admin.ModelAdmin):
    list_display = ['id', 'name' ,'survey']

@admin.register(Attributes)
class Attributes(admin.ModelAdmin):
    list_display = ['id', 'name' ,'limit' ,'total' ,'need']

@admin.register(Element)
class Element(admin.ModelAdmin):
    list_display = ['id', 'name']

@admin.register(Option)
class Option(admin.ModelAdmin):
    list_display = ['id', 'name', 'option_type']

@admin.register(ElementOption)
class ElementOption(admin.ModelAdmin):
    list_display = ['id', 'element', 'option']

@admin.register(Questions)
class Questions(admin.ModelAdmin):
    list_display = ['id', 'name' , 'column', 'element' ,'conditions']

@admin.register(QuestionOptions)
class QuestionOptions(admin.ModelAdmin):
    list_display = ['id', 'name', 'question']

@admin.register(SurveyPage)
class SurveyPage(admin.ModelAdmin):
    list_display = ['id', 'name', 'survey']

@admin.register(SurveyPanelQuestion)
class SurveyPanelQuestion(admin.ModelAdmin):
    list_display = ['id', 'survey', 'question', 'survey_page']

@admin.register(SurveyQuestionareSurvey)
class SurveyQuestionareSurvey(admin.ModelAdmin):
    list_display = ['id', 'panelist_id', 'question_id', 'option_id']