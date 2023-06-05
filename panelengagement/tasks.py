from celery import shared_task
from .models import *


@shared_task(bind=True)
def deletePeCampaign(self, *args, **kwargs):
    PeCampaign.objects.filter(id=kwargs['pe_campaign_id']).delete()

    return "pe_campaign deleted successfully"