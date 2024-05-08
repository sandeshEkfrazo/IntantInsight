from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(UserSurveyPoints)
class UserSurveyPoints(admin.ModelAdmin):
    list_display = ['id', 'user_survey', 'points_earned', 'points_spent', 'available_points']

@admin.register(UserSurveyRewards)
class UserSurveyRewards(admin.ModelAdmin):
    list_display = ['id', 'user_survey', 'earned_reward']


@admin.register(UserSurveyOffers)
class UserSurveyOffers(admin.ModelAdmin):
    list_display = ['id','survey_name', 'points_for_survey', 'user_survey', 'offer_link', 'is_attened', 'end_date', 'attened_date_time', 'status', 'survey_type']
