from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import RedirectView
from rest_framework.authtoken.views import obtain_auth_token
from django.contrib.staticfiles.views import serve
from django.conf.urls import url
from account import backends_
from projects.views import *
from panelbuilding.views import *
from panelengagement.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('panelbuilding.urls')),
    path('api/', include('projects.urls')),
    path('api/', include('account.urls')),
    path('api/', include('prescreener.urls')),
    path('api/', include('sampling.urls')),
    path('api/', include('panelengagement.urls')),
    path('api/', include('surveyQuestionare.urls')),
    path('api/', include('masters.urls')),
    path('api/', include('comman.urls')),
    path('api/', include('usersurvey.urls')),
    
    path('pid=<int:pid>&mid=<str:mid>&uid=<str:uid>', MaskedLinkClick.as_view()), # pid = project id & uid = user/panelist id 	
    path('pid=<int:pid>&sid=<str:sid>&mid=<str:mid>&vid=<str:vid>', VendorMaskedLinkClick.as_view()),
    path('c/cid=<str:cid>&sid=<str:sid>&tid=<str:tid>', CamapignLinkWithTransactionID.as_view()), #cid = camapign_id & sid=supplier_id & tid=transaction/tracking id
    # url(r'^campaign/$', CamapignLinkWithTransactionID.as_view()),
    path('campaign-login/cid=<str:cid>&sid=<str:sid>&panelist_id=<str:panelist_id>&tid=<str:tid>', CamapaignLoginRedirectView.as_view()),

    path('pcid=<str:pcid>&uid=<str:uid>', pecampaignMaskedLink.as_view()),
 
    path('error-page', backends_.authorization_required, name='error-page'),
        # url(r'^$', serve,kwargs={'path': 'index.html'}),    
        url(r'^(?!/?static/)(?!/?media/)(?P<path>.*\..*)$',
        RedirectView.as_view(url='/static/%(path)s', permanent=False)),
    # path('api/robas/',include('account.urls'), name='app'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)+[url(r'^.*', serve,kwargs={'path': 'index.html'})]
