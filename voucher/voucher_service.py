from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from django.db.models import F, Q
from django.utils import timezone
from pay import utils
from pay import settings
from voucher.models import Voucher, SoldVoucher, UsedVoucher, Recharge
import codecs
import random
import hashlib

from datetime import datetime
import logging


logger = logging.getLogger(__name__)

DEFAULT_VOUCHER_LIMIT = 1000

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

            Account = utils.get_model("accounts", "Account")
            user = User.objects.get(pk=user_pk)
            voucher_queryset = Voucher.objects.filter(voucher_code=voucher)
            voucher_queryset.update(is_used=True)
            v = voucher_queryset.get()
            amount = v.amount
            Account.objects.filter(user=user).update(balance=F('balance') + amount)
            UsedVoucher.objects.create(customer=user, voucher=v)

            logger.info("Voucher %s used by user %s", voucher, user.get_full_name())
            succeed = True
        else:

            logger.info("Voucher %s could not be used. Verify that the voucher is activated", voucher)
            
        return succeed,amount


    @staticmethod
    def get_voucher_set(start=None, end=None, **filters):       
        return Voucher.objects.filter(**filters)[start:end]

    @staticmethod
    def get_used_voucher_set(start=None, end=None, **filters):       
        return UsedVoucher.objects.filter(**filters)[start:end]


    @staticmethod
    def get_sold_voucher_set(start=None, end=None, **filters):       
        return SoldVoucher.objects.filter(**filters)[start:end]

    @staticmethod
    def get_recharge_set(start=None, end=None, **filters):       
        return Recharge.objects.filter(**filters)[start:end]

    @classmethod
    def process_recharge_user_account(cls, seller=None, customer=None, amount=-1):
        now = datetime.now()
        result = {
            'succeed': False,
            'errors': ''
        }
        Account = utils.get_model("accounts", "Account")
        Recharge = utils.get_model("voucher", "Recharge")
        queryset = Account.objects.filter(Q(user__username=settings.PAY_RECHARGE_USER) | (Q(user=seller) | Q(user=customer)))
        count = queryset.count()
        if count != 3:
            logger.info("[processing_service_request] Error : Recharge, customer ans Seller Account not found. The service request cannot be processed")
            logger.error("[processing_service_request] Error : queryset result %s instance", count)
            logger.error(queryset)
            result['errors'] = "Recharge account not found. The service request cannot be processed"
            return result
        if  amount > 0 :
            v = Voucher.objects.filter(activated=False,is_sold=False, is_used=False, amount=amount).first()
            if v is None :
                v = Voucher.objects.create(name="STAFF GENERATED CARD", voucher_code = cls.get_voucher(seller), 
                    activated=True,is_sold=True, is_used=True, amount=amount, used_by=customer, sold_by=seller,
                    activated_at=timezone.now(), used_at=timezone.now(), sold_at=timezone.now())
            else :
                Voucher.objects.filter(pk=v.pk).update(activated=True, is_sold=True, is_used=True, used_by=customer, sold_by=seller,
                    activated_at=timezone.now(), used_at=timezone.now(), sold_at=timezone.now())
            queryset.update(balance=F('balance') + amount)
            Recharge.objects.create(voucher=v, customer=customer, seller=seller, amount=amount)
            logger.info("User Account %s has been recharge by the User %s with the amount of %s", queryset.get(user=customer).full_name(), queryset.get(user=seller).full_name(), amount)
            result['succeed'] = True
        else:
            logger.info("[processing_service_request] Error : Amount is negativ (%s). The service request cannot be processed", amount)
            result['errors'] = "Amount is negativ {}. The service request cannot be processed".format(amount)
            return result
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
            


    


