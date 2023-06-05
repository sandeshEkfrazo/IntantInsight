from celery import shared_task
from django.core.mail import EmailMessage
from prescreener.models import *
from bs4 import BeautifulSoup
from projects.models import *

from hashids import Hashids
from usersurvey.models import *


@shared_task(bind=True)
def ScheduleSendout(self, *args, **kwargs):   
    hashids = Hashids(min_length=8)

    # project_obj = kwargs['project_obj']
    # sample_obj = kwargs['sample_obj']

    email_body = kwargs['email_body']

    soup = BeautifulSoup(email_body, 'html')
    clss = soup.find("a", class_="targetPage")
    clss_link_val = soup.find("a", class_="link_value")
    # project_obj = kwargs['project_obj']
    # sample_obj = kwargs['sample_obj']link_value")

    for i in kwargs['emails']:
        panelist_id = UserSurvey.objects.get(email=i).id
        encoded_user_id = hashids.encode(int(panelist_id))

        clss['href'] = RequirementForm.objects.filter(project_id=kwargs['project_id']).last().masked_url_with_unique_id+"&uid="+str(encoded_user_id)
        clss_link_val.append(RequirementForm.objects.filter(project_id=kwargs['project_id']).last().masked_url_with_unique_id+"&uid=<#user_id#>")

        em_body = soup.prettify()

        email = EmailMessage(kwargs['subject'], em_body, from_email=kwargs['sender'], to=[i])
        email.content_subtype = "html"
        email.send(fail_silently=False)

        if UserSurveyOffers.objects.filter(user_survey_id=panelist_id, offer_link=RequirementForm.objects.filter(project_id=kwargs['project_id']).last().masked_url_with_unique_id+"&uid="+str(encoded_user_id)).exists():
            pass
        else:
            UserSurveyOffers.objects.create(user_survey_id=panelist_id, offer_link=RequirementForm.objects.filter(project_id=kwargs['project_id']).last().masked_url_with_unique_id+"&uid="+str(encoded_user_id), survey_name=kwargs['project_name'], points_for_survey=kwargs['bonus_points'], end_date=kwargs['project_end_date'])

        if ProjectDashboard.objects.filter(project_id=kwargs['project_id'], ie='internal').exists():
            total_invite_sent = ProjectDashboard.objects.get(project_id=kwargs['project_id'], ie='internal').total_invite_sent
            ProjectDashboard.objects.filter(project_id=kwargs['project_id'], ie='internal').update(total_invite_sent=int(total_invite_sent)+len(kwargs['emails']), total_clicks=0)
        else:
            ProjectDashboard.objects.create(project_id=kwargs['project_id'], total_invite_sent=len(kwargs['emails']), total_clicks=0, ie='internal')

    return "Mail Sent Successfully"


@shared_task(bind=True)
def deleteCampaign(self, *args, **kwargs):
    print("kwargs['campaign_id']==>", kwargs['campaign_id'])
    Campaign.objects.filter(id=kwargs['campaign_id']).delete()

    return "campaign deleted successfully"



    