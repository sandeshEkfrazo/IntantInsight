from django.db import models
from panelbuilding.models import *
from panelengagement.models import *

# Create your models here.
class UserSurveyPoints(models.Model):
    user_survey = models.ForeignKey(UserSurvey, on_delete=models.CASCADE, null=True, blank=True)
    points_earned = models.IntegerField(null=True, blank=True)
    points_spent = models.IntegerField(null=True, blank=True)
    available_points = models.IntegerField(null=True, blank=True)

class UserSurveyRewards(models.Model):
    user_survey = models.ForeignKey(UserSurvey, on_delete=models.CASCADE, null=True, blank=True)
    earned_reward = models.ForeignKey(Redemption, on_delete=models.CASCADE, null=True, blank=True)

class UserSurveyOffers(models.Model):
    survey_name = models.TextField(null=True, blank=True)
    user_survey = models.ForeignKey(UserSurvey, on_delete=models.CASCADE, null=True, blank=True)
    offer_link = models.TextField(null=True, blank=True)
    points_for_survey = models.IntegerField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    is_attened = models.BooleanField(null=True, default=False, blank=True)
    attened_date_time = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=200, null=True, blank=True)
    survey_type = models.CharField(max_length=100, null=True, blank=True)
