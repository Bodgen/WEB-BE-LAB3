from __future__ import absolute_import, unicode_literals
from celery import shared_task
from django.core.mail import send_mail

from djangoProject1 import settings
from blog.models import EmailLog


@shared_task(bind=True)
def send_mail_func(self, subject, message, recipient_list):
    print("message")
    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        recipient_list,
    )
    EmailLog.objects.create(user_email=recipient_list, subject=subject)
    return None