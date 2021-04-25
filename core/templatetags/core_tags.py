from django import template
from pay import utils
from accounts import constants as ACCOUNT_CONSTANTS
import logging

logger = logging.getLogger(__name__)
register = template.Library()


@register.filter
def access_dict(_dict, key):
    if isinstance(_dict, dict) :
        return _dict.get(key, None)
    return None



@register.filter
def account_type_key(value):
    k,v = utils.find_element_by_value_in_tuples(value, ACCOUNT_CONSTANTS.ACCOUNT_TYPE)
    if k is None:
        logger.info(f"account_type_key: Could not found key  for value \"{value}\"")
        return value
    return k


@register.filter
def account_type_value(key):
    k,v = utils.find_element_by_key_in_tuples(key, ACCOUNT_CONSTANTS.ACCOUNT_TYPE)
    if v is None:
        logger.info(f"account_type_value: Could not found value  for key \"{key}\"")
        return key
    return v