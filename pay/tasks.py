import string
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from celery import shared_task
import django.template.loader as loader
import logging


logger = logging.getLogger(__name__)



@shared_task
def send_mail_task(email_context=None):
    
    # TODO : make sending email based on Django Template System.
    if email_context is not None:
        logger.debug("email_context available. Running send_mail now")
        template_name = email_context['template_name']
        rendered = loader.render_to_string(template_name, {'email': email_context})
        html_message = loader.get_template(template_name=template_name).render({'email': email_context})
        send_mail(
            email_context['title'],
            rendered,
            'root@local_pay.com',
            [email_context['recepient_email']],
            html_message=html_message
        )
    else:
        logger.debug("email_context or template_name not available")
