from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
#from django.core import urlresolvers
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.template import RequestContext
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as django_login, logout as django_logout
from accounts.models import Account
from accounts.forms import AccountForm
from django.forms.models import inlineformset_factory
from django.core.exceptions import PermissionDenied
from pay import settings
from accounts.account_services import AccountService
from django.urls import reverse_lazy
from django.views.generic.edit import  UpdateView

# Create your views here.

# GLOBAL Redirect url variable
REDIRECT_URL = settings.LOGIN_REDIRECT_URL

# Create your views here.
def login(request):
    """
    Log in view
    """
    page_title = "Connexion d'utilisateur"
    template_name = 'registration/login.html'
    
    # template_name = 'tags/login_form.html'
    if request.method == 'POST':
        result = AccountService.process_login_request(request)
        if result['user_logged']:
            return redirect(result['next_url'])
    else:
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
    template_name = "registration/register.html"
    page_title = 'Creation de compte | ' + settings.SITE_NAME
    if request.method == 'POST':
        result = AccountService.process_registration_request(request)
        if result['user_logged']:
            return result['next_url']

    else:
        # form = UserCreationForm()
        form = AccountService.get_registration_form()
    context = {
        'page_title': page_title,
        'template_name': template_name,
        'form': form,
    }
    return render(request, template_name, context)


@login_required
def user_account(request):
    """
     This method serves the default user account page.
     This page display an overview of the user's orders,
     user's infos ...  So this method have to provide these
     informations to the template.
    """
    template_name = "accounts/account.html"
    page_title = 'Mon Compte | ' + settings.SITE_NAME
    #user = User.objects.get(username=request.user.username)
    name = 'Cyrille Ngassam Nkwenga'
    #orders = user.order_set.order_by('-date').exclude(status=Order.FINISHED)[:2]
    context = {
        'name'      : name,
        'page_title':page_title,
        'template_name':template_name,
    }
    return render(request, template_name, context)


@login_required
def edit_account(request, pk):
    '''
    template_name = "accounts/my-account.html"
    page_title = 'Modification du profile | ' + settings.SITE_NAME
    user = User.objects.get(pk=pk)
    user = request.user
    user_form = UserForm(instance=user)
    ProfileInlineFormSet = inlineformset_factory(User,
                                                 UserProfile,
                                                 fields=('country', 'city',
                                                         'province', 'address',
                                                         'zip_code', 'telefon',
                                                         'newsletter',
                                                         'is_active_account'))
    formset = ProfileInlineFormSet(instance=user)
    if request.method == "POST":
        user_form = UserForm(request.POST, request.FILES, instance=user)
        formset = ProfileInlineFormSet(request.POST, request.FILES, instance=user)

        if user_form.is_valid():
            created_user = user_form.save(commit=False)
            formset = ProfileInlineFormSet(request.POST, request.FILES, instance=created_user)

            if formset.is_valid():
                created_user.save()
                formset.save()
                return HttpResponseRedirect(REDIRECT_URL)

    name = request.user.username
    return render(request, template_name, locals())
    '''
    pass