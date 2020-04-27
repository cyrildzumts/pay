from celery import shared_task
from voucher.models import Voucher
from voucher import voucher_service
from itertools import islice
import logging, uuid


logger = logging.getLogger(__name__)
batch_size = 15

@shared_task
def generate_voucher(context={}):
    
    name='PAY-STANDARD'
    amount=2500
    number=100
    if context :
        name = context.get('name', name)
        amount = context.get('amount', amount)
        number = context.get('number', number)
        user   = context.get('user')

    logger.info("Starting generating %s  %s vouchers card with credit of %s", number, name, amount)
    kwargs = {
        'name' : name,
        'amount': amount
    }
    voucher_codes = [ voucher_service.voucher_generate() for i in range(number)]
    logger.info("Gener")
    vouchers = (Voucher(name=name, amount=amount, voucher_code=code) for code in voucher_codes)
    while True:
        batch = list(islice(vouchers, batch_size))
        if not batch:
            break
        Voucher.objects.bulk_create(batch, batch_size)
    
    logger.info("Generation of  %s  %s vouchers card with credit of %s done.", number, name, amount)
    
