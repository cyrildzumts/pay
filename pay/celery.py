import os
from pay import settings
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pay.settings')
app = Celery(settings.SITE_NAME)
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()