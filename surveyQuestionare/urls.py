from django.urls import path
from surveyQuestionare.views import *
from surveyQuestionare import views
from .views import *

app_name = 'surveyQuestionare'

urlpatterns = [
    #@@@@@@@@@@@@  list of all Api's   @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    path('all-elements', ElementListApiView.as_view(), name="all-elements"),
    path('all-options', OptionListApiView.as_view()),
    path('all-questions', QuestionListApiView.as_view()),
    path('all-surveygoal', SureveyGoalListApiView.as_view()),
    path('all-industrytype', IndustryTypeListApiView.as_view()),
    path('all-survey-category', SurveyCategoryListApiView.as_view()),
    path('all-survey', SurveyListApiView.as_view()),
    path('all-document', DocumentListApiView.as_view()),
    path('all-quotas', QuotasListApiView.as_view()),
    path('all-attributes', AttributesListApiView.as_view()),


    #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

    path('surveygoal', SurveyGoalApiView.as_view(), name="SurveyGoal"),
    path('surveygoal/<int:pk>', SurveyGoalApiView.as_view(), name="SurveyGoal"),

    path('industrytype', IndustryTypeApiView.as_view(), name="IndustryType"),
    path('industrytype/<int:pk>', IndustryTypeApiView.as_view(), name="IndustryType"),

    path('surveycategory', SurveyCategoryApiView.as_view(), name="SurveyCategory"),
    path('surveycategory/<int:pk>', SurveyCategoryApiView.as_view(), name="SurveyCategory"),

    path('survey', SurveyApiView.as_view(), name="Survey"),
    path('survey/<int:pk>', SurveyApiView.as_view(), name="Survey"),

    path('document', DocumentApiView.as_view(), name="Document"),
    path('document/<int:pk>', DocumentApiView.as_view(), name="Document"),

    path('quotasSQ', QuotasApiView.as_view(), name="Quotas"),
    path('quotasSQ/<int:pk>', QuotasApiView.as_view(), name="Quotas"),

    path('attributes', AttributesApiView.as_view(), name="Attributes"),
    path('attributes/<int:pk>', AttributesApiView.as_view(), name="Attributes"),

    path('elements', ElementApiView.as_view(), name="element"),
    path('elements/<int:pk>', ElementApiView.as_view(), name="element"),

    path('options', OptionsApiView.as_view(), name="option"),
    path('options/<int:pk>', OptionsApiView.as_view(), name="option"),

    path('survey-questions', SurveyQuestionApiView.as_view(), name="questions"),
    path('survey-questions/<int:pk>', SurveyQuestionApiView.as_view(), name="questions"),


    path('survey_questionare_page', SurveyQuestionarePage.as_view(), name="survey_questionare_page"),
    path('panelist-survey-answer', PanelistPeCampaignAnswer.as_view()),

]