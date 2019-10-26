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
from accounts.models import Account, ServiceCategory, AvailableService, IDCard
from accounts.forms import AccountForm, AccountCreationForm, UserSignUpForm, RechargeForm, UpdateAccountForm, UpdateIDCardForm
from django.forms.models import inlineformset_factory
from django.core.exceptions import PermissionDenied
from pay import settings, utils
from accounts.account_services import AccountService, print_form
from django.urls import reverse_lazy
from django.views.generic.edit import  UpdateView
from payments.models import Transaction
from django.db.models import F, Q
import logging
from pay.tasks import send_mail_task


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
     *current balance
     *transaction history
     *list of available services
     *a list of favoris
    """
    template_name = "accounts/account.html"
    page_title = _('My Account ') + '| ' + settings.SITE_NAME
    #user = User.objects.get(username=request.user.username)
    name = request.user.get_full_name()
    current_account = Account.objects.get(user=request.user)
    current_balance = current_account.balance
    model = AccountService.get_transfer_model()
    activities = model.objects.filter(Q(sender=current_account) | Q(recipient=current_account) )
    active_cat = ServiceCategory.objects.select_related().exclude(available_services__isnull=True)
    available_services = AvailableService.objects.select_related().all()

    context = {
        'name'          : name,
        'page_title'    : page_title,
        'site_name'     : settings.SITE_NAME,
        'balance'       : current_balance,
        'activities'    : activities,
        'active_cats'   : active_cat,
        'account'       : current_account,
        'services'      : available_services,
        'has_idcard'    : False,
        'favorites'     : None
    }
    if hasattr(request.user, 'idcard'):
        context['has_idcard'] = True
    else:
        messages.warning(request, _("You have not identify yourself with an ID card. You will not be able to make transactions."))

    return render(request, template_name, context)

@login_required
def account_details(request, pk=None):
    page_title = _("Account Details") + ' | ' + settings.SITE_NAME
    instance = get_object_or_404(Account, pk=pk)
    template_name = "accounts/account_detail.html"
    #form = AccountForm(request.POST or None, instance=instance)
    context = {
        'page_title':page_title,
        'site_name' : settings.SITE_NAME,
        'template_name':template_name,
        'account': instance
    }
    return render(request,template_name,context )


@login_required
def account_update(request, pk=None):
    
    page_title = _("Edit my account")+ ' | ' + settings.SITE_NAME
    instance = get_object_or_404(Account, pk=pk)
    template_name = "accounts/account_update.html"
    if request.method =="POST":
        form = UpdateAccountForm(request.POST, instance=instance)
        if form.is_valid():
            logger.info("Edit Account form is valid. newsletter : %s", form.cleaned_data['newsletter'])
            form.save()
            messages.success(request, _("You account has been successfuly updated."))
            return redirect('accounts:account')
        else:
            logger.info("Edit Account form is not valid. Errors : %s", form.errors)
            messages.success(request, _("You account could not be updated. Please check the form and try again."))
    
    form = UpdateAccountForm(instance=instance)
    context = {
            'page_title':page_title,
            'site_name' : settings.SITE_NAME,
            'template_name':template_name,
            'account' : instance,
            'balance'     : instance.balance,
            'form': form
        }
    
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
    template_name = "accounts/transaction_done.html"
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
    template_name = "accounts/transaction_detail.html"
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
        current_balance = current_account.balance
        user_transactions = Transaction.objects.filter(Q(sender=current_account) | Q(recipient=current_account) )
        context['balance'] = current_balance
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
                'balance': account.balance,
                'contacts': User.objects.filter(is_staff=False)
            }
    return render(request, template_name, context)

@login_required
def transfer_done(request):
    print("Transfer Done")
    context = {}
    template_name = "accounts/transfer_done.html"
    page_title = "Confirmation" + " - " + settings.SITE_NAME
    context['page_title'] = page_title
    context['site_name'] = settings.SITE_NAME
    return render(request,template_name, context)


@login_required
def transfer_details(request, pk=None):
    context = {}
    model = utils.get_model('payments', 'Transfer')
    user_services = model.objects.filter(Q(sender__user=request.user) | Q(recipient__user=request.user) )
    transfer = get_object_or_404(user_services, pk=pk)
    balance = Account.objects.get(user=request.user).balance
    template_name = "accounts/transfer_detail.html"
    page_title = _("Transfer Details") + " - " + settings.SITE_NAME
    context['page_title'] = page_title
    context['site_name'] = settings.SITE_NAME
    context['transfer'] = transfer
    context['balance'] = balance
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
            messages.success(request, 'We have send you a confirmation E-Mail. You will receive it in an instant')
            send_mail_task.apply_async(args=[context['email_context']],
                queue=settings.CELERY_OUTGOING_MAIL_QUEUE,
                routing_key=settings.CELERY_OUTGOING_MAIL_ROUTING_KEY
            )
            logger.info("Service request successful. Redirecting now to transaction_done")
            return redirect('accounts:transaction_done', redirected_from="service_request")
        else : 
            logger.debug("There was an error with the service request : {}".format(context['errors']))
            form = AccountService.get_service_form()
            service = get_object_or_404(AvailableService, pk=pk)
            context = {
                'page_title':page_title,
                'site_name' : settings.SITE_NAME,
                'service' : service,
                'form': form()
            }

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
    template_name = "accounts/service_detail.html"
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
    template_name = "accounts/service_category_detail.html"
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
    template_name = "accounts/available_service_detail.html"
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
    template_name = "payments/payment_detail.html"
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
    template_name = "accounts/policy_detail.html"
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
    template_name = "accounts/case_detail.html"
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
    template_name = "payments/reduction_detail.html"
    page_title = "Reduction Details - " + settings.SITE_NAME
    context['page_title'] = page_title
    context['site_name'] = settings.SITE_NAME
    context['reduction'] = reduction
    return render(request,template_name, context)


@login_required
def recharge(request):
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
    email_template_name = "accounts/account_recharge_done_email.html"
    template_name = "accounts/recharge.html"
    page_title = "Account Recharge"
    if request.method == "POST":
        context = AccountService.process_recharge_request(request)
        if context['success']:
            messages.success(request, 'Your account has been recharged.We have send you a confirmation E-Mail. You will receive it in an instant')
            send_mail_task.apply_async(args=[context['email_context']],
                queue=settings.CELERY_OUTGOING_MAIL_QUEUE,
                routing_key=settings.CELERY_OUTGOING_MAIL_ROUTING_KEY
            )
            logger.info("Recharge request successful. Redirecting now to user account")
            return redirect('accounts:account')
        else : 
            logger.debug("There was an error with the recharge request : {}".format(context['errors']))
            form = RechargeForm()
            context = {
                'page_title':page_title,
                'site_name' : settings.SITE_NAME,
                'form': form
            }

    elif request.method == "GET":
            form = RechargeForm()
            context = {
                'page_title':page_title,
                'site_name' : settings.SITE_NAME,
                'form': form
            }
    return render(request, template_name, context)

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
    context['has_idcard'] = False
    if hasattr(request.user, 'idcard'):
        context['has_idcard'] = True
        if request.user.idcard.pk == int(pk):
            context['idcard'] = request.user.idcard
        else:
            context['has_idcard'] = False
    template_name = "accounts/idcard_detail.html"
    page_title = "My ID Card - " + settings.SITE_NAME
    context['page_title'] = page_title
    context['site_name'] = settings.SITE_NAME
    return render(request,template_name, context)



@login_required
def upload_idcard(request):
    context = {}
    form = AccountService.get_idcard_form()
    
    template_name = "accounts/upload_idcard.html"
    page_title = "Identification Solution - " + settings.SITE_NAME
    context['page_title'] = page_title
    context['site_name'] = settings.SITE_NAME
    if form().is_multipart():
        logger.info("IDCard Form is multipart")
    else :
        logger.info("IDCard Form is not multipart")

    if request.method == "POST":
        postdata = utils.get_postdata(request)
        
        id_form = form(postdata, request.FILES)
        if id_form.is_valid():
            logger.info("submitted idcard form is valide")
            post_user = int(postdata['user'])
            if post_user == request.user.pk:
                logger.info("saving submitted idcard form")
                id_form.save()
                logger.info("submitted idcard form saved")
                return redirect('accounts:upload_idcard_done')
            else :
                logger.warning("User uploading ID card suspicious : submitted user %s is different than the request user %s ", post_user, request.user.pk )
        else:
            logger.error("The idcard form is not valide. Error : %s", id_form.errors)
    
    context['form'] = form()
    return render(request,template_name, context)


@login_required
def update_idcard(request, pk=None):
    page_title = _("Edit my account")+ ' | ' + settings.SITE_NAME
    instance = get_object_or_404(IDCard, pk=pk)
    template_name = "accounts/account_idcard_update.html"
    if request.method =="POST":
        form = UpdateIDCardForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            logger.info("Update IDCard form is valid")
            form.save()
            return redirect('accounts:account')
        else:
            logger.info("Edit Account form is not valid. Errors : %s", form.errors)
            logger.info("Form clean data : %s", form.cleaned_data)
    
    form = UpdateIDCardForm(instance=instance)
    account = get_object_or_404(Account, user=request.user)
    context = {
            'page_title':page_title,
            'site_name' : settings.SITE_NAME,
            'template_name':template_name,
            'idcard' : instance,
            'balance'     : account.balance,
            'form': form
        }
    
    return render(request, template_name,context )


@login_required
def upload_idcard_done(request):
    context = {}
    template_name = "accounts/upload_idcard_done.html"
    page_title = "ID Card uploaded - " + settings.SITE_NAME
    context['page_title'] = page_title
    context['site_name'] = settings.SITE_NAME
    return render(request,template_name, context)

@login_required
def validate_idcard(request):
    pass






@login_required
def idcards_done(request):
    pass



