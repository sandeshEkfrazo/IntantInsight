from django.db import models
from prescreener.models import *
from masters.models import *
from projects.models import *
from panelengagement.models import *

# class CampaignType(models.Model):
#     name = models.CharField(max_length=100, null=True, blank=True)

# class CommissionModel(models.Model):
#     name = models.CharField(max_length=100, null=True, blank=True)

class Campaign(models.Model):
    market_type = models.ForeignKey(Country, on_delete=models.CASCADE,null=True, blank=True)
    campaign_name = models.CharField(max_length=100, null=True, blank=True)
    lead_required = models.CharField(max_length=100, null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    length_of_interview = models.CharField(max_length=100, null=True, blank=True)
    is_quality_follow_up = models.BooleanField(default=False)
    description = models.CharField(max_length=100, null=True, blank=True)
    is_relevantld_check = models.BooleanField(default=False)
    cpa = models.CharField(max_length=100, null=True, blank=True)
    end_data = models.DateField(null=True, blank=True)
    recruitment_type = models.CharField(max_length=100, null=True, blank=True)
    campaign_link = models.URLField(null=True, blank=True)
    surveyTemplate_link = models.URLField(null=True, blank=True)
    token = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(max_length=100, null=True, blank=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)
    campaign_type = models.ForeignKey(CampaignType, on_delete=models.CASCADE, null=True, blank=True)
    commision_model = models.ForeignKey(CommissionModel, on_delete=models.CASCADE, null=True, blank=True)
    ############ styling #########

    live_survey_link_for_custom_panel_builidng = models.TextField(null=True, blank=True)
    background_color = models.TextField(null=True, blank=True)
    camapign_image = models.FileField(null=True, blank=True, upload_to='camapainImages/')
    camapign_logo = models.FileField(null=True, blank=True, upload_to='camapainImages/')
    text_color = models.TextField(null=True, blank=True)
    campaign_title = models.TextField(null=True, blank=True)

    ########## end-styling #######
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True, related_name="created_by")
    updated_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True, related_name="updated_by")


    is_deleted = models.BooleanField(default=False, null=True, blank=True)

    def __str__(self):
        return self.campaign_name

class SupplierCampaignLink(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    campaign_supplier_link = models.TextField()

class GeneratedPixcelCodeForCustomPanelBuilding(models.Model):
    pixel_code_screen = models.CharField(max_length=500, null=True, blank=True)
    s2s_postback_pixel_code = models.CharField(max_length=500, null=True, blank=True)
    google_pixel_code = models.CharField(max_length=500, null=True, blank=True)
    facebook_pixel_code = models.CharField(max_length=500, null=True, blank=True)
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, null=True, blank=True)


class PixcelCode(models.Model):
    pixel_code_screen = models.CharField(max_length=500, null=True, blank=True)
    s2s_postback_pixel_code = models.CharField(max_length=500, null=True, blank=True)
    google_pixel_code = models.CharField(max_length=500, null=True, blank=True)
    facebook_pixel_code = models.CharField(max_length=500, null=True, blank=True)
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, null=True, blank=True)
    
class Vendor(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    market = models.CharField(max_length=100, null=True, blank=True)
    cpa = models.CharField(max_length=100, null=True, blank=True)
    cpi = models.CharField(max_length=100, null=True, blank=True)
    cpc = models.CharField(max_length=100, null=True, blank=True)
    cps = models.CharField(max_length=100, null=True, blank=True)
    cpl = models.CharField(max_length=100, null=True, blank=True)
    compaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name
    
# class CampaignQuestionLibrary(models.Model):
#     campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name="campaign", null=True, blank=True)
#     question_library = models.ForeignKey(QuestionLibrary, on_delete=models.CASCADE, related_name="questionlibrary", null=True, blank=True)

class PrescreenerSurvey(models.Model):
    panelist_id = models.CharField(max_length=100, null=True, blank=True)
    question_id = models.CharField(max_length=100, null=True, blank=True)
    option_id = models.CharField(max_length=100, null=True, blank=True)
    prescreener = models.ForeignKey(Prescreener, on_delete=models.CASCADE, null=True, blank=True)

class PeCampaignSurvey(models.Model):
    panelist_id = models.CharField(max_length=100, null=True, blank=True)
    # question_id = models.CharField(max_length=100, null=True, blank=True)
    # option_id = models.CharField(max_length=100, null=True, blank=True)
    pecampaign = models.ForeignKey(PeCampaign, on_delete=models.CASCADE, null=True, blank=True)

class CampaignSurvey(models.Model):
    panelist_id = models.CharField(max_length=100, null=True, blank=True)
    # question_id = models.CharField(max_length=100, null=True, blank=True)
    # option_id = models.CharField(max_length=100, null=True, blank=True)
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, null=True, blank=True)

class TransactionIds(models.Model):
    transaction_id = models.TextField(null=True, blank=True)
    supplier_id = models.CharField(max_length=100,null=True, blank=True)
    campaign_id = models.CharField(max_length=100, null=True, blank=True)

class CampaignDashboard(models.Model):
    total_clicks = models.IntegerField(null=True, blank=True)
    total_soi = models.IntegerField(null=True, blank=True)
    total_doi = models.IntegerField(null=True, blank=True)
    total_conversion_rate = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=5)
    total_spent = models.IntegerField(null=True, blank=True)
    total_response_rate = models.FloatField(null=True, blank=True)
    total_completion_rate = models.IntegerField(null=True, blank=True)
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, null=True, blank=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, null=True, blank=True)
    total_invite_sent = models.IntegerField(null=True, blank=True)

class UserQuery(models.Model):
    panelist_id = models.CharField(max_length=100, null=True, blank=True)
    panelist_email = models.EmailField(max_length=200)
    subject = models.CharField(max_length=100, null=True,blank=True)
    query = models.TextField(null=True, blank=True)
    reply_data = models.TextField(null=True, blank=True)
    is_solved = models.BooleanField(default=False)

class UserClicks(models.Model):
    panelist_id = models.ForeignKey(UserSurvey, on_delete=models.CASCADE, null=True, blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True)
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, null=True, blank=True)
    is_clicked = models.BooleanField(null=True, blank=True)

class VerifiedUserClicks(models.Model):
    panelist_id = models.ForeignKey(UserSurvey, on_delete=models.CASCADE, null=True, blank=True)
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, null=True, blank=True)
    is_clicked = models.BooleanField(null=True, blank=True)

