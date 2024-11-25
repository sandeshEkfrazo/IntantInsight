from os import name
from django.urls import path, include
from panelbuilding.views import *
from panelbuilding import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('campaign', CampaignView, basename='campaign')


urlpatterns = [
   path('delete-or-restore-campaign', DeleteOrRestoreCampaign.as_view()),
   
   path('campaign-type', CampaignTypeView.as_view(), name="company-type"),
   path('campaign-type/<int:pk>', CampaignTypeView.as_view(), name="company-type"),
   path('commision-model', CommissionModelView.as_view(), name="commision-model"),
   path('commision-model/<int:pk>', CommissionModelView.as_view(), name="commision-model"),
   # path('campaign', CampaignView.as_view(), name="campaign"),
   path('pixel-codes', pixelCode.as_view(), name="pixelCode"),
   path('pixel-codes/<int:cid>', pixelCode.as_view(), name="pixelCode"),
   path('camapaign-status', CampaignStatus.as_view()),
   path('camapaign-status/<int:pk>', CampaignStatus.as_view()),
   # path('campaign/<int:pk>', CampaignDetailView.as_view(), name="campaign-detail"),
   path('vendors', VendorView.as_view(), name="vendor"),
   path('vendors/<int:pk>', VendorDetailView.as_view(), name="vendor-detail"),
   path('campaign/submit', CampaignSubmitApi.as_view()),
   path('campaign/verify', CampaignVerify.as_view(), name="campaign_verify"),
   path('camapign-login', UserSurveyLogin.as_view(), name="camapign-login"),
   path('supplier-camapign_link', CamapignSupllierLink.as_view(), name='camapign_supplier_link'),  #update camapign link to particular supplier

   path('verify-email', views.verifyemailTemplate, name='verify_email'),

   path('oprators', Operators.as_view(), name='operators'),
   path('select-criteria', SelectCriteria.as_view(), name='select-criteria'),
   path('build-criteria', BuildCriteria.as_view(), name="build_criteria"),
   path('build-criteria-for-reports', BuildCriteriaForReports.as_view(), name="build_criteria"),
   path("draw-sample", DrawSamples.as_view(), name=""),
   path('robas.com/campaign', GetLandingPageURL.as_view(), name="get_landing_pageURL"),
   path('email-communique', EMailCommunique.as_view(), name="email_communique"),
   path('send-outs', SendOut.as_view(), name="send_out"),
   path('communque-send-outs', CommunqueSendOut.as_view(), name="Communique send_out"),
   path('promotional-send-outs', PromotionalSendOut.as_view(), name="promotional_send_outs"),
   path('panel-statistic-report', Reports.as_view(), name='panel_satistic_repport'),
   path('panelist-summary', PanelistSummary.as_view(), name='panelist_summary'),
   path('select-questions', SelectQuestionLibrary.as_view(), name="select-questions"),
   path('criteria-question', SelectQuestionForBuildCriteria.as_view(), name="criteria-question"),
   path('campaign-page', CampaignPageApiView.as_view(), name="page"),
   path('logic-questions/campaign-id/<int:p_id>/page/<int:pk>', CampaignRoutingLogicQuestions.as_view(), name='logic-questions2'),
   # path("prescreener", PrescreenerTemplate, name="prescrennerTemplate"),
   path('panelist-prescreener-answer', PanelistPrescreenerAnswer.as_view()),
   path('panelist-pe-campaign-answer', PanelistPeCampaignAnswer.as_view()),
   path('surveyTemplate', SurveyTemplateApiView.as_view()),
   path('panelist-campaign-answer', PanelistCampaignAnswer.as_view()),
   path('campaigndashboard_data/<int:c_id>', getCampaignDashBoard.as_view()),

   path('panelist-data', PanlistDetailsAPI.as_view()),
   path('panelist-data/<int:panelist_id>', PanlistDetailsAPI.as_view()),
   path('users-query', PanlistQuery.as_view()),
   path('upload-custom-sample', UploadCustomSample.as_view()),
   
   path('get-language-for-survey', getLanguageForSurvey.as_view()),
   path('campaign-date-filter', CamapignDateFilter.as_view()),

   path('get-all-panelist_email', getAllPanelistEmail.as_view()),

   path('export-or-clone-campaign', ExportOrCloneCampaign.as_view()),

   path('check-link', CheckLink.as_view()),

   path('', include(router.urls))
]