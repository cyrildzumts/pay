from pay import utils
from django.contrib.auth.models import User
from django.db.models import F, Q
from django.db.models import Count, Sum, Avg, Min, Max
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
import logging
from datetime import datetime



logger = logging.getLogger(__name__)



def get_model_instance_filter_by(appName=None, modelName=None, **kwargs):
    model = utils.get_model(appName, modelName)
    instance = None
    if model is None:
        logger.debug('No model %s found in the app %s')
        return None
    try:
        instance = model.objects.get(**kwargs)
    except ObjectDoesNotExist as e:
        logger.error("No model entry found with the following attribut : %s", **kwargs)
    
    except MultipleObjectsReturned as e:
        logger.error("Multiple entry found with the following attribut : %s. Only one entry is expected", **kwargs)

    return instance

def get_model_all_instance_filter_by(appName=None, modelName=None, **kwargs):
    model = utils.get_model(appName, modelName)
    queryset = None
    if model is None:
        logger.warning('No model %s found in the app %s')
    else :
        logger.debug("analytics query from the app %s and model %s with parameters %s", appName, modelName, **kwargs)
        queryset = model.objects.filter(**kwargs)

    return queryset


def get_number_model_instance_filter_by(appName=None, modelName=None, **kwargs):
    model = utils.get_model(appName, modelName)
    count = None
    if model is None:
        logger.warning('No model %s found in the app %s')
    else :
        logger.debug("analytics query number of instance from the app %s and model %s with parameters %s", appName, modelName, **kwargs)
        count = model.objects.filter(**kwargs).count()

    return count



def get_number_of_validated_account_by_country():
    '''
    This method returns a queryset that contains the number of by country.
    The queryset is laid out this way :
    QuerySet [{'field_name': 'field_value', 'number_of_users': 'a number'}].
    bellow is an example : 
    QuerySet [{'country': 'Cameroon', 'number_of_users': 4}].
    If the queryset return many country, then there will be more than one entry in the queryset.
    None is returned when no model could be found in the app defined by appName
    '''
    appName='accounts'
    modelName = 'Account'
    field = 'country'
    model = utils.get_model(appName, modelName)
    queryset = None
    accounts_by_country = None
    if model is None:
        logger.warning('No model %s found in the app %s')
    else :
        logger.debug("analytics query number of account grouped by Country  from the app %s and model %s", appName, modelName)
        validated_account = model.objects.filter(email_validated=True)
        accounts_by_country = validated_account.values(field).annotate(number_of_users=Count(field))
    return accounts_by_country



def get_number_of_validated_account_by_city():
    '''
    This method returns a queryset that contains the number of user by city grouped by country.
    The queryset is laid out this way :
    QuerySet [{'country_field_name': field_value,'city_field_name': fiedl_value, 'number_of_users': 'a number'}].
    bellow is an example : 
    QuerySet [{'country': 'Cameroon', 'city': 'Yaoundé', 'number_of_users': 4}].
    An attention should be paid to the order in which the fields are entered in the values() function.
    The fields will appear in the same order in the result.
    If the queryset return many country, then there will be more than one entry in the queryset.
    None is returned when no model could be found in the app defined by appName
    '''
    appName='accounts'
    modelName = 'Account'
    city_field = 'city'
    country_field = 'country'
    model = utils.get_model(appName, modelName)
    queryset = None
    accounts_by_city = None
    if model is None:
        logger.warning('No model %s found in the app %s')
    else :
        logger.debug("analytics query number of account grouped by Country and City  from the app %s and model %s", appName, modelName)
        validated_account = model.objects.filter(email_validated=True)
        accounts_by_city = validated_account.values(country_field, city_field).annotate(number_of_users=Count(city_field))
    return accounts_by_city


def get_number_of_account():
    queryset = get_number_model_instance_filter_by(appName='accounts', modelName='Account', **{'is_active_account': True})
    return queryset.count()

def get_number_of_validated_account():
    queryset = get_number_model_instance_filter_by(appName='accounts', modelName='Account', **{'email_validated':True})
    return queryset.count()

def get_max_transfered_amount_pro_user():
    '''
    This method return a dict that contains the max transfered amount.
    the dict is represented as follow :
    {'max_transferred_amount': max_amount}.
    Example : [{'recipient':value, 'recipient_user__username': value, 'number_of_transfers': value,'max_transferred_amount': value},
    ...,
    ...
    ].
    None is returned when no Transfer
    '''
    amount_field = 'amount'
    appName = 'payments'
    modelName = 'Transfer'
    recipient_field = 'recipient'
    recipient_name_field = 'recipient__user__username'
    created_at_field = 'created_at'
    queryset = get_model_all_instance_filter_by(appName, modelName, **{})
    if queryset is not None:
        queryset.values(recipient_field, recipient_name_field).annotate(number_of_transfers=Count(recipient_field)).annotate(max_transferred_amount=Max(amount_field))
    return queryset

