from django.contrib import admin
from prescreener.models import *
from import_export.admin import ImportExportModelAdmin

# Register your models here.
@admin.register(QuestionLibrary)
class QuestionLibrary(ImportExportModelAdmin):
    list_display = ['id','question_id', 'language' ,'question_name' ,'question_text' ,'instruction' ,'question_type' ,'question_category', 'position_value', 'is_base_question']

@admin.register(QuestionLibraryWithLanguages)
class QuestionLibraryWithLanguages(ImportExportModelAdmin):
    list_display = ['id','base_queestion', 'created_question_language']

@admin.register(Prescreener)
class Prescreener(admin.ModelAdmin):
    list_display = ['id','name' ,'link' ,'enable_otp_verification' ,'project', 'generated_link']

@admin.register(QuestionCategory)
class QuestionCategory(ImportExportModelAdmin):
    list_display = ['id','name', 'survey_category_image']

@admin.register(QuestionOperator)
class QuestionOperator(ImportExportModelAdmin):
    list_display = ['id','name']

@admin.register(QuestionType)
class QuestionType(ImportExportModelAdmin):
    list_display = ['id','name']

@admin.register(QuestionTypeOperator)
class QuestionTypeOperator(admin.ModelAdmin):
    list_display = ['id','question_type' ,'question_operator']

@admin.register(QuestionChoice)
class QuestionChoice(admin.ModelAdmin):
    list_display = ['id', 'option_id','name', 'text', 'question_library']

@admin.register(PrescreenerQuestionLibrary)
class PrescreenerQuestionLibrary(admin.ModelAdmin):
    list_display = ['id','prescreener', 'question_library']

@admin.register(UserSurvey)
class UserSurvey(admin.ModelAdmin):
    list_display = ['id','panelist_id','status' ,'first_name' ,'last_name' ,'email', 'password' ,'dob' ,'gender' ,'is_email_verified', 'tid', 'campaign_id', 'supplier_id', 'date_of_joining', 'city', 'state', 'country', 'age', 'profile_image']

@admin.register(Answer)
class Answer(admin.ModelAdmin):
    list_display = ['id','user_survey' ,'answers' ,'question_library', 'prescreener_id', 'campaign_id', 'pe_campaign_id']

@admin.register(ExternalSamplePanelistAnswer)
class ExternalSamplePanelistAnswer(admin.ModelAdmin):
    list_display = ['id','panelist_id' ,'answers' ,'question_library', 'prescreener_id', 'campaign_id', 'pe_campaign_id']

@admin.register(DuplicateorFraudPanelistID)
class DuplicateorFraudPanelistID(admin.ModelAdmin):
    list_display = ['id','panelist_id', 'project_id', 'supplier_id', 'supplier_name', 'status', 'threat_potential', 'threat_potential_score', 'duplicate_score', 'browser', 'os', 'ip_adress', 'user_country', 'survey_start_time', 'survey_end_time', 'client_id', 'county_mismath']

@admin.register(BuildQueryOpearator)
class BuildQueryOpearator(admin.ModelAdmin):
    list_display = ['id','name']

