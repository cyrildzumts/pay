from django.contrib import auth
from django.contrib.auth.models import User
from django.db import IntegrityError
from pay import utils, settings
from abc import ABCMeta, ABC
from payments.forms import   ServiceCreationForm, IDCardForm, RechargeForm, PaymentForm, TransactionForm, TransferForm
from payments.models import Policy, Transaction, Transfer, Service, Payment
from django.db.models import F, Q
from django.apps import apps
from django.forms import modelform_factory
from voucher import voucher_service
import sys
import logging
import numbers


logger = logging.getLogger(__name__)

this = sys.modules[__name__]
this.TransactionModel = utils.get_model('payments', 'Transaction')
this.TransactionForm = None
this.TransferModel = utils.get_model('payments', 'Transfer')
this.TransferForm = None
this.ServiceForm = ServiceCreationForm


class PaymentService :
    
    @staticmethod
    def get_commission(price, applied_commision):
        pay_fee = 0
        operator_amount = price
        succeed = False
        if isinstance(price, numbers.Number) and isinstance(applied_commision, numbers.Number):
            pay_fee = round(price * applied_commision, 2)
            operator_amount = price - pay_fee
            succeed = True
        logger.info("Commission : {} - PAY fee : {} - Price : {} - Operator Amount : {}".format(applied_commision, pay_fee, price, operator_amount))
        
        return (pay_fee, operator_amount, succeed)

    @staticmethod
    def create_policy(policy_data=None):
        created = False
        if policy_data:
            try:
                p , created = Policy.objects.get_or_create(**policy_data)
            except IntegrityError:
                pass
        return created

    @staticmethod
    def add_idcard_to_user(cardImage=None):
        created = False
        return created

    @classmethod
    def make_payment(cls, request):
        pass
    

    @classmethod
    def is_payment_validated(cls, request):
        return False
    
    @classmethod
    def extract_participants(cls, request):
        participants = {}
        participants['receiver_id'] = None
        participants['sender_id'] = None
        return None
    
    @classmethod
    def extract_amount(cls, request):
        return 0
    

    @classmethod
    def can_customer_pay(cls, customer_id):
        return False

    @staticmethod
    def process_transaction_request(request, transaction_type = 'T'):
        context = {}
        context['success'] = False
        logger.debug("[account_service.py] process_transaction_request entering")
        
        if request.method == 'POST':
            logger.debug("[account_service.py] process_transaction_request entering : POST REQUEST")
            Account = utils.get_model('accounts', 'Account')
            current_account = Account.objects.get(user=request.user)
            current_balance = current_account.balance
            postdata = utils.get_postdata(request)
            transaction_form = TransactionForm(postdata)
            if transaction_form.is_valid():
                logger.debug("[account_service.py] process_transaction_request entering : Transaction Form is Valid")
                recipient = postdata['recipient']
                amount = int(postdata['amount'])
                if(current_balance >=  amount):
                    recipient_exist = Account.objects.filter(user_email=recipient).exists()
                    if recipient_exist:
                        Account.objects.all().filter(user_email=recipient).update(balance=F('balance') + amount)
                        Account.objects.all().filter(pk=current_account.pk).update(balance=F('balance') - amount)
                        transaction_form.save()
                        context['success'] = True
                        context['balance'] = current_account.balance - amount
                    else:
                        context['errors'] = "The recipient could not be found."
                        logger.debug("[account_service.py]There was an error with the transaction request : ")
                        logger.debug(context['errors'])
                        return context
                    
                else :
                    context['success'] = False
                    context['balance'] = current_account.balance
                    context['errors'] = "Vous n'avez pas assez d'argent dans votre compte"
                    return context
        else:
            context['balance'] = current_account.balance
            context['errors'] = "Verifiez les champs du formulaire."
        return context


    @staticmethod
    def process_transfer_request(request):
        context = {}
        context['success'] = False
        logger.debug("[account_service.py] process_transaction_request entering")
        Account = utils.get_model('accounts', 'Account')

        if request.method == 'POST':
            logger.info("processing new transfer request : POST REQUEST")
            current_account = Account.objects.get(user=request.user)
            current_balance = current_account.balance
            postdata = utils.get_postdata(request)
            transfer_form = TransferForm(postdata)
            if transfer_form.is_valid():
                logger.info(" Transfer Form is Valid")
                recipient = postdata['recipient']
                amount = int(postdata['amount'])
                if(current_balance - amount) >= 0:
                    recipient_exist = Account.objects.filter(user=recipient).exists()
                    if recipient_exist:
                        Account.objects.all().filter(user=recipient).update(balance=F('balance') + amount)
                        Account.objects.all().filter(pk=current_account.pk).update(balance=F('balance') - amount)
                        transfer_form.save()
                        context['success'] = True
                        context['balance'] = current_balance - amount
                        logger.info("Transfer was succefull")
                    else:
                        context['errors'] = "The recipient could not be found."
                        logger.error("There was an error with the transfer request : %s", context['errors'])
                        
                        return context
                    
                else :
                    context['success'] = False
                    context['balance'] = current_account.balance
                    context['errors'] = "Vous n'avez pas assez d'argent dans votre compte"
                    return context
        else:
            context['balance'] = current_account.balance
            context['errors'] = "Verifiez les champs du formulaire."
        return context


    
    @staticmethod
    def process_service_request(request, service_pk=None):
        #TODO : when a user registers itself, for bussiness users it should be checked
        # that all the necessary fields are present : policy, id card and email is verified
        context = {}

        context['success'] = False
        logger.debug("[account_service.py] process_service_request entering")
        Account = utils.get_model('accounts', 'Account')
        

        if request.method == 'POST':
            logger.info("processing new service request : POST REQUEST")
            postdata = utils.get_postdata(request)
            postdata.setdefault('commission', 0.03)
            service_form = ServiceCreationForm(postdata)
            if service_form.is_valid():
                logger.info(" Service Form is Valid")
                user_operator = postdata['operator']
                price = int(postdata['price'])
                pay_account_exist= Account.objects.filter(user__username="pay").exists()
                if not pay_account_exist:
                    logger.debug("[processing_service_request] Error : Pay account not found. The service request cannot be processed")
                    context['errors'] = "Pay account not found. The service request cannot be processed"
                    return context
                pay_account = Account.objects.get(user__username="pay")
                current_account = Account.objects.get(user=request.user)
                operator_account = Account.objects.select_related().get(user=user_operator)
                current_balance = current_account.balance
                if(current_balance - price) >= 0:
                    operator_exist = Account.objects.filter(user=user_operator).exists()
                    if operator_exist:
                        commission = operator_account.policy.commission
                        pay_fee, operator_amount, succeed = PaymentService.get_commission(price,commission)
                        if succeed :
                            
                            Account.objects.all().filter(user=user_operator).update(balance=F('balance') + operator_amount)
                            Account.objects.all().filter(pk=current_account.pk).update(balance=F('balance') - price)
                            Account.objects.all().filter(pk=pay_account.pk).update(balance=F('balance') + pay_fee)
                            postdata['commission'] = commission
                            service_form = form(postdata)
                            service = service_form.save()
                            email_context = {
                                'title'             : 'Payment Confirmation',
                                'recipient_name'    : operator_account.full_name(),
                                'sender_name'       : current_account.full_name(),
                                'service_name'      : service.name,
                                'customer_reference': service.customer_reference,
                                'consumer_name'     : current_account.full_name(),
                                'reference_number'  : service.reference_number,
                                'invoice_date'      : service.issued_at,
                                'category_name'     : service.category.category_name,
                                'price'             : service.price,
                                'commission'        : service.commission,
                                'pay_fee'           : pay_fee,
                                'payment_date'      : service.created_at,
                                'description'       : service.description,
                                'template_name'     : 'accounts/service_mail_confirmation_incoming.html',
                                'recipient_email'   : service.operator.email,
                                'sender_email'      : service.customer.email,
                                'has_image'         : False
                            }
                            context['success'] = True
                            context['email_context'] = email_context
                            context['balance'] = current_balance - price
                            logger.info("Service Operation was succefull")
                            return context
                        else:
                            logger.info("Service Operation was not succefull : there was an error on process the commission fee")
                    else:
                        context['errors'] = "The service operator could not be found."
                        logger.error("There was an error with the service request : %s", context['errors'])
                        
                        return context
                    
                else :
                    context['success'] = False
                    context['balance'] = current_balance
                    context['errors'] = "You don't have enough money on your account."

                    return context
            else :
                #context['balance'] = current_balance
                logger.error("Form is Invalid : See the errors fields below")
                logger.error(service_form.errors)
                context['errors'] = "Form invalide : Check your Form fields please."
        else:
            #context['balance'] = current_balance
            context['errors'] = "Your request could not be process. Please Check the Form fields."
        return context

    @staticmethod
    def process_recharge_request(request):
        context = {
            'success': False
        }
        if request and request.method=="POST":
            logger.info("processing new recharge request")
            postdata = utils.get_postdata(request)
            recharge_form = RechargeForm(postdata)
            if recharge_form.is_valid():
                logger.info(" Submitted Recharge Form is Valid")
                voucher = recharge_form.cleaned_data['voucher']
                succeed, amount = voucher_service.VoucherService.use_voucher(voucher, request.user.pk)
                if succeed:
                    email_context = {
                        'title' : 'Recharge Confirmation',
                        'customer_name': request.user.get_full_name(),
                        'voucher': voucher,
                        'amount' : amount,
                        'recipient_email': request.user.email,
                        'template_name': "accounts/account_recharge_done_email.html"
                    }
                    context['success'] = True
                    context['email_context'] = email_context
                    logger.info("Recharge was succefull")
                    return context
                else :
                    context['errors'] = "Voucher could'nt be use"
        return context

    
    