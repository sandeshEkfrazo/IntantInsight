from django.conf.urls import url
from django.db import models
from django.db.models.base import Model
from django_celery_beat.models import ClockedSchedule, PeriodicTask
from masters.models import *
import uuid
from account.models import *
from prescreener.models import *

class Project(models.Model):
    name                = models.CharField(max_length=150, blank=True, null=True)
    incentive_cost      = models.CharField(max_length=100, null=True, blank=True)
    cpi                 = models.CharField(max_length=200, null=True, blank=True)
    total_complete      = models.CharField(max_length=100, null=True, blank=True)
    remove_targeted_audience = models.CharField(max_length=100, null=True, blank=True)
    bidding_manager                = models.CharField(max_length=100, null=True, blank=True)
    study_type          = models.CharField(max_length=100, null=True, blank=True)
    length_of_interview = models.IntegerField(blank=True, null=True)
    status              =models.CharField(max_length=150, default='Draft')
    market_type         = models.CharField(max_length=150, null=True, blank=True)
    country             = models.JSONField(null=True, blank=True)
    bidding_id                 = models.CharField(max_length=150, blank=True, null=True)
    device_compatibility       = models.CharField(max_length=150, null=True, blank=True)	
    enable_geo_location        = models.BooleanField(default=False)
    requires_webcam	           = models.BooleanField(default=False)	
    collects_pii	           = models.BooleanField(default=False)		
    estimated_incidence_rate_percentage = models.CharField(max_length=150, null=True, blank=True)
    project_manager                       = models.CharField(max_length=100, null=True, blank=True)
    company             = models.ForeignKey(Company, on_delete=models.CASCADE, blank=True, null=True)
    client              = models.ForeignKey(Client, on_delete=models.CASCADE, blank=True, null=True)
    project_type        = models.ForeignKey(ProjectType,on_delete=models.CASCADE, blank=True, null=True)
    service             = models.ForeignKey(Service,on_delete=models.CASCADE, blank=True, null=True)
    currency       = models.ForeignKey(Currency,on_delete=models.CASCADE, blank=True, null=True)
    # quotas        = models.ForeignKey(Quotas,on_delete=models.CASCADE, blank=True, null=True)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    quotas_details = models.JSONField(null=True, blank=True)
    created_date = models.DateField(blank=True, null=True, editable=True)
    updated_dateTime = models.DateTimeField(null=True, blank=True, editable=True)
    copy = models.CharField(max_length=150, blank=True, null=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True, related_name="project_created_by")
    updated_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True, related_name="project_updated_by")
    
    is_deleted = models.BooleanField(default=False, null=True, blank=True)

    # enable_rd = models.BooleanField(default=False, null=True, blank=True)

    def __str__(self):
        return self.name

class ProjectScheduler(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True)
    clock = models.ForeignKey(ClockedSchedule, on_delete=models.CASCADE, null=True, blank=True)
    task = models.ForeignKey(PeriodicTask, on_delete=models.CASCADE, null=True, blank=True)

class RequirementForm(models.Model):    
    survey_topic = models.ForeignKey(SurveyTopic, on_delete=models.CASCADE, null=True, blank=True)
    subject_line = models.CharField(max_length=150, blank=True, null=True)
    actual_survey_length = models.CharField(max_length=150, blank=True, null=True)
    target_audience_type = models.CharField(max_length=150, null=True, blank=True)
    b2b_b2c_dropdowns = models.CharField(max_length=150, blank=True, null=True)
    target_audience_textbox =  models.CharField(max_length=150, blank=True, null=True)
    de_dupe_needed = models.BooleanField(default=False, null=True)
    # start_date = models.DateTimeField(null=True, blank=True)
    # end_date = models.DateTimeField(null=True, blank=True)
    live_survey_link = models.URLField(null=True, blank=True)
    test_survey_link = models.URLField(null=True, blank=True)
    masked_url_with_unique_id = models.TextField(null=True, blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='requirement_form',null=True, blank=True)
    de_dupe_project = models.ForeignKey(Project, on_delete=models.CASCADE,null=True, blank=True)

class Template(models.Model):
    name               = models.CharField(max_length=100, blank=True, null=True)
    design             = models.CharField(max_length=5000, blank=True, null=True) 
    company            = models.CharField(max_length=100, null=True, blank=True)
    type               = models.CharField(max_length=100, blank=True, null=True)
    

class ProjectRedirects(models.Model):
    link          = models.TextField()
    template      = models.ForeignKey(Template, on_delete=models.CASCADE, null=True, blank=True)
    survey_status = models.ForeignKey(SurveyStatus, on_delete=models.CASCADE, null=True, blank=True)
    project       = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='project_redirect', null=True, blank=True)

