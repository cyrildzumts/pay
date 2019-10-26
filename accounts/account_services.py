from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as django_login, logout as django_logout
from django.contrib.auth.forms import PasswordChangeForm
from django.db import IntegrityError
from pay import utils, settings
from abc import ABCMeta, ABC
from accounts.forms import  RegistrationForm, AuthenticationForm, AccountForm, UserSignUpForm, AccountCreationForm, ServiceCreationForm, IDCardForm, RechargeForm
from accounts.models import Account, Policy
from django.db.models import F, Q
from django.apps import apps
from django.forms import modelform_factory
from voucher import voucher_service
import sys
import logging
import numbers

logger = logging.getLogger(__name__)

REDIRECT_URL = settings.LOGIN_REDIRECT_URL

this = sys.modules[__name__]
this.TransactionModel = utils.get_model('payments', 'Transaction')
this.TransactionForm = None
this.TransferModel = utils.get_model('payments', 'Transfer')
this.TransferForm = None
this.ServiceForm = ServiceCreationForm





def get_all_fields_from_form(instance):
    """"
    Return names of all available fields from given Form instance.

    :arg instance: Form instance
    :returns list of field names
    :rtype: list
    """

    fields = list(instance().base_fields)

    for field in list(instance().declared_fields):
        if field not in fields:
            fields.append(field)
    return fields

def print_form(form=None):
    print("Printing  Form Fields")
    if form :
        print(get_all_fields_from_form(form))
    else :
        print("form is not defined")




