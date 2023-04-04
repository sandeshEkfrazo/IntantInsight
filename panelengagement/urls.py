from re import A
from panelengagement.views import *
from django.urls import path
from panelengagement import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('all-pe-campaigns', PeCampaignListApiView.as_view(), name='pe_campaign'),
    path('all-redemption', RedemptionListApiView.as_view(), name='redemption'),
    path('all-page', AllPageApiView.as_view(), name='all_page'),

    # path('pe-campaign-type', PeCampaignTypeView.as_view()),
    # path('pe-campaign-type/<int:pk>', PeCampaignTypeView.as_view()),
    # path('pe-category', PeCategoryView.as_view()),
    # path('pe-category/<int:pk>', PeCategoryView.as_view()),
    path('pe-campaigns', PeCampaignView.as_view()),
    path('pe-campaigns/<int:pk>', PeCampaignView.as_view()),

    path('assign-pe-campaign-to-all', AssingCamapigntoAllPanelist.as_view()),
    path('delete-user-survey-offer', AssingCamapigntoAllPanelist.as_view()),

    path('redemptions', RedemptionView.as_view()),
    path('redemptions/<int:pk>', RedemptionView.as_view()),
    path('upload-redemption', UploadRedemption.as_view()),
    path('download-redemption', DownloadRedemptionList.as_view()),
    path('page', PageApiview.as_view(), name="page"),
    path('create-page', CreatPage.as_view()),
    path('re-arrange-questions', RearrangeQuestionPosition.as_view()),
    path('page/<int:pk>', PageApiview.as_view(), name="page"),
    path('pe-campaign-page', PeCampaignPageApiView.as_view(), name="page"),
    path('routig-logic', PageRoutingLogicApiView.as_view(), name='routig-logic'),
    path('masking-logics', PageMaskingLogicApiView.as_view(), name='masking-logics'),
    path('piping-logics', PagePipingLogicApiView.as_view(), name='piping-logics'),
    path('pe-send-out', EmailSendOut.as_view()),
    path('logic-questions/pe-campaign-id/<int:p_id>/page/<int:pk>', PeCampaignRoutingLogicQuestions.as_view(), name='logic-questions1'),
    path('logic-choice/question-id/<int:pk>/page-id/<int:p_id>', QuestionChoiceForQuestion.as_view(), name='logic-choice'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)