from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

# router = DefaultRouter()
# router.register('user-offer', UserOffers, basename='useroffers')

urlpatterns = [
    # path('', include(router.urls))
    path('user-offer', UserOffers.as_view()),
    path('user-points', UserPoints.as_view()),
    path('user-redeme-points', RedemeVocher.as_view()),
    path('get-user-redemtion-detail/user-id/<int:user_id>', RedemeVocher.as_view()),
    path('panelist-forgot-password', PanelistForgotPasswordAPI.as_view()),
    path('reset-panelist-password', ResetPanelistPassword.as_view())
]