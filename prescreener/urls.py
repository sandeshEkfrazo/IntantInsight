from unicodedata import name
from django.urls import path
from prescreener.views import *

urlpatterns = [
    path('all-question-library', AllQuestionlibrary.as_view()),


    path('question-type', QuestionTypes.as_view(), name="question-type"),
    path('question-type/<int:pk>', QuestionTypes.as_view(), name="question-type"),
    path('question-categories', QuestionCatagories.as_view(), name="question-categories"),
    path('question-categories/<int:pk>', QuestionCatagories.as_view(), name="question-categories"),
    path('questions', Questionlibrary.as_view(), name="questions"),
    path('questions/<int:pk>', Questionlibrary.as_view(), name="single-questions"),
    path('questions/language', QuestionLibraryWithLanguagesAPI.as_view(), name="questions_language"),
    path('prescreener', PrescreenerApiView.as_view(), name="Prescreener"),
    path('prescreener/<int:pk>', PrescreenerDetailView.as_view(), name="PrescreenerDetail"),
    path('selected-category', SelectCategoryForCrieteria.as_view(), name="selected-category"),
    # path('prescreener-question-library', PrescreenerQuestionLibraryApi.as_view(), name="Prescreener"),
    path('prescreener-page', PrescreenerPageApiView.as_view(), name="page"),
    path("import-questions", ImportQuestionAndChoices.as_view(), name="import-questions"),
    path('logic-questions/prescreener-id/<int:p_id>/page/<int:pk>', PrescreenerLogicQuestions.as_view(), name='prscreener-questions2'),
    path("read-campaign-file", readCampaignExcelData.as_view(), name="readCampaignFile"),

    path('delete-question/<int:question_id>', DeleteQuestionFromQ_Lib.as_view())
]