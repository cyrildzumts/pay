from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
#from django.core import urlresolvers
from django.http import HttpResponseRedirect, JsonResponse, HttpResponseForbidden
from django.contrib import auth, messages
from django.template import RequestContext
from django.utils.translation import gettext as _
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm
from django.contrib.auth import login as django_login, logout as django_logout, update_session_auth_hash
from accounts.models import Account, ServiceCategory, AvailableService
from accounts.forms import AccountForm, AccountCreationForm, UserSignUpForm
from django.forms.models import inlineformset_factory
from django.core.exceptions import PermissionDenied
from pay import settings, utils
from accounts.account_services import AccountService, print_form
from django.urls import reverse_lazy
from django.views.generic.edit import  UpdateView
from payments.models import Transaction
from django.db.models import F, Q
import logging


logger = logging.getLogger(__name__)

# Create your views here.

# GLOBAL Redirect url variable
REDIRECT_URL = settings.LOGIN_REDIRECT_URL

# Create your views here.
def login(request):
    """
    Log in view
    """
    page_title = _("Login") + ' | ' + settings.SITE_NAME
    template_name = 'accounts/registration/login.html'

    # template_name = 'tags/login_form.html'
    if request.method == 'POST':
        result = AccountService.process_login_request(request)
        if result['user_logged']:
            logger.info("New user logged in.")
            return redirect(result['next_url'])
    
    form = AccountService.get_authentication_form()
    register_form = AccountService.get_registration_form()
    
    context = {
        
        'page_title':page_title,
        'template_name':template_name,
        'form': form,
        'registration_form': register_form,
    }
    return render(request, template_name, context)


def logout(request):
    """
    Log out view
    """
    auth.logout(request)
    return redirect(REDIRECT_URL)


def register(request):
    """
    User registration view
    """
    template_name = "accounts/registration/register.html"
    page_title = _('Registration') +' | ' + settings.SITE_NAME
    if request.method == 'POST':
        result = AccountService.process_registration_request(request)
        if result['user_created']:
            return HttpResponseRedirect(result['next_url'])
        else:
            #form = AccountService.get_registration_form()
            account_form = AccountCreationForm()
            user_form = UserSignUpForm()

    else:
        # form = UserCreationForm()
        #form = AccountService.get_registration_form()
        account_form = AccountCreationForm()
        user_form = UserSignUpForm()
    context = {
        'page_title': page_title,
        'template_name': template_name,
        #'form': form,
        'account_form' : account_form,
        'user_form': user_form
    }
    return render(request, template_name, context)

@login_required
def password_change_views(request):
    """ 
        This view is called when the user want to change its password
    """
    page_title = 'Modification de  mot de passe | ' + settings.SITE_NAME
    template_name = "accounts/registration/password_change.html"
    success_url = 'accounts:password_change_done'
    if request.method == 'POST':
        postdata = utils.get_postdata(request)
        form = PasswordChangeForm(request.user, postdata)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Votre mot de passe a été changé!")
            context = {
                'changed' : True,
                'redirect_to': success_url
            }
            return redirect(success_url)
        else:
            messages.error(request, 'Veuillez corriger les erreurs indiquées.')
    else:
        form = PasswordChangeForm(request.user)
    
    context = {
        'page_title': page_title,
        'form' : form
    }
    return render(request, template_name, context)
    

def password_change_done_views(request):
    """ 
        This view is called when the user has changed its password
    """
    template_name = "accounts/registration/password_change_done.html"
    page_title = 'Confirmation | ' + settings.SITE_NAME
    
    context = {
        'page_title': page_title,
        'template_name': template_name
    }
    return render(request, template_name, context)



def password_reset_views(request):
    """ 
        This view is called when the user want to reset her password
    """
    template_name = "accounts/registration/password_reset_form.html"
    email_template_name = "registration/password_reset_email.html"
    page_title = 'Remise à zéro du mot de passe | ' + settings.SITE_NAME

    
    context = {
        'page_title': page_title,
        'template_name': template_name
    }
    return render(request, template_name, context)

