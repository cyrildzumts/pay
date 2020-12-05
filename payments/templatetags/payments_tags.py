
from django import template
from pay import utils
from payments import constants as Constants
import logging

logger = logging.getLogger(__name__)


register = template.Library()



@register.filter
def declined_reason_key(value):
    k,v = utils.find_element_by_value_in_tuples(value, Constants.REFUND_DECLINED_REASON)
    if k is None:
        logger.info(f"declined_reason_key : Could not found key  for value \"{value}\"")
        return value
    return k

@register.filter
def declined_reason_value(key):
    k,v = utils.find_element_by_key_in_tuples(key, Constants.REFUND_DECLINED_REASON)
    if v is None:
        logger.info(f"declined_reason_value: Could not found value  for key \"{key}\"")
        return key
    return v


@register.filter
def payment_status_key(value):
    k,v = utils.find_element_by_value_in_tuples(value, Constants.REFUND_STATUS)
    if k is None:
        logger.info(f"payment_status_key : Could not found key  for value \"{value}\"")
        return value
    return k

@register.filter
def payment_status_value(key):
    k,v = utils.find_element_by_key_in_tuples(key, Constants.REFUND_STATUS)
    if v is None:
        logger.info(f"payment_status_value: Could not found value  for key \"{key}\"")
        return key
    return v