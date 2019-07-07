from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as django_login, logout as django_logout
from django.contrib.auth.forms import PasswordChangeForm
from django.db import IntegrityError
from pay import utils, settings
from abc import ABCMeta, ABC
from accounts.forms import  RegistrationForm, AuthenticationForm, AccountForm, UserSignUpForm, AccountCreationForm, ServiceCreationForm
from accounts.models import Account, Policy
from django.db.models import F, Q
from django.apps import apps
from django.forms import modelform_factory
import sys
import logging

logger = logging.getLogger(__name__)

REDIRECT_URL = settings.LOGIN_REDIRECT_URL

this = sys.modules[__name__]
this.TransactionModel = utils.get_model('payments', 'Transaction')
this.TransactionForm = None
this.TransferModel = utils.get_model('payments', 'Transfer')
this.TransferForm = None





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
        return ServiceCreationForm()

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
                this.TransactionForm = modelform_factory(this.TransactionModel, exclude=('created_at','validated_at'))
            except LookupError as e:
                pass
        return this.TransactionModel

    @staticmethod
    def get_transfer_model():
        if this.TransferModel is None:
            try:
                this.TransferModel = apps.get_model('payments', 'Transfer')
                this.TransferForm = modelform_factory(this.TransferModel, exclude=('created_at'))
            except LookupError as e:
                pass
        return this.TransferModel
    
    @staticmethod
    def get_transaction_form():
        if this.TransactionForm is None:
            try:
                this.TransactionModel = AccountService.get_transaction_model()
                this.TransactionForm = modelform_factory(this.TransactionModel, exclude=('created_at','validated_at'))
            except LookupError as e:
                pass
        return this.TransactionForm

    @staticmethod
    def get_transfer_form():
        if this.TransferForm is None:
            try:
                model = AccountService.get_transfer_model()
            except LookupError as e:
                pass
        return this.TransferForm

    @staticmethod
    def process_transaction_request(request, transaction_type = 'T'):
        context = {}
        context['success'] = False
        print("[account_service.py] process_transaction_request entering")
        if this.TransactionModel is None:
            try:
                this.TransactionModel = apps.get_model('payments', 'Transaction')
                this.TransactionForm = modelform_factory(this.TransactionModel, exclude=('created_at','validated_at'))
            except LookupError as e:
                context['errors'] = "Transaction Model not available in the payments APP"
                return context
        

        if request.method == 'POST':
            print("[account_service.py] process_transaction_request entering : POST REQUEST")
            current_account = Account.objects.get(user=request.user)
            current_solde = current_account.solde
            postdata = utils.get_postdata(request)
            transaction_form = this.TransactionForm(postdata)
            if transaction_form.is_valid():
                print("[account_service.py] process_transaction_request entering : Transaction Form is Valid")
                recipient = postdata['recipient']
                amount = int(postdata['amount'])
                if(current_solde >=  amount):
                    recipient_exist = Account.objects.filter(user_email=recipient).exists()
                    if recipient_exist:
                        Account.objects.all().filter(user_email=recipient).update(solde=F('solde') + amount)
                        Account.objects.all().filter(pk=current_account.pk).update(solde=F('solde') - amount)
                        transaction_form.save()
                        context['success'] = True
                        context['solde'] = current_account - amount
                    else:
                        context['errors'] = "The recipient could not be found."
                        print("[account_service.py]There was an error with the transaction request : ")
                        print(context['errors'])
                        return context
                    
                else :
                    context['success'] = False
                    context['solde'] = current_account
                    context['errors'] = "Vous n'avez pas assez d'argent dans votre compte"
                    return context
        else:
            context['solde'] = current_account
            context['errors'] = "Verifiez les champs du formulaire."
        return context


    @staticmethod
    def process_transfer_request(request):
        context = {}
        context['success'] = False
        ("[account_service.py] process_transaction_request entering")
        model = AccountService.get_transfer_model()
        form = AccountService.get_transfer_form()
        

        if request.method == 'POST':
            logger.info("processing new transfer request : POST REQUEST")
            current_account = Account.objects.get(user=request.user)
            current_solde = current_account.solde
            postdata = utils.get_postdata(request)
            transfer_form = form(postdata)
            if transfer_form.is_valid():
                logger.info(" Transfer Form is Valid")
                recipient = postdata['recipient']
                amount = int(postdata['amount'])
                if(current_solde >=  amount):
                    recipient_exist = Account.objects.filter(user_email=recipient).exists()
                    if recipient_exist:
                        Account.objects.all().filter(user_email=recipient).update(solde=F('solde') + amount)
                        Account.objects.all().filter(pk=current_account.pk).update(solde=F('solde') - amount)
                        transfer_form.save()
                        context['success'] = True
                        context['solde'] = current_account - amount
                        logger.info("Transfer was succefull")
                    else:
                        context['errors'] = "The recipient could not be found."
                        logger.error("There was an error with the transfer request : %s", context['errors'])
                        
                        return context
                    
                else :
                    context['success'] = False
                    context['solde'] = current_account
                    context['errors'] = "Vous n'avez pas assez d'argent dans votre compte"
                    return context
        else:
            context['solde'] = current_account
            context['errors'] = "Verifiez les champs du formulaire."
        return context

    @staticmethod
    def process_service_request(request, service=None):
        pass


    @staticmethod
    def checkFromAvailability(form=None):
        logger.info("Checking Form availability")
        logger.info("Checking TransactionForm :")
        print_form(AccountService.get_transaction_form())
        logger.info("Checking TransferForm :")
        print_form(AccountService.get_transfer_form())
        logger.info("Checking passed parameter Form :")
        print_form(form)