#@login_required
def user_account(request):
    """
     This method serves the default user account page.
     This page display an overview of the user's orders,
     user's infos ...  So this method have to provide these
     informations to the template.
     This view must provide a context providing the following informations :
     *current solde
     *transaction history
     *list of available services
     *a list of favoris
    """
    template_name = "accounts/account.html"
    page_title = _('My Account ') + '| ' + settings.SITE_NAME
    #user = User.objects.get(username=request.user.username)
    name = request.user.get_full_name()
    current_account = Account.objects.get(user=request.user)
    current_solde = current_account.solde
    model = AccountService.get_transfer_model()
    activities = model.objects.filter(Q(sender=current_account) | Q(recipient=current_account) )
    active_cat = ServiceCategory.objects.select_related().exclude(available_services__isnull=True)
    available_services = AvailableService.objects.select_related().all()
    context = {
        'name'          : name,
        'page_title'    : page_title,
        'site_name'     : settings.SITE_NAME,
        'solde'         : current_solde,
        'activities'    : activities,
        'active_cats'   : active_cat,
        'account'       : current_account,
        'services': available_services,
        'favorites': None
    }
    return render(request, template_name, context)


def account_details(request, pk=None):
    page_title = _("Account Details") + ' | ' + settings.SITE_NAME
    instance = get_object_or_404(Account, pk=pk)
    template_name = "accounts/account_details.html"
    #form = AccountForm(request.POST or None, instance=instance)
    context = {
        'page_title':page_title,
        'site_name' : settings.SITE_NAME,
        'template_name':template_name,
        'account': instance
    }
    return render(request,template_name,context )


@login_required
def edit_account(request, pk=None):
    page_title = _("Edit my account")+ ' | ' + settings.SITE_NAME
    instance = Account.objects.get(pk=pk)
    template_name = "accounts/edit_account.html"
    form = AccountForm(request.POST or None, instance=instance)
    context = {
        'page_title':page_title,
        'site_name' : settings.SITE_NAME,
        'template_name':template_name,
        'form': form
    }
    if form.is_valid():
        form.save()
        return redirect('next_view')
    return render(request, template_name,context )

@login_required
def transactions(request):
    context = {}
    model = utils.get_model(app_name='payments', modelName='Transaction')
    current_account = Account.objects.get(user=request.user)
    user_transactions = model.objects.filter(Q(sender=current_account) | Q(recipient=current_account) )
    template_name = "accounts/transaction_list.html"
    page_title = _("Your Transactions") + " - " + settings.SITE_NAME
    context['page_title'] = page_title
    context['site_name'] = settings.SITE_NAME
    context['transactions'] = user_transactions
    logger.debug("%s requested transactions list", current_account.full_name())
    return render(request,template_name, context)



@login_required
def new_transaction(request):
    """
    This view is responsible for processing transactions.
    To process a transaction : 
    The user must provide the following informations :
        * recipient ID
        * the amount of money to send
        * the type of transaction : TRANSFER, INVOICE PAYMENT, SERVICE CONSUMER
    For TRANSFER no more information data are needed.
    For INVOICE PAYMENT, the following extra informations are needed :
        * Invoice Reference Number
        * Invoice Date
        * Customer ID of as used by the recipient
    For SERVICE CONSUMER, the following extra informations are needed :
        The needed information are dependent of the type of service.
        A service REF ID is needed to identify the actual data needed.
    """
    context = {}
    email_template_name = "accounts/transaction_done_email.html"
    template_name = "accounts/new_transaction.html"
    page_title = _("New Transaction")
    logger.debug("New transaction request incoming")
    if request.method == "POST":
        context = AccountService.process_transaction_request(request=request)
        if context['success']:
            redirect('accounts:transaction_done')
        else : 
            logger.debug("There was an error with the transaction request : %s", context['errors'])

    elif request.method == "GET":
        form = AccountService.get_transaction_form()
        print_form(form)
        if form is None:
            logger.error("Transaction Form is not Valide")
        context = {
                'page_title': page_title,
                'site_name' : settings.SITE_NAME,
                'form': form
        }
    return render(request, template_name, context)


def transaction_done(request, redirected_from = None):
    if redirected_from is None:
        return HttpResponseForbidden()
    
    context = {}
    template_name = "accounts/transactions_done.html"
    page_title = "Transaction effectué - " + settings.SITE_NAME
    context['page_title'] = page_title
    context['site_name'] = settings.SITE_NAME
    return render(request,template_name, context)


