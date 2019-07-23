import string
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from celery import shared_task


@shared_task
def send_mail_task(to=None, msg=None):
    # TODO : make sending email based on Django Template System.
    send_mail(
        get_random_string(12),
        get_random_string(75),
        'root@local_pay.com',
        ['pay_user@local_pay.com']
    )
