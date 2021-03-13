from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from django.db.models import F, Q
from django.utils import timezone
from pay import utils
from pay import settings
from voucher.models import Voucher, SoldVoucher, UsedVoucher, Recharge
from payments.models import Balance, BalanceHistory
from payments import constants as PAYMENTS_CONSTANTS

import codecs
import random
import hashlib

from datetime import datetime
import logging


logger = logging.getLogger(__name__)

DEFAULT_VOUCHER_LIMIT = 100

VOUCHER_DEFAULT_PART_COUNT = 4
VOUCHER_DEFAULT_PART_LENGTH = 4

BAD_WORDS = map(lambda w: codecs.decode(w, 'rot13'), [
    'SHPX', 'PHAG', 'JNAX', 'JNAT', 'CVFF', 'PBPX', 'FUVG', 'GJNG', 'GVGF',
    'SNEG', 'URYY', 'ZHSS', 'QVPX', 'XABO', 'NEFR', 'FUNT', 'GBFF', 'FYHG',
    'GHEQ', 'FYNT', 'PENC', 'CBBC', 'OHGG', 'SRPX', 'OBBO', 'WVFZ', 'WVMM',
    'CUNG'
])

SYMBOLS = list('0123456789ABCDEFGHJKLMNPQRTUVWXY')

SYMBOLS_MAP = {s: i for i, s in enumerate(SYMBOLS)}

PART_SEP = '-'

REPLACEMENTS = [
    (r'[^0-9A-Z]+', ''),
    (r'O', '0'),
    (r'I', '1'),
    (r'Z', '2'),
    (r'S', '5')
]

def has_bad_word(code):
    """ Check if a given code contains a bad word.
    """
    for word in BAD_WORDS:
        if word in code:
            return True
    return False


def check_digit(data, n):
    """ Generate the check digit for a code part.
    """
    for c in data:
        n = n * 19 + SYMBOLS_MAP[c]
    return SYMBOLS[n % (len(SYMBOLS) - 1)]


def voucher_generate(plaintext=None, n_parts=VOUCHER_DEFAULT_PART_COUNT, part_len=VOUCHER_DEFAULT_PART_LENGTH):
    """ Generate a coupon code.

    Parameters:
    -----------
    plaintext : str
        A plaintext to generate the code from.

    n_parts : int
        The number of parts for the code.

    part_len : int
        The number of symbols in each part.

    Returns:
    --------
    A coupon code string.
    """
    parts = []
    # sha1 module to be used
    
    if plaintext is not None:
        raise NotImplementedError(
            'Generating a code from plaintext is not yet implemented'
        )

    while len(parts) == 0 or has_bad_word(''.join(parts)):
        for i in range(n_parts):
            part = ''
            for j in range(part_len - 1):
                part += random.choice(SYMBOLS)
            part += check_digit(part, i+1)
            parts.append(part)

    return PART_SEP.join(parts)



def voucher_validate(code, n_parts=VOUCHER_DEFAULT_PART_COUNT, part_len=VOUCHER_DEFAULT_PART_LENGTH):
    """ Validate a given code.

    Parameters:
    -----------
    code : str
        The code to validate.

    n_parts : int
        The number of parts for the code.

    part_len : int
        The number of symbols in each part.

    Returns:
    --------
    A cleaned code if the code is valid, otherwise an empty string.
    """
    is_valid = True
    code = code.upper()
    for replacement in REPLACEMENTS:
        code = code.replace(*replacement)

    parts = code.split(PART_SEP)
    if len(parts) != n_parts:
        is_valid = False

    for i, part in enumerate(parts):
        if len(part) != part_len:
            is_valid = False

        data = part[0:-1]
        check = part[-1]

        if check != check_digit(data, i+1):
            is_valid = False

    return is_valid


def update_balance(data):
    recipient = data['recipient']
    sender = data['sender']
    recipient_amount = data['recipient_amount']
    amount = data['amount']
    voucher = data['voucher']
    activity = data['activity']

    if activity == PAYMENTS_CONSTANTS.BALANCE_ACTIVITY_RECHARGE:
        recharge = Recharge.objects.create(voucher=voucher, customer=recipient, seller=voucher.sold_by, amount=amount)
        BalanceHistory.objects.create(balance=sender.balance, balance_ref_id=sender.balance.pk, recharge=recharge, activity=activity, voucher=voucher , current_amount=-amount, current_amount_without_fee=-amount, balance_amount=sender.balance.balance, balance_amount_without_fee=sender.balance.balance, sender=sender, receiver=recipient)
        BalanceHistory.objects.create(balance=recipient.balance, balance_ref_id=recipient.balance.pk,recharge=recharge,  activity=activity, voucher=voucher , current_amount=amount, current_amount_without_fee=+amount ,balance_amount=recipient.balance.balance, balance_amount_without_fee=recipient.balance.balance_without_fee, sender=sender, receiver=recipient)

        Balance.objects.filter(user=recipient).update(balance=F('balance') + amount, balance_without_fee=F('balance_without_fee') + amount)
        Balance.objects.filter(user=sender).update(balance=F('balance') - amount, balance_without_fee=F('balance_without_fee') - amount)
        


