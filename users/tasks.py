from django.core.mail import send_mail
from Setup.celery import app

@app.task()
def send_email(subject, message, recipient_list):
    send_mail(
             subject,
             message,
             "abdurakhimovy@gmail.com",
             recipient_list
         )