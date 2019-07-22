import os
from kombu import Exchange, Queue
from pay import settings
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pay.settings')
app = Celery(settings.SITE_NAME)
app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.task_queues = (
    Queue('pay-default', Exchange('pay-default'), routing_key='pay-default'),
    Queue('pay-outgoing-mails', Exchange('pay-mail'), routing_key='pay.mail.outgoing'),
    Queue('pay-ident', Exchange('pay-ident'), routing_key='pay.identification'),
)
app.conf.task_default_queue = 'pay-default'
app.conf.task_default_exchange_type = 'direct'
app.conf.task_default_routing_key = 'pay.default'
app.autodiscover_tasks()