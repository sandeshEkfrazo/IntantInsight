from apscheduler.schedulers.background import BackgroundScheduler
from time import sleep

scheduler = BackgroundScheduler(timezone="Asia/Kolkata")


def prompt(subject, em_body, sender, i):
    print("Executing Task...")
    email = EmailMessage(subject, em_body, from_email=sender, to=[i])
    email.content_subtype = "html"
    email.send(fail_silently=False)
    

def sheduleTask(datetimeValue, subject, em_body, sender, i):
    print("coming to excute")
    job = scheduler.add_job(prompt, 'date', run_date =datetimeValue, args= [subject, em_body, sender, i])
    print("print job",job)
    scheduler.start()
    scheduler.shutdown(wait=False)
    

    while True:
        sleep(1)
        # scheduler.shutdown()







