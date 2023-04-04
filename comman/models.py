from django.db import models
from prescreener.models import *
from panelbuilding.models import *
from panelengagement.models import *
from projects.models import *

# Create your models here.
class CustomizeThankyouandTerminatePage(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    inline_html_code = models.TextField() 

class Page(models.Model):
    name= models.CharField(max_length=100, null=True, blank=True)
    pe_campaign = models.ForeignKey(PeCampaign,on_delete=models.CASCADE, null=True, blank=True)
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, null=True, blank=True)
    prescreener = models.ForeignKey(Prescreener,on_delete=models.CASCADE, null=True, blank=True)
    end_template_page = models.ForeignKey(CustomizeThankyouandTerminatePage, on_delete=models.CASCADE, null=True, blank=True)

class PageRoutingLogic(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    page = models.ForeignKey(Page,on_delete=models.CASCADE, null=True, blank=True)
    logic = models.JSONField(null=True, blank=True)
    targeted_page = models.CharField(max_length=100, null=True, blank=True)
    targeted_page_name = models.CharField(max_length=100, null=True, blank=True)

class PageMaskingLogic(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    page = models.ForeignKey(Page,on_delete=models.CASCADE, null=True, blank=True)
    question_id = models.IntegerField(null=True, blank=True)
    questio_choice_id = models.IntegerField(null=True, blank=True)  #answer_id
    target_question_id = models.IntegerField(null=True, blank=True)
    hide_answer_id = models.IntegerField(null=True, blank=True)
    

class PagePipingLogic(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    page = models.ForeignKey(Page,on_delete=models.CASCADE, null=True, blank=True)
    question_id = models.IntegerField(null=True, blank=True)
    next_question_id = models.IntegerField(null=True, blank=True)
    next_question_text = models.TextField(null=True, blank=True)

class PeCampaignCampaignPrescreenerQuestionLibraryPage(models.Model):
    pe_campaign = models.ForeignKey(PeCampaign, on_delete=models.CASCADE, related_name="pecampaign", null=True, blank=True)
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, null=True, blank=True)
    prescreener = models.ForeignKey(Prescreener, on_delete=models.CASCADE, null=True, blank=True)
    question_library = models.ForeignKey(QuestionLibrary, on_delete=models.CASCADE, related_name="pe_questionlibrary", null=True, blank=True)
    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name="pe_questionlibrary", null=True, blank=True)

class QuestionsLinkedPage(models.Model):
    question_library = models.ForeignKey(QuestionLibrary, on_delete=models.CASCADE, null=True, blank=True)
    page = models.ForeignKey(Page, on_delete=models.CASCADE, null=True, blank=True)

class DashboardData(models.Model):
    total_clicks = models.IntegerField(null=True, blank=True, default=1)
    total_invite_sent = models.IntegerField(null=True, blank=True, default=1)
    total_completes = models.IntegerField(null=True, blank=True, default=1)
    response_rate = models.FloatField(null=True, blank=True, default=1)
    completion_rate = models.IntegerField(null=True, blank=True, default=1)
    snc = models.IntegerField(null=True, blank=True, default=1)  # snc = sent but not completed
    completed = models.IntegerField(null=True, blank=True, default=1)
    quotas_full = models.IntegerField(null=True, blank=True, default=1)
    terminated = models.IntegerField(null=True, blank=True, default=1)
    quality_fail = models.IntegerField(null=True, blank=True, default=1)
    panel_duplicate = models.IntegerField(null=True, blank=True, default=1)
    total_soi = models.IntegerField(null=True, blank=True, default=1)
    total_doi = models.IntegerField(null=True, blank=True, default=1)
    total_conversion_rate = models.FloatField(null=True, blank=True, default=1)
    total_spent = models.FloatField(null=True, blank=True, default=1)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True)

class EnableRd(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True)
    enable_rd = models.BooleanField(default=False, null=True, blank=True)
    risk =  models.JSONField(null=True, blank=True)