@login_required
def transaction_details(request, pk=None):

    context = {}
    model = utils.get_model(app_name='payments', modelName='Transaction')
    current_account = Account.objects.get(user=request.user)
    user_transactions = model.objects.filter(Q(sender=current_account) | Q(recipient=current_account) )
    transaction = get_object_or_404(user_transactions, pk=pk)
    template_name = "accounts/transaction_details.html"
    page_title = _("Transaction Details") + " - " + settings.SITE_NAME
    context['page_title'] = page_title
    context['site_name'] = settings.SITE_NAME
    context['transaction'] = transaction
    return render(request,template_name, context)


@login_required
def api_get_transactions(request, pk=None):
    context = {}
    if request.is_ajax:
        current_account = Account.objects.get(user=request.user)
        current_solde = current_account.solde
        user_transactions = Transaction.objects.filter(Q(sender=current_account) | Q(recipient=current_account) )
        context['solde'] = current_solde
        context['transactions'] = user_transactions
    return JsonResponse(context)


@login_required
def transfers(request):
    pass

@login_required
def new_transfer(request):
    """
    This view is responsible for processing a service.
    To process a transaction : 
    The user must provide the following informations :
        * recipient ID
        * the amount of money to send
        * the type of transaction : TRANSFER, INVOICE PAYMENT, SERVICE CONSUMER
    For TRANSFER no more information data are needed.
    
    """
    context = {}
    email_template_name = "accounts/transfer_done_email.html"
    template_name = "accounts/new_transfer.html"
    page_title = _("New Transfer") + " - " + settings.SITE_NAME
    account = Account.objects.get(user=request.user)
    
    if request.method == "POST":
        context = AccountService.process_transfer_request(request)
        if context['success']:
            return redirect('accounts:transfer_done')
        else : 
            logger.error("There was an error with the transfer request : %s", context['errors'])

    elif request.method == "GET":
            form = AccountService.get_transfer_form()
            AccountService.checkFromAvailability(form=form)
            context = {
                'page_title':page_title,
                'site_name' : settings.SITE_NAME,
                'form': form,
                'solde': account.solde,
                'contacts': User.objects.filter(is_staff=False)
            }
    return render(request, template_name, context)

@login_required
def transfer_done(request):
    print("Transfer Done")
    context = {}
    template_name = "accounts/transfer_done.html"
    page_title = _("Confirmation") + " - " + settings.SITE_NAME
    context['page_title'] = page_title
    context['site_name'] = settings.SITE_NAME
    return render(request,template_name, context)


@login_required
def transfer_details(request, pk=None):
    context = {}
    model = utils.get_model('payments', 'Transfer')
    user_services = model.objects.filter(Q(sender__user=request.user) | Q(recipient__user=request.user) )
    transfer = get_object_or_404(user_services, pk=pk)
    solde = Account.objects.get(user=request.user).solde
    template_name = "accounts/transfer_details.html"
    page_title = _("Transfer Details") + " - " + settings.SITE_NAME
    context['page_title'] = page_title
    context['site_name'] = settings.SITE_NAME
    context['transfer'] = transfer
    context['solde'] = solde
    return render(request,template_name, context)

@login_required
def services(request):
    context = {}
    model = utils.get_model('accounts', 'Service')
    services = model.objects.select_related('category').filter(customer=request.user)
    template_name = "accounts/service_list.html"
    page_title = _("Services") + " - " + settings.SITE_NAME
    context['page_title'] = page_title
    context['site_name'] = settings.SITE_NAME
    context['services'] = services
    return render(request,template_name, context)


