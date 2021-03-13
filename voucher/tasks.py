from celery import shared_task
from voucher.models import Voucher
from django.contrib.auth.models import User
from voucher import voucher_service
from itertools import islice
import logging, uuid


logger = logging.getLogger(__name__)
batch_size = 15

@shared_task
def generate_voucher(context={}):
    
    name='PAY-STANDARD'
    amount=2500
    number=10
    user = None
    if context :
        name = context.get('name', name)
        amount = context.get('amount', amount)
        number = context.get('number', number)
        user_pk = context.get('user')
        try:
            user = User.objects.get(pk=user_pk)
        except User.DoesNotExist:
            logger.warn(f"No user found with id {user_pk} ")
    
    if user is None:
        logger.warn(f"Generation of vouchers aborted requester user is missing")
        return

    logger.info(f"Starting generating {number}  {name} vouchers card with credit of {amount}")
    voucher_codes = [ voucher_service.voucher_generate() for i in range(number)]
    vouchers = (Voucher(name=name, amount=amount, voucher_code=code, created_by=user) for code in voucher_codes)
    while True:
        batch = list(islice(vouchers, batch_size))
        if not batch:
            break
        Voucher.objects.bulk_create(batch, batch_size, ignore_conflicts=True)
    
    logger.info(f"[OK] Generation of {number}  {name} vouchers card with credit of {amount} done")
    
