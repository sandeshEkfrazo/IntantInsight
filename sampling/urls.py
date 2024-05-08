from os import name
from django.urls import path, include
from sampling.views import *
from sampling import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('sampling', SamplingAPIView, basename='SamplingView')

urlpatterns = [
    path('', include(router.urls))
#     path('sampling', ListOfSample.as_view()),
#     path('samplings', SamplingAPIView.as_view(), name="Samplings"),
#     path('samplings/<int:pk>', SamplingAPIView.as_view(), name="samplings-singledata"),
#     path('upload-excel', UploadExcel.as_view())
    
]