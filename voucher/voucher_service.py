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
        if cls.is_valide(voucher):
            active = voucher in cls.voucher_activated
            used = voucher not in cls.voucher_already_used
            flag = active and used
        return flag

    @classmethod
    def use_voucher(cls, voucher):
        if cls.can_be_used(voucher):
            cls.voucher_already_used.add(voucher)
            try:
                cls.voucher_activated.remove(voucher)
                cls.used_voucher += 1
                logger.info("Voucher {} used.".format(voucher))
            except KeyError:
                logger.error("Voucher error : Voucher {} not in the activated list".format(voucher))
                
        else:
            logger.info("Voucher {} could not be used.".format(voucher))
            
    


    @classmethod
    def activate_voucher(cls,voucher):
        if cls.is_valide(voucher):
            if voucher not in cls.voucher_activated:
                cls.voucher_activated.add(voucher)
                cls.activated_voucher += 1
                logger.info("Voucher {} activated.".format(voucher))
            else :
                 logger.warning("Voucher {} already activated.".format(voucher))
    

    @classmethod
    def generate_new_code(cls,number_of_code=DEFAULT_VOUCHER_LIMIT, parts=VOUCHER_DEFAULT_PART_COUNT, part_len=VOUCHER_DEFAULT_PART_LENGTH):
        for i in range(number_of_code):
            cls.voucher_generated.add(voucher_generate(n_parts=parts, part_len=part_len))
        
        cls.generated_voucher += number_of_code
        logger.info("Generated %s new vouchers code", number_of_code)
    

    @classmethod
    def get_voucher(cls):
        voucher = None
        if cls.generated_voucher <= cls.used_voucher:
            logger.info("There are no voucher left. New voucher are now generated")
            cls.generate_new_code(number_of_code=DEFAULT_VOUCHER_LIMIT)
        voucher = cls.voucher_generated.pop()
        cls.activate_voucher(voucher)
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
        print(summary_str)
            


    


