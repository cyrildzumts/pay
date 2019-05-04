from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
#from django.core import urlresolvers
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib import auth, messages
from django.template import RequestContext
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm
from django.contrib.auth import login as django_login, logout as django_logout, update_session_auth_hash
from accounts.models import Account
from accounts.forms import AccountForm, AccountCreationForm, UserSignUpForm
from django.forms.models import inlineformset_factory
from django.core.exceptions import PermissionDenied
from pay import settings, utils
from accounts.account_services import AccountService
from django.urls import reverse_lazy
from django.views.generic.edit import  UpdateView
from payments.models import Transaction
from django.db.models import F, Q

# Create your views here.

# GLOBAL Redirect url variable
REDIRECT_URL = settings.LOGIN_REDIRECT_URL

# Create your views here.
def login(request):
    """
    Log in view
    """
    page_title = "Connexion d'utilisateur"
    template_name = 'accounts/registration/login.html'
    
    # template_name = 'tags/login_form.html'
    if request.method == 'POST':
        result = AccountService.process_login_request(request)
        if result['user_logged']:
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
    page_title = 'Creation de compte | ' + settings.SITE_NAME
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
    template_name = "registration/password_change.html"
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
    template_name = "registration/password_change_done.html"
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
    page_title = 'Mon Compte | ' + settings.SITE_NAME
    #user = User.objects.get(username=request.user.username)
    if request.user.is_authenticated:
        name = request.user.get_full_name()
        current_account = Account.objects.get(user=request.user)
        current_solde = current_account.solde
        user_transactions = Transaction.objects.filter(Q(sender=current_account) | Q(recipient=current_account) )
        context = {
        'name'      : name,
        'page_title':page_title,
        'site_name' : settings.SITE_NAME,
        'solde'     : current_solde,
        'transactions' : user_transactions
    }
    else:
        context = {
        'name'      : "AnonymUser",
        'page_title':page_title,
        'site_name' : settings.SITE_NAME,
        'transactions' : None
    }

    
    return render(request, template_name, context)




@login_required
def edit_account(request, pk=None):
    page_title = "Modifier mon compte"
    instance = Account.objects.get(pk)
    template_name = "tags/edit_accoutn.html"
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
    if request.method == 'POST':
        current_account = Account.objects.get(user=request.user)
        current_solde = current_account.solde
        postdata = utils.get_postdata(request)
        transaction_form = Transaction(data=postdata)
        if transaction_form.is_valid():
            recipient_name = postdata['recipient']
            amount = int(postdata['amount'])
            if(current_solde >=  amount):
                Account.objects.all().filter(user_name=recipient_name).update(solde=F('solde') + amount)
                Account.objects.all().filter(user=request.user).update(solde=F('solde') - amount)
                transaction_form.save()
                context['success'] = 1
                context['solde'] = current_account - amount
                
            else :
                context['success'] = 0
                context['solde'] = current_account
                context['errors'] = "Vous n'avez pas assez d'argent dans votre compte"
        else:
            context['success'] = 0
            context['solde'] = current_account
            context['errors'] = "Verifiez les champs du formulaire."


    return JsonResponse(context)

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
def services(request):
    pass