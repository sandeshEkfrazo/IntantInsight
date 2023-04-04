from django.db.models import base
from django.urls import path, include
from account.views import *
from rest_framework import routers
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.authtoken.views import obtain_auth_token
from . import views
from rest_framework_swagger.views import get_swagger_view
from rest_framework.routers import DefaultRouter
# from panelbuilding.views import *


app_name = 'account'


# router = routers.DefaultRouter()

router = DefaultRouter()
router.register('all-company',CompanyModelViewset),
schema_view = get_swagger_view(title='Api Documentation')

urlpatterns = [
    path('', include(router.urls)),
    path('api_documentation/', schema_view),
    # path('signup/', SignupApi.as_view()),
    # path('login', LoginView.as_view(), name="JWTlogin"),
    # path('login-token', CustomAuthToken.as_view(), name="LOGIN"),
    # path('reset_password/', ForgotPassword.as_view(), name="reset"),
    # path('forgot-password-update/', ForgotPasswordUpdate.as_view()),

    

    

    path('company',CompanyApiView.as_view()),

    # path('custom',CustomapiView.as_view()),

    

    # path('test-excel',TestExcel.as_view()),
    path('project-excel-export',ProjectExcelExport.as_view()),

    

    path('custom-one',CustomApiView.as_view()),
    
    
    

    path('register', UserRegister.as_view(), name="Register"),
    path('login', UserLogin.as_view(), name='login'),
    path('change-password', changePassword.as_view()),
    path('forgot-password', forgotPassword.as_view(), name="forgot-password"), 
    path('reset-password', resetPassword.as_view(), name="resetPassword"),
    path('add-users', AddUsers.as_view(), name="Users"),
    path('users/<int:pk>', UserDetail.as_view(), name="UserDetail"),
    path('roles', RoleAccessControlView.as_view()),
    path('roles/<int:id>', RoleAccessControlView.as_view()),
    

    

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
