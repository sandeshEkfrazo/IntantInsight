from django.db import models
from projects.models import *
from prescreener.models import *
from prescreener.models import *
from panelbuilding.models import *
from masters.models import *

# class PeCampaignType(models.Model):
#     name = models.CharField(max_length=100, null=True, blank=True)

#     def __str__(self):
#         return self.name

# class PeCategory(models.Model):
#     name = models.CharField(max_length=100, null=True, blank=True)

#     def __str__(self):
#         return self.name

class PeCampaign(models.Model):
    market = models.CharField(max_length=100, null=True, blank=True)
    campaign_name = models.CharField(max_length=100, null=True, blank=True)
    points = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(max_length=100, null=True, blank=True)
    profile_type = models.CharField(max_length=100, null=True, blank=True)
    external_profile_link = models.URLField(null=True, blank=True)
    internal_campaign_generated_link = models.URLField(null=True, blank=True)
    pe_category = models.ForeignKey(PeCategory, on_delete=models.CASCADE, null=True, blank=True, related_name="pe_category")
    pe_campaign_type = models.ForeignKey(PeCampaignType, on_delete=models.CASCADE, null=True, blank=True, related_name="pe_campaign_type")
    created_date = models.DateField(blank=True, null=True, editable=True, auto_now_add=True)
    updated_dateTime = models.DateTimeField(null=True, blank=True, editable=True, auto_now_add=True)

class Redemption(models.Model):
    market = models.CharField(max_length=100 ,null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    threshold_value = models.CharField(max_length=100, null=True, blank=True)
    description = models.CharField(max_length=100, null=True, blank=True)
    image = models.FileField(null=True, blank=True, upload_to='redemption_images/')
    is_instant_redemption = models.BooleanField(default=False)
    is_edenred_redemption = models.BooleanField(default=False)

class MarketWiseRedemption(models.Model):
    redemption = models.ForeignKey(Redemption, on_delete=models.CASCADE, null=True, blank=True)
    market = models.ForeignKey(Country, on_delete=models.CASCADE, null=True, blank=True)
    
# upload redemption and dowload from here
class PanelistIncentive(models.Model):
    redemption_id = models.CharField(max_length=100, null=True, blank=True)
    user_survey_id = models.CharField(max_length=100, null=True, blank=True)
    date_of_redemption = models.CharField(max_length=100, null=True, blank=True)
    timestamp_date = models.CharField(max_length=100, null=True, blank=True)
    redemption_value = models.CharField(max_length=100, null=True, blank=True)
    redemption_status = models.CharField(max_length=100, null=True, blank=True)
    ps_catelog_id = models.CharField(max_length=100, null=True, blank=True)
    redeem_choice = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    source = models.CharField(max_length=100, null=True, blank=True)
    membership_status = models.CharField(max_length=100, null=True, blank=True)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    house_number = models.CharField(max_length=100, null=True, blank=True)
    street = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    postal_code = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    mobile_number = models.CharField(max_length=100, null=True, blank=True)
    earned_points = models.CharField(max_length=100, null=True, blank=True)
    spent_points = models.CharField(max_length=100, null=True, blank=True)
    points = models.CharField(max_length=100, null=True, blank=True)
    voucher_code = models.CharField(max_length=100, null=True, blank=True)
    pin  = models.CharField(max_length=100, null=True, blank=True)
    amount = models.CharField(max_length=100, null=True, blank=True)
    expiry_date = models.CharField(max_length=100, null=True, blank=True)
    paypal_id = models.CharField(max_length=100, null=True, blank=True)
    paytm_id = models.CharField(max_length=100, null=True, blank=True)
    redemption_source = models.CharField(max_length=100, null=True, blank=True)
