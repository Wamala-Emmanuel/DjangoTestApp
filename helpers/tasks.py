from celery import shared_task
from django.core.mail import send_mail
from sending_documents_system import settings
import smtplib

# @shared_task(bind=True)
# def send_notification_mail(self, target_mail, message):
#     mail_subject = "Welcome on Board!"
#     send_mail(
#         subject = mail_subject,
#         message=message,
#         from_email=settings.EMAIL_HOST_USER,
#         recipient_list=[target_mail],
#         fail_silently=False,
#         )
#     return "Done"

@shared_task(bind=True)
def send_notification_mail(self, target_mail, message):
    sender = "otimtonyjeff@gmail.com"
    receiver = "otimtonyjeff@gmail.com"

    subject = 'welcome to GFG world'
    message = f'Hi, thank you for registering in geeksforgeeks.'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [receiver, ]
    send_mail( subject, message, email_from, recipient_list)
    
    return "Done"
