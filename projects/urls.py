from django.urls import path, include
from projects import views
from projects.views import *
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('projects', ProjecttView, basename='ProjecttView')

urlpatterns = [
    path("projectDashboard/<int:pid>", ProjectDashboardView.as_view()),
    path('all-external-sampling', ExternalSamplingListApiView.as_view()),
    # path('all-projects', AllProjectListView.as_view()),
    path('all-email-template', EmailTemplateListApiView.as_view()),
    # path('projects', ProjectListView.as_view()),
    path('project', ProjectQuery.as_view()),
    path('project-export/<int:pk>', ProjectExport.as_view()),
    # path('projects/<int:pk>', ProjectDetailView.as_view(), name='project-detail'),
    path('projects/requirements', RequirementFormList.as_view()),
    path('projects/<int:pk>/requirements', RequirementFormApi.as_view(), name='requirement'),
    path('projects/<int:pro>/requirements/<int:req>', RequirementFormDetailApi.as_view()),
    path('delete-or-restore-project', DeleteOrRestoreProjectStatus.as_view()),
    path('templates', TemplateView.as_view()),
    path('project-redirect', ProjectRedirectView.as_view()),
    path('project-redirect/<int:pk>', ProjectRedirectDetailView.as_view(), name='project-redirect'),
    path('suppliers',SupplierApiView.as_view()),
    path('suppliers/<int:pk>',SupplierUpdateApiView.as_view()),
    path('email-template', EmailTemplateAPI.as_view(), name="email_template"),
    path('email-template/<int:pk>', EmailTemplateAPI.as_view(), name="email_template"),
    path('theme', ThemeAPI.as_view(), name="theme"),
    path('projects/<int:pk>/redirects', RedirectApi.as_view(), name="redirect"),
    path('external-sampling', ExternalSamplingApiView.as_view(), name="external-sampling"),
    path('external-sampling/<int:pk>', ExternalSamplingApiView.as_view(), name="external-sampling"),

    path('supplier-maked-link', SupplierMaskedLinks.as_view()),

    path('select-event-type', SelectEventType.as_view()),
    path('sample-status', SampleStatus.as_view()),
    path('export-project', ExportOrCopyProject.as_view()),
    path('project-date-filter', ProjectDateFilter.as_view()),
    path('remove-user-points', RemoveUserPointsByExcelUploads.as_view()),
    path('export-fraud-ids', ExportDuplicateIDsForProject.as_view()),

    path('sendMail-celery', SendEmailThroughCelelry.as_view()),

    path('get-rd-response-from-client', GetRDResponse.as_view()),

    path('', include(router.urls)),
]
