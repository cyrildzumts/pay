from celery import shared_task
from voucher.models import Voucher
from django.contrib.auth.models import User
from voucher import voucher_service
from itertools import islice
import logging, uuid


logger = logging.getLogger(__name__)

@shared_task
def generate_voucher(context={}):
    logger.info("starting voucher generation task")
    voucher_service.generate_vouchers(context)
    logger.info("finished voucher generation task")
