from celery import shared_task
from time import sleep
from robas import settings

from django.core.mail import send_mail, EmailMessage
from projects.models import*
import time


@shared_task
def sleepy(duration):
    sleep(duration)
    return None


@shared_task
def send_email_task(emails, sender, email_body, subject):
    email = EmailMessage(subject, email_body, from_email=sender, to=['sandesh@ekfrazo.in'])
    email.content_subtype = "html"
    email.send(fail_silently=False)
    return None

@shared_task
def project_task_active(project_id):
    Project.objects.filter(id=project_id).update(status='Active')

@shared_task
def project_task_closed(project_id):
    Project.objects.filter(id=project_id).update(status='Closed')


@shared_task
def simple_task():
    print("started")
    time.sleep(1637594580)
    print("ended")
    # return None