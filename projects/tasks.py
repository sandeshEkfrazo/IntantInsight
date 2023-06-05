from celery import shared_task
from django.core.mail import send_mail, EmailMessage
from .models import *
from account.models import *
from django.template.loader import get_template
from django.shortcuts import render
from django.conf import settings
from panelbuilding.models import *

@shared_task(bind=True)
def updateProjectStatusAndSendMail(self, *args, **kwargs):
    print("kwargs==>",kwargs)

    user_obj = CustomUser.objects.get(id=kwargs['created_by_id'])
    project_obj = Project.objects.get(id=kwargs['project_id'])

    html_path = 'projectExpired.html'
    context_data = {'name': user_obj.first_name, 'project_name': project_obj.name}
    email_html_template = get_template(html_path).render(context_data)
    receiver_email = user_obj.email
    email_msg = EmailMessage('Reneval Project', email_html_template, settings.APPLICATION_EMAIL, [receiver_email])

    email_msg.content_subtype='html'
    email_msg.send(fail_silently=False)

    Project.objects.filter(id=kwargs['project_id']).update(status='Closed')

    return "status updated"


@shared_task(bind=True)
def sendMailProject(self):

    print("send mail function executing")
    
    send_mail(
        "Subject here",
        "Here is the message.",
        "donotreplyrobas@gmail.com",
        ["sandesh@ekfrazo.in"],
        fail_silently=False,
    )

    data = {"hello": "hello"}

    return data



@shared_task(bind=True)
def getAllProjects(self):
    allval = Project.objects.all().order_by('-id')
    print("allval==>", allval)
    data = {'data': list(allval)}
    return {"data": data}


@shared_task(bind=True)
def deleteProject(self, *args, **kwargs):
    Project.objects.filter(id=kwargs['project_id']).delete()

    return "project deleted successfully"

