from celery import shared_task
from voucher.models import Voucher
from voucher import voucher_service
from itertools import islice
import logging


logger = logging.getLogger(__name__)
batch_size = 15

@shared_task
def generate_voucher(name='PAY-STANDARD', amount=2500, number=100):
    logger.info("Starting generating %s  %s vouchers card with credit of %s", number, name, amount)
    kwargs = {
        'name' : name,
        'amount': amount
    }
    voucher_codes = [ voucher_service.voucher_generate() for i in range(number)]
    
    vouchers = (Voucher(name=name, amount=amount, code=code) for code in voucher_codes)
    while True:
        batch = list(islice(vouchers, batch_size))
        if not batch:
            break
        Voucher.objects.bulk_create(batch, batch_size)
    
    logger.info("Generation of  %s  %s vouchers card with credit of %s done.", number, name, amount)
    
