from django.contrib import admin
from comman.models import *
from comman.models import *
from comman.models import *

# Register your models here.
@admin.register(PeCampaignCampaignPrescreenerQuestionLibraryPage)
class PeCampaignQuestionLibraryPage(admin.ModelAdmin):
    list_display = ['id', 'pe_campaign', 'campaign', 'prescreener', 'question_library', 'page']

@admin.register(Page)
class LogicType(admin.ModelAdmin):
    list_display = ['id', 'name', 'pe_campaign', 'campaign', 'prescreener', 'end_template_page']

@admin.register(CustomizeThankyouandTerminatePage)
class CustomizeThankyouandTerminatePage(admin.ModelAdmin):
    list_display = ['id', 'name','inline_html_code']

@admin.register(PageRoutingLogic)
class PageRoutingLogic(admin.ModelAdmin):
    list_display = ['id', 'name', 'page', 'logic', 'targeted_page', 'targeted_page_name', 'pe_campaign', 'campaign_id', 'prescreener']

@admin.register(PageMaskingLogic)
class Logics(admin.ModelAdmin):
    list_display = ['id', 'name' ,'page' ,'question_id' ,'questio_choice_id' ,'target_question_id' ,'hide_answer_id']

@admin.register(PagePipingLogic)
class Logics(admin.ModelAdmin):
    list_display = ['id', 'name' ,'page' ,'question_id' ,'next_question_id', 'next_question_text']

@admin.register(DashboardData)
class DashboardData(admin.ModelAdmin):
    list_display = ['id', 'total_clicks' ,'total_invite_sent' ,'total_completes' ,'response_rate' ,'completion_rate' ,'snc' ,'completed' ,'quotas_full' ,'terminated' ,'quality_fail' ,'panel_duplicate', 'total_soi', 'total_doi', 'total_conversion_rate', 'total_spent']

@admin.register(QuestionsLinkedPage)
class QuestionsLinkedPage(admin.ModelAdmin):
    list_display = ['id', 'question_library' ,'page']

@admin.register(EnableRd)
class EnableRd(admin.ModelAdmin):
    list_display = ['project', 'enable_rd', 'risk']