@login_required
def new_service(request, pk=None):
    '''
    This view is responsible for processing a service.
    To process a transaction : 
    The user must provide the following informations :
        * recipient ID
        * the amount of money to send
        * the type of transaction : TRANSFER, INVOICE PAYMENT, SERVICE CONSUMER
    For TRANSFER no more information data are needed.
    For INVOICE PAYMENT, the following extra informations are needed :
        * Invoice Reference Number
        * Invoice Date
        * Customer ID of as used by the recipient
    For SERVICE CONSUMER, the following extra informations are needed :
        The needed information are dependent of the type of service.
        A service REF ID is needed to identify the actual data needed.
    '''
    context = {}
    email_template_name = "accounts/service_done_email.html"
    template_name = "accounts/new_service.html"
    page_title = "Service Usage"
    if request.method == "POST":
        context = AccountService.process_service_request(request, service_pk=pk)
        if context['success']:
            return redirect('accounts:transaction_done')
        else : 
            logger.debug("There was an error with the service request : {}".format(context['errors']))

    elif request.method == "GET":
            form = AccountService.get_service_form()
            service = get_object_or_404(AvailableService, pk=pk)
            context = {
                'page_title':page_title,
                'site_name' : settings.SITE_NAME,
                'service' : service,
                'form': form()
            }
    return render(request, template_name, context)


@login_required
def service_done(request):
    pass

@login_required
def service_details(request, pk=None):
    context = {}
    model = utils.get_model('accounts', 'Service')
    user_services = model.objects.filter(Q(operator=request.user) | Q(customer=request.user) )
    service = get_object_or_404(user_services, pk=pk)
    template_name = "accounts/service_details.html"
    page_title = "Service Details - " + settings.SITE_NAME
    context['page_title'] = page_title
    context['site_name'] = settings.SITE_NAME
    context['service'] = service
    return render(request,template_name, context)


@login_required
def service_categories(request):
    context = {}
    model = utils.get_model('accounts', 'ServiceCategory')
    categories = model.objects.filter(is_active=True)
    template_name = "accounts/service_category_list.html"
    page_title = "Service Categories - " + settings.SITE_NAME
    context['page_title'] = page_title
    context['site_name'] = settings.SITE_NAME
    context['categories'] = categories
    return render(request,template_name, context)


@login_required
def service_category_details(request, pk=None):
    context = {}
    model = utils.get_model('accounts', 'ServiceCategory')
    category = get_object_or_404(model, pk=pk)
    template_name = "accounts/service_category_details.html"
    page_title = "Service Category Details - " + settings.SITE_NAME
    context['page_title'] = page_title
    context['site_name'] = settings.SITE_NAME
    context['category'] = category
    return render(request,template_name, context)

@login_required
def available_services(request):
    context = {}
    model = utils.get_model('accounts', 'AvailableService')
    available_services = model.objects.all()
    template_name = "accounts/available_service_list.html"
    page_title = "Available Services - " + settings.SITE_NAME
    context['page_title'] = page_title
    context['site_name'] = settings.SITE_NAME
    context['available_services'] = available_services
    return render(request,template_name, context)


@login_required
def available_service_details(request, pk=None):
    context = {}
    model = utils.get_model('accounts', 'AvailableService')
    service= get_object_or_404(model, pk=pk)
    template_name = "accounts/available_service_details.html"
    page_title = "Available Service Details - " + settings.SITE_NAME
    context['page_title'] = page_title
    context['site_name'] = settings.SITE_NAME
    context['service'] = service
    return render(request,template_name, context)


@login_required
def new_payment(request):
    pass

@login_required
def payment_done(request):
    pass

@login_required
def payments(request):
    context = {}
    model = utils.get_model(app_name='payments', modelName='Payment')
    current_account = Account.objects.get(user=request.user)
    user_payments = model.objects.filter(Q(sender=current_account) | Q(recipient=current_account) )
    template_name = "payments/payment_list.html"
    page_title = "Payments - " + settings.SITE_NAME
    context['page_title'] = page_title
    context['site_name'] = settings.SITE_NAME
    context['payments'] = user_payments
    return render(request,template_name, context)


@login_required
def payment_details(request, pk=None):
    context = {}
    model = utils.get_model(app_name='payments', modelName='Payment')
    current_account = Account.objects.get(user=request.user)
    user_payments = model.objects.filter(Q(sender=current_account) | Q(recipient=current_account) )
    payment = get_object_or_404(user_payments, pk=pk)
    template_name = "payments/payment_details.html"
    page_title = "Payment Details - " + settings.SITE_NAME
    context['page_title'] = page_title
    context['site_name'] = settings.SITE_NAME
    context['payment'] = payment
    return render(request,template_name, context)