class AccountService(ABC):
    """
    This class exists only to avoid that the accounts.views directly manipulate the models it is working with.
    That way the Service can be changed without affecting the views.
    The job of this AccountService is to provide access to the database related to the Account operations.
    It provides differents utilities functions to obtains Forms, log user in, to create a new user account, 
    to create a new policy. 
    New bussiness services will be added to the class instead of updating the views.
    """

    @staticmethod
    def get_authentication_form(initial_content=False):
        return AuthenticationForm()
    
    @staticmethod
    def get_registration_form():
        return RegistrationForm()
    
    @staticmethod
    def get_service_form():
        return ServiceCreationForm

    @staticmethod
    def get_idcard_form():
        return IDCardForm

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
    def process_change_password_request(request):
        result_dict = {}
        result_dict['changed'] = False
        
        postdata = utils.get_postdata(request)
        form = PasswordChangeForm(request.user, postdata)
        if form.is_valid():
            user = form.save()
            result_dict['changed'] = True
            result_dict['next_url'] = 'accounts:password_change'
        return result_dict
        

    @staticmethod
    def process_login_request(request):
        result_dict = {}
        result_dict['user_logged'] = False
        result_dict['next_url'] = REDIRECT_URL
        postdata = utils.get_postdata(request)
        form = AuthenticationForm(data=postdata)
        username = postdata['username']
        password = postdata['password']
        logger.info("[AccountService.process_login_request] : starting")
        if form.is_valid():
            logger.debug("[AccountService.process_login_request] : form is valid Username : {} - Password : {}".format(username,password))
            user = auth.authenticate(username=username,
                                    password=password)
            logger.debug("[AccountService.process_login_request] : user authentication")
            if user is not None:
                if user.is_active:
                    auth.login(request, user)
                    logger.debug("[AccountService.process_login_request] : user is authenticated")
                    result_dict['user_logged'] = True
                
        logger.debug("[AccountService.process_login_request] : finished")
        return result_dict
    

    @staticmethod
    def process_registration_request(request):
        """
        The form used to fill the data provide data for both the UserSignUpForm and the AccountCreationForm.
        From the data it is possible process many form at the same times just like this code is doing.
        """
        result_dict = {}
        result_dict['user_created'] = False
        result_dict['next_url'] = REDIRECT_URL
        postdata = utils.get_postdata(request)
        #form = RegistrationForm(data=postdata)
        user_form = UserSignUpForm(postdata)
        account_form = AccountCreationForm(postdata)
        print_form(postdata)
        if user_form.is_valid() and account_form.is_valid():
            logger.info("User creation data is valid")
            user = user_form.save()
            user.refresh_from_db()
            account_form = AccountCreationForm(postdata, instance=user.account)
            account_form.full_clean()
            account_form.save()
            logger.info("User creation succesfull")
            result_dict['user_created'] = True

        return result_dict



    @staticmethod
    def create_account(accountdata=None, userdata=None):
        created = False
        if accountdata and userdata:
            try:
                user = User.objects.create(**userdata)
                user.refresh_from_db()
                # creating a new user will trigger a signal that will automatically create a new account the new user.
                # So instead of creating a new account , update the already created account associated to the new user.
                if user: 
                    Account.objects.filter(user=user).update(**accountdata)
                    created = True
            
            except IntegrityError:
                pass

        return created


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


    @staticmethod
    def get_transaction_model():
        if this.TransactionModel is None:
            try:
                this.TransactionModel = apps.get_model('payments', 'Transaction')
                this.TransactionForm = modelform_factory(this.TransactionModel, exclude=['created_at','validated_at'])
            except LookupError as e:
                pass
        return this.TransactionModel

    @staticmethod
    def get_transfer_model():
        print("[get_transfer_model ]: Entered")
        if this.TransferModel is None:
            print("[get_transfer_model ]: TransferModel None")
            try:
                this.TransferModel = apps.get_model('payments', 'Transfer')
                this.TransferForm = modelform_factory(this.TransferModel, exclude=['created_at'])
                if this.TransferModel is None:
                    print("[get_transfer_model ]: TransferModel still None")

                if this.TransferForm is None:
                    print("[get_transfer_model ]: TransferForm still None")
            except LookupError as e:
                pass
        return this.TransferModel
    
    @staticmethod
    def get_transaction_form():
        if this.TransactionForm is None:
            try:
                this.TransactionModel = AccountService.get_transaction_model()
                this.TransactionForm = modelform_factory(this.TransactionModel, exclude=['created_at','validated_at'])
            except LookupError as e:
                pass
        return this.TransactionForm

    @staticmethod
    def get_transfer_form():
        print("[get_transfer_form ]: Entered")
        if this.TransferForm is None:
            print("[get_transfer_form ]: TransferForm is none")
            try:
                model = AccountService.get_transfer_model()
                if this.TransferForm is None:
                    print("[get_transfer_form]: TransferForm still None")
                    this.TransferForm = modelform_factory(model, exclude=['created_at'])
                else:
                    print("[get_transfer_form]: TransferForm is Available")
            except LookupError as e:
                print("[get_transfer_form] Exception LookupError : {}".format(e))
        return this.TransferForm

    @staticmethod
    def process_transaction_request(request, transaction_type = 'T'):
        context = {}
        context['success'] = False
        print("[account_service.py] process_transaction_request entering")
        if this.TransactionModel is None:
            try:
                this.TransactionModel = apps.get_model('payments', 'Transaction')
                this.TransactionForm = modelform_factory(this.TransactionModel, exclude=['created_at','validated_at'])
            except LookupError as e:
                context['errors'] = "Transaction Model not available in the payments APP"
                return context
        

        if request.method == 'POST':
            print("[account_service.py] process_transaction_request entering : POST REQUEST")
            current_account = Account.objects.get(user=request.user)
            current_balance = current_account.balance
            postdata = utils.get_postdata(request)
            transaction_form = this.TransactionForm(postdata)
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
                        print("[account_service.py]There was an error with the transaction request : ")
                        print(context['errors'])
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
        model = AccountService.get_transfer_model()
        form = AccountService.get_transfer_form()
        

        if request.method == 'POST':
            logger.info("processing new transfer request : POST REQUEST")
            current_account = Account.objects.get(user=request.user)
            current_balance = current_account.balance
            postdata = utils.get_postdata(request)
            transfer_form = form(postdata)
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
        form = AccountService.get_service_form()
        

        if request.method == 'POST':
            logger.info("processing new service request : POST REQUEST")
            postdata = utils.get_postdata(request)
            postdata.setdefault('commission', 0.03)
            service_form = form(postdata)
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
                        pay_fee, operator_amount, succeed = AccountService.get_commission(price,commission)
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
                print("Form is Invalid : See the errors fields below")
                print(service_form.errors)
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


    @staticmethod
    def checkFromAvailability(form=None):
        logger.info("Checking Form availability")
        logger.info("Checking TransactionForm :")
        print_form(AccountService.get_transaction_form())
        logger.info("Checking TransferForm :")
        print_form(AccountService.get_transfer_form())
        logger.info("Checking passed parameter Form :")
        print_form(form)

