from django.urls import path
from .views import *

urlpatterns = [
    path('service',ServiveApiView.as_view()),
    path('service/<int:pk>',ServiveApiView.as_view()),
    path('projecttype',ProjectTypeApiView.as_view()),
    path('projecttype/<int:pk>',ProjectTypeApiView.as_view()),
    path('currency',CurrencyApiView.as_view()),
    path('currency/<int:pk>',CurrencyApiView.as_view()),
    path('category',CategoryView.as_view()),
    path('category/<int:pk>',CategoryView.as_view()),

    path('quotas',QuotasApiView.as_view()),
    path('quotas/<int:pk>',QuotasApiView.as_view()),
    path('country',CountryApiView.as_view()),
    path('country/<int:pk>',CountryApiView.as_view()),

    path('b2b', B2BApi.as_view()),
    path('b2b/<int:pk>', B2BApi.as_view()),
    path('b2c', B2CApi.as_view()),
    path('b2c/<int:pk>', B2CApi.as_view()),

    path('survey-topic', SurevyTopicApi.as_view()),
    path('survey-topic/<int:pk>', SurevyTopicApi.as_view()),

    path('clients',ClientApiView.as_view()),
    path('clients/<int:pk>', ClientApiView.as_view()),

    path('get-survey-status', getSurveyStatus.as_view()),
    path('survey-status', SurveyStatusView.as_view()),
    path('survey-status/<int:pk>', SurveyStatusView.as_view(), name='survey-status'),


    path('pe-campaign-type', PeCampaignTypeView.as_view()),
    path('pe-campaign-type/<int:pk>', PeCampaignTypeView.as_view()),
    path('pe-category', PeCategoryView.as_view()),
    path('pe-category/<int:pk>', PeCategoryView.as_view()),
]