@login_required
def policies(request):
    context = {}
    model = utils.get_model(app_name='accounts', modelName='Policy')
    #current_account = Account.objects.get(user=request.user)
    current_policies = model.objects.all()
    template_name = "accounts/policy_list.html"
    page_title = "Policies - " + settings.SITE_NAME
    context['page_title'] = page_title
    context['site_name'] = settings.SITE_NAME
    context['policies'] = current_policies
    return render(request,template_name, context)


@login_required
def policy_details(request, pk=None):
    context = {}
    model = utils.get_model(app_name='accounts', modelName='Policy')
    #current_account = Account.objects.get(user=request.user)
    policy = get_object_or_404(model, pk=pk)
    template_name = "accounts/policy_details.html"
    page_title = "Policy Details - " + settings.SITE_NAME
    context['page_title'] = page_title
    context['site_name'] = settings.SITE_NAME
    context['policy'] = policy
    return render(request,template_name, context)

@login_required
def cases(request):
    context = {}
    model = utils.get_model(app_name='payments', modelName='CaseIssue')
    current_account = Account.objects.get(user=request.user)
    user_claims = model.objects.filter(Q(sender=current_account) | Q(recipient=current_account) )
    template_name = "accounts/case_list.html"
    page_title = "Claims - " + settings.SITE_NAME
    context['page_title'] = page_title
    context['site_name'] = settings.SITE_NAME
    context['claims'] = user_claims
    return render(request,template_name, context)

@login_required
def case_details(request, pk=None):
    context = {}
    model = utils.get_model(app_name='payments', modelName='CaseIssue')
    current_account = Account.objects.get(user=request.user)
    user_claims = model.objects.filter(Q(sender=current_account) | Q(recipient=current_account) )
    claim = get_object_or_404(user_claims, pk=pk)
    template_name = "accounts/policy_details.html"
    page_title = "Claim Details - " + settings.SITE_NAME
    context['page_title'] = page_title
    context['site_name'] = settings.SITE_NAME
    context['claim'] = claim
    return render(request,template_name, context)

@login_required
def reductions(request):
    context = {}
    model = utils.get_model(app_name='payments', modelName='Reduction')
    #current_account = Account.objects.get(user=request.user)
    current_reductions = model.objects.all()
    template_name = "payment/reduction_list.html"
    page_title = "Reductions - " + settings.SITE_NAME
    context['page_title'] = page_title
    context['site_name'] = settings.SITE_NAME
    context['reductions'] = current_reductions
    return render(request,template_name, context)


@login_required
def reduction_details(request, pk=None):
    context = {}
    model = utils.get_model(app_name='payments', modelName='Reduction')
    #current_account = Account.objects.get(user=request.user)
    reduction = get_object_or_404(model, pk=pk)
    template_name = "payments/reduction_details.html"
    page_title = "Reduction Details - " + settings.SITE_NAME
    context['page_title'] = page_title
    context['site_name'] = settings.SITE_NAME
    context['reduction'] = reduction
    return render(request,template_name, context)


@login_required
def idcards(request):
    context = {}
    model = utils.get_model(app_name='accounts', modelName='IDCard')
    #current_account = Account.objects.get(user=request.user)
    current_idcards = model.objects.filter(user=request.user)
    template_name = "accounts/idcard_list.html"
    page_title = "ID Cards - " + settings.SITE_NAME
    context['page_title'] = page_title
    context['site_name'] = settings.SITE_NAME
    context['idcards'] = current_idcards
    return render(request,template_name, context)


@login_required
def idcard_details(request, pk=None):
    context = {}
    model = utils.get_model(app_name='accounts', modelName='IDCard')
    user_idcards = model.objects.filter(user=request.user)
    idcard = get_object_or_404(user_idcards, pk=pk)
    template_name = "accounts/idcard_details.html"
    page_title = "ID Card Details - " + settings.SITE_NAME
    context['page_title'] = page_title
    context['site_name'] = settings.SITE_NAME
    context['idcard'] = idcard
    return render(request,template_name, context)


@login_required
def idcards_done(request):
    pass