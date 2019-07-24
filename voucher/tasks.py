from celery import shared_task
from voucher.models import Voucher

import logging


logger = logging.getLogger(__name__)


@shared_task
def generate_voucher(name='PAY-STANDARD', amount=2500, number=50):
    logger.info("Starting generating %s  %s vouchers card with credit of %s", number, name, amount)

    
    logger.info("Generation of  %s  %s vouchers card with credit of %s done.", number, name, amount)
    