class VoucherService:
    """
    voucher_activated : contains a list of activated voucher code
    voucher_generated : contains a list of of valide generated  voucher code
    voucher_already_used : contains a list of aleady used voucher code. used voucher are invalid
    """
    voucher_activated = set()
    voucher_generated = set()
    voucher_already_used = set()
    generated_voucher = 0
    used_voucher = 0
    activated_voucher = 0

    def __init__(self, voucher_number=DEFAULT_VOUCHER_LIMIT):
        for i in range(voucher_number):
            VoucherService.voucher_generated.add(voucher_generate())
        
        VoucherService.generated_voucher = voucher_number
        logger.info("VoucherService initialized with {0} Vouchers".format(voucher_number))
    

    @classmethod
    def is_valide(cls, voucher):
        flag = False
        if voucher and isinstance(voucher, str):
            flag = voucher_validate(voucher)
        return flag


    @classmethod
    def can_be_used(cls, voucher):
        flag = False
        Voucher = utils.get_model("voucher", "Voucher")
        if cls.is_valide(voucher):
            flag = Voucher.objects.filter(voucher_code=voucher, activated=True, is_used=False).exists()
        return flag


    @classmethod
    def use_voucher(cls, voucher, user_pk=None):
        succeed = False
        amount = 0
        if cls.can_be_used(voucher):
            recipient = User.objects.get(pk=user_pk)
            voucher_queryset = Voucher.objects.filter(voucher_code=voucher)
            v = voucher_queryset.get()
            amount = v.amount
            data = {
                'sender' : v.sold_by,
                'recipient': recipient,
                'amount': amount,
                'recipient_amount' : amount,
                'voucher' : v,
                'activity' : PAYMENTS_CONSTANTS.BALANCE_ACTIVITY_RECHARGE
            }
            update_balance(data)
            
            voucher_queryset.update(is_used=True, used_by=recipient, used_at=timezone.now())

            logger.info(f"Voucher {voucher} used by user {user.get_full_name()} ")
            succeed = True
        else:

            logger.info(f"Voucher {voucher} could not be used. Verify that the voucher is activated")
            
        return succeed,amount


    @staticmethod
    def get_voucher_set(start=None, end=None, **filters):       
        return Voucher.objects.filter(**filters).order_by('-created_at')[start:end]

    @staticmethod
    def get_used_voucher_set(start=None, end=None, **filters):       
        return Voucher.objects.filter(is_used=True).filter(**filters).order_by('-created_at')[start:end]


    @staticmethod
    def get_sold_voucher_set(start=None, end=None, **filters):       
        return SoldVoucher.objects.filter(is_sold=True).filter(**filters).order_by('-created_at')[start:end]

    @staticmethod
    def get_recharge_set(start=None, end=None, **filters):       
        return Recharge.objects.filter(**filters).order_by('-created_at')[start:end]

    @classmethod
    def process_recharge_user_account(cls, seller=None, customer=None, amount=-1):
        now = datetime.now()
        result = {
            'succeed': False,
            'errors': ''
        }
        Recharge = utils.get_model("voucher", "Recharge")
        recharge_account_exist = User.objects.filter(username=settings.PAY_RECHARGE_USER).exists()
        customer_account_exist = customer is not None
        seller_account_exist = seller is not None
        if not (recharge_account_exist and customer_account_exist and seller_account_exist):
            logger.info("[processing_service_request] Error : Recharge, customer ans Seller Account not found. The service request cannot be processed")
            result['errors'] = "The service request cannot be processed"
            return result
        if  amount > 0 :
            v = Voucher.objects.filter(activated=False,is_sold=False, is_used=False, amount=amount).first()
            if v is None :
                v = Voucher.objects.create(name="STAFF GENERATED CARD", voucher_code = cls.get_voucher(seller), 
                    activated=True,is_sold=True, is_used=True, amount=amount, used_by=customer, sold_by=seller,
                    activated_at=timezone.now(), activated_by=seller, used_at=timezone.now(), sold_at=timezone.now())
            else :
                Voucher.objects.filter(pk=v.pk).update(activated=True, is_sold=True, is_used=True, used_by=customer, activated_by=seller, sold_by=seller,
                    activated_at=timezone.now(), used_at=timezone.now(), sold_at=timezone.now())
            Balance.objects.filter(user__username=settings.PAY_RECHARGE_USER).update(balance=F('balance') + amount)
            Balance.objects.filter(user=customer).update(balance=F('balance') + amount)
            Recharge.objects.create(voucher=v, customer=customer, seller=seller, amount=amount)
            logger.info("User Account %s has been recharge by the User %s with the amount of %s", customer.get_full_name(), seller.get_full_name(), amount)
            result['succeed'] = True
        else:
            logger.info("[processing_service_request] Error : Amount is negativ (%s). The service request cannot be processed", amount)
            result['errors'] = "Amount is negativ {}. The service request cannot be processed".format(amount)
            return result
        return result


    @classmethod
    def recharge_balance(cls, seller, customer, amount):
        
        result = {
            'succeed': False,
            'errors': ''
        }
        if not isinstance(seller, User) or not isinstance(customer, User):
            return result

        Recharge = utils.get_model("voucher", "Recharge")

        if  amount > 0 :
            v = Voucher.objects.filter(activated=False,is_sold=False, is_used=False, amount=amount).first()
            if v is None :
                v = Voucher.objects.create(name="STAFF GENERATED CARD", voucher_code = cls.get_voucher(seller), 
                    activated=True,is_sold=True, is_used=True, amount=amount, used_by=customer, sold_by=seller,
                    activated_at=timezone.now(), activated_by=seller, used_at=timezone.now(), sold_at=timezone.now())
            else :
                Voucher.objects.filter(pk=v.pk).update(activated=True, is_sold=True, is_used=True, used_by=customer, activated_by=seller, sold_by=seller,
                    activated_at=timezone.now(), used_at=timezone.now(), sold_at=timezone.now())

            data = {
                'sender' : seller,
                'recipient': customer,
                'amount': amount,
                'recipient_amount' : amount,
                'voucher': v,
                'activity' : PAYMENTS_CONSTANTS.BALANCE_ACTIVITY_RECHARGE
            }
            update_balance(data)
            #Recharge.objects.create(voucher=v, customer=customer, seller=seller, amount=amount)
            logger.info(f"User Balance {customer.username} has been recharged by the User {seller.username} with the amount of {amount}")
            result['succeed'] = True
        else:
            logger.info(f"[processing_service_request] Error : Amount is negativ {amount}. The service request cannot be processed")
            result['errors'] = f"Amount is negativ {amount}. The service request cannot be processed"
  
        return result


    @classmethod
    def activate_voucher(cls,voucher, seller=None):
        succeed = False
        #TODO Add permission checking.User must have the permission to activate a voucher
        if cls.is_valide(voucher):
            queryset = Voucher.objects.filter(voucher_code=voucher, activated=False, is_used=False)
        if queryset.exists():
            queryset.update(activated=True, activated_by=seller, activated_at=timezone.now(), is_sold=True, sold_by=seller, sold_at=timezone.now())
            succeed = True
            logger.info("Voucher %s is successfuly activated ",voucher)

        else :
            logger.warning("Voucher %s is whether activated or it doesn't exists.",voucher)

        return succeed

    @classmethod
    def generate_new_code(cls,number_of_code=DEFAULT_VOUCHER_LIMIT, parts=VOUCHER_DEFAULT_PART_COUNT, part_len=VOUCHER_DEFAULT_PART_LENGTH):
        for i in range(number_of_code):
            cls.voucher_generated.add(voucher_generate(n_parts=parts, part_len=part_len))
        
        cls.generated_voucher += number_of_code
        logger.info("Generated %s new vouchers code", number_of_code)
    

    @classmethod
    def get_voucher(cls, user):
        voucher = None
        if cls.generated_voucher <= cls.used_voucher:
            logger.info("There are no voucher left. New voucher are now generated")
            cls.generate_new_code(number_of_code=DEFAULT_VOUCHER_LIMIT)
        voucher = cls.voucher_generated.pop()
        cls.activate_voucher(voucher, user)
        return voucher


    @classmethod
    def get_generated_voucher(cls):
        return list(cls.voucher_generated)
    
    @classmethod
    def get_used_voucher(cls):
        return list(cls.voucher_already_used)
    
    @classmethod
    def get_activated_voucher(cls):
        return list(cls.voucher_activated)

    @classmethod
    def summary(cls):
        summary_str = """ Voucher usage summary as of today {}.\n
                  Total number of vouchers created : {}\n
                  Number of used Voucher : {}\n
                  Number of active Voucher {} \n""".format(datetime.now(),cls.generated_voucher, cls.used_voucher, cls.activated_voucher)
        logger.info(summary_str)
            


    


