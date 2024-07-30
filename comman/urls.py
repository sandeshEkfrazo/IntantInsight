from django.urls import path
from .views import *

urlpatterns = [
    path('dashboard', DashboardAPi.as_view()),
    path('translate', Translatelanguage.as_view()),
    path('global-dashboard', GlobalDashboard.as_view()),
    # path("send-otp-mobile", SendOTP.as_view()),
    path('add-end-pages', AddEndPagesTemplate.as_view()),
    path('add-end-pages/<int:page_id>', AddEndPagesTemplate.as_view()),
    path('upload-supplier-xls', UploadSupplierXLS.as_view()),

    path('employee-ratings/', EmployeeRatigsView.as_view()),
    path('employee-ratings/<int:user_id>/', EmployeeRatigsView.as_view()),

    path('ip-token', IpTokenApi.as_view()),
]