
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from accounts.models import Account
from core.tasks import send_mail_task
from pay import settings
import logging


logger = logging.getLogger(__name__)

@receiver(post_save, sender=User)
def send_welcome_mail(sender, instance, created, **kwargs):
    
    if created:
        logger.debug("sending welcome mail ...")
        logger.debug("new user created, sending welcome mail ...")
        email_context = {
            'template_name': settings.DJANGO_WELCOME_EMAIL_TEMPLATE,
            'title': 'Bienvenu chez PAY',
            'recipient_email': instance.email,
            'context':{
                'SITE_NAME': settings.SITE_NAME,
                'SITE_HOST': settings.SITE_HOST,
                'FULL_NAME': instance.get_full_name()
            }
        }
        send_mail_task.apply_async(
            args=[email_context],
            queue=settings.CELERY_OUTGOING_MAIL_QUEUE,
            routing_key=settings.CELERY_OUTGOING_MAIL_ROUTING_KEY
        )


@receiver(post_save, sender=Account)
def send_validation_mail(sender, instance, created, **kwargs):
    
    if created:
        logger.debug("sending validation mail ...")
        logger.debug("new user created, sending validation mail ...")
        if not settings.SITE_HOST:
            logger.warning("SITE_HOST environment vairable is missing")
            
        email_context = {
            'template_name': settings.DJANGO_VALIDATION_EMAIL_TEMPLATE,
            'title': 'Validation de votre adresse mail',
            'recipient_email': instance.user.email,
            'context':{
                'SITE_NAME': settings.SITE_NAME,
                'SITE_HOST': settings.SITE_HOST,
                'FULL_NAME': instance.user.get_full_name(),
                'validation_url' : (settings.SITE_HOST or "") + instance.get_validation_url()
            }
        }
        send_mail_task.apply_async(
            args=[email_context],
            queue=settings.CELERY_OUTGOING_MAIL_QUEUE,
            routing_key=settings.CELERY_OUTGOING_MAIL_ROUTING_KEY
        )