def get_max_transfered_amount():
    '''
    This method return a dict that contains the max transfered amount.
    the dict is represented as follow :
    {'max_transferred_amount': max_amount}.
    Example : {'max_transferred_amount': value}
    None is returned when no Transfer
    '''
    amount_field = 'amount'
    appName = 'payments'
    modelName = 'Transfer'

    queryset = get_model_all_instance_filter_by(appName, modelName, **{})
    if queryset is not None:
        queryset.aggregate(max_transferred_amount=Max(amount_field))
    return queryset


def get_transfers_summary():
    '''
    This method returns a transfer summary as a queryset.
    The output of this queryset is as follow :

    QuerySet [{'created_at': value, 'number_of_transfers': value, 'max_transferred_amount': value, 'min_transferred_amount},
    ...,
    ...,
    ]
    The query is sorted by the order_by_field variable. The value of this variable must be an attribut of the Transfer Model.

    TODO : Add a verification on the existence of the field in the model defined by modelName.
    '''
    amount_field = 'amount'
    appName = 'payments'
    modelName = 'Transfer'
    pk_field = 'pk'
    order_by_field = '-created_at'
    recipient_field = 'recipient'
    sender_field = 'sender'
    recipient_name_field = 'recipient__user__username'
    created_at_field = 'created_at'
    summary = None
    Transfer = utils.get_model(appName, modelName)
    queryset = Transfer.objects.filter(created_at__month=datetime.now().month)
    #queryset = get_model_all_instance_filter_by(appName, modelName, **{'created_at__month': datetime.now().month})
    if queryset is not None:
        summary = queryset.aggregate(number_of_transfers=Count(pk_field),max_transferred_amount=Max(amount_field),
            min_transferred_amount=Min(amount_field), number_of_sender=Count(sender_field, distinct=True), 
            number_of_recipients=Count(recipient_field, distinct=True), average_transferred_amount=Avg(amount_field) )
    return summary


def get_service_usage_summary():
    appName ='accounts'
    modelName = 'Service'
    price_field = 'price'
    pk_field = 'pk'
    customer_field = 'customer'
    operator_field = 'operator'
    summary = None
    Service = utils.get_model(appName, modelName)
    queryset = Service.objects.filter(created_at__month=datetime.now().month)
    if queryset is not None:
        logger.debug("get_service_usage: queryet not None")
        summary = queryset.aggregate(total_amount=Sum(price_field), usage_count=Count(pk_field), 
        min_paid_amount=Min(price_field), max_paid_amount=Max(price_field), number_of_customer=Count(customer_field, distinct=True),
        number_of_operator=Count(operator_field, distinct=True), average_amount=Avg(price_field))

    return summary

def dashboard_summary():
    """
    This method returns a summary context variable that contains 
    summary report on the services and transfers of the current month.
    The service summary provides the following data :
    {total_amount, usage_count, min_paid_amount, max_paid_amount, number_of_customer, number_of_operator, average_amount}.

    The transfer summary provides the following data :
    {number_of_transfers, max_transferred_amount, min_transferred_amount, number_of_sender, number_of_recipient,average_transferred_amount}
    """
    #Service = utils.get_model('accounts', 'Service')
    #Transfer = utils.get_model('payments', 'Transfer')
    #service_queryset = Service.objects.filter(created_at__month=datetime.now().month)
    #transfer_queryset = Transfer.objects.filter(created_at__month=datetime.now().month)
    service_summary = get_service_usage_summary()
    transfer_summary = get_transfers_summary()
    context = {
        'service_summary': service_summary,
        'transfer_summary': transfer_summary
    }


def get_number_of_active_account():
    return utils.get_model('accounts', 'Account').objects.filter(is_active=True).count()


def get_all_account_filter_by(**kwargs):
    return utils.get_model('accounts', 'Account').objects.filter(**kwargs)

def get_account_filter_by(**kwargs):
    return utils.get_model('accounts', 'Account').objects.get(**kwargs)


def get_number_of_account_filter_by(**kwargs):
    return utils.get_model('accounts', 'Account').objects.filter(**kwargs).count()

def get_idcards_filter_by(**kwargs):
    return utils.get_model('accounts', 'IDCard').objects.filter(**kwargs)

def get_nomber_of_idcards_filter_by(**kwargs):
    return utils.get_model('accounts', 'IDCard').objects.filter(**kwargs).count()

def get_services_filter_by(**kwargs):
    return utils.get_model('accounts', 'Service').objects.filter(**kwargs)

def get_number_of_services_filter_by(**kwargs):
    return utils.get_model('accounts', 'Service').objects.filter(**kwargs).count()

def get_available_services_filter_by(**kwargs):
    return utils.get_model('accounts', 'AvailableService').objects.filter(**kwargs)


def get_number_available_services_filter_by(**kwargs):
    return utils.get_model('accounts', 'AvailableService').objects.filter(**kwargs).count()


def get_category_services_filter_by(**kwargs):
    return utils.get_model('accounts', 'ServiceCategory').objects.filter(**kwargs)


def get_number_category_services_filter_by(**kwargs):
    return utils.get_model('accounts', 'ServiceCategory').objects.filter(**kwargs).count()


def get_policies_filter_by(**kwargs):
    return utils.get_model('accounts', 'Policy').objects.filter(**kwargs)


def get_number_of_policies_filter_by(**kwargs):
    return utils.get_model('accounts', 'Policy').objects.filter(**kwargs).count()