class TrackPanel(models.Model):
    user = models.CharField(max_length=100, null=True, blank=True)
    project_redirect = models.ForeignKey(ProjectRedirects, on_delete=models.CASCADE, null=True, blank=True)     

class Supplier(models.Model):
    Supplier_Name = models.CharField(max_length=150, blank=True, null=True)
    Contact_Person = models.CharField(max_length=150, blank=True, null=True)
    Methodology = models.CharField(max_length=150, blank=True, null=True)
    Email = models.EmailField(verbose_name="email",max_length=150, blank=True, null=True)
    Billing_Email = models.CharField(max_length=150, blank=True, null=True)
    Website = models.CharField(max_length=150, blank=True, null=True)
    Phone =models.CharField(max_length=150, blank=True, null=True)
    Status = models.CharField(max_length=150, blank=True, null=True)
    Total_Projects = models.CharField(max_length=150, blank=True, null=True)
    Total_Completes = models.CharField(max_length=150, blank=True, null=True)
    Avg_Vendor_Rating = models.CharField(max_length=150, blank=True, null=True)
    Payment_Term = models.CharField(max_length=150, blank=True, null=True)
    MSA = models.CharField(max_length=150, blank=True, null=True)
    NDA = models.CharField(max_length=150, blank=True, null=True)
    GDPR = models.CharField(max_length=150, blank=True, null=True)
    Vendor_Remarks = models.CharField(max_length=150, blank=True, null=True)
    Avg_CPC = models.CharField(max_length=150, blank=True, null=True)
    Audience =  models.CharField(max_length=150, blank=True, null=True)
    is_for_project =models.BooleanField(default=False)

    def __str__(self):
        return self.Supplier_Name

class EmailTemplate(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    subject = models.CharField(max_length=100, null=True, blank=True)
    media_type = models.CharField(max_length=100, null=True, blank=True)
    sender = models.CharField(max_length=100, null=True, blank=True)
    category = models.CharField(max_length=100, null=True, blank=True)
    event_type = models.CharField(max_length=100, null=True, blank=True)
    portal_name = models.CharField(max_length=100, null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    placeholder = models.CharField(max_length=100, null=True, blank=True)

class Theme(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    language = models.CharField(max_length=100, null=True, blank=True)
    portal_name = models.CharField(max_length=100, null=True, blank=True)
    upload_css = models.FileField(max_length=100, null=True, blank=True)
    upload_image = models.ImageField(max_length=100, null=True, blank=True)
    default_theme = models.BooleanField(default=False)

class ExternalSampling(models.Model):
    complete_link = models.URLField(null=True, blank=True)
    quotas_full_link = models.URLField(null=True, blank=True)
    terminated_link = models.URLField(null=True, blank=True)
    client_quality_fail_link = models.URLField(null=True, blank=True)
    panel_duplicate_link = models.URLField(null=True, blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True, related_name="project")
    supplier =  models.ForeignKey(Supplier, on_delete=models.CASCADE, null=True, blank=True)

class SupplierMaskedLink(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, null=True, blank=True, related_name='suppliers')
    masked_link = models.URLField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True)

class IESamplingStatus(models.Model):
    user_id = models.TextField(null=True, blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    status = models.CharField(max_length=100)
    IE = models.CharField(max_length=100, null=True, blank=True)
    campaign_id = models.IntegerField(null=True, blank=True)
    survey_start_time = models.TextField(null=True, blank=True)
    survey_end_time = models.TextField(null=True, blank=True)
    browser = models.TextField(null=True, blank=True)
    os = models.TextField(null=True, blank=True)
    ip_adress = models.TextField(null=True, blank=True)
    user_country = models.TextField(null=True, blank=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, null=True, blank=True)
    client_id = models.TextField(null=True, blank=True)
    vendor_tid = models.TextField(null=True, blank=True)

class ProjectDashboard(models.Model):
    response_rate = models.CharField(max_length=100, null=True, blank=True)
    total_spent =  models.IntegerField(null=True, blank=True)
    completion_rate = models.CharField(max_length=100, null=True, blank=True)
    total_invite_sent = models.IntegerField(null=True, blank=True)
    snc = models.IntegerField(null=True, blank=True)
    total_clicks = models.IntegerField(null=True, blank=True)
    complete = models.IntegerField(null=True, blank=True)
    quotas_full = models.IntegerField(null=True, blank=True)
    terminated = models.IntegerField(null=True, blank=True)
    quality_fail = models.IntegerField(null=True, blank=True)
    panel_duplicate = models.IntegerField(null=True, blank=True)
    ie = models.CharField(max_length=100, null=True, blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True)
    supplier_name = models.TextField(null=True, blank=True)
    supplier_id = models.ForeignKey(Supplier, on_delete=models.CASCADE, null=True, blank=True)

    

