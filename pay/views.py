from django.shortcuts import render, HttpResponseRedirect
from django.contrib import auth
# from django import forms
from django.contrib.auth.forms import UserCreationForm
from pay import settings
import logging

logger = logging.getLogger(__name__)

    

def page_not_found(request):
    template_name = '404.html'
    return render(request, template_name)


def server_error(request):
    template_name = '500.html'
    return render(request, template_name)

def permission_denied(request):
    template_name = '500.html'
    return render(request, template_name)

def bad_request(request):
    template_name = '500.html'
    return render(request, template_name)


def home(request):
    """
    This function serves the About Page.
    By default the About html page is saved
    on the root template folder.
    """
    template_name = "home.html"
    page_title = settings.SITE_NAME + " - Paiement en ligne"
    context = {
        'page_title': page_title,
        'user_is_authenticated' : request.user.is_authenticated
    }


    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pay.settings')
    logger.debug(f"DATABASE HOST : {os.environ['PAY_DATABASE_HOST']}")
    return render(request, template_name,context)


def about(request):
    """
    This function serves the About Page.
    By default the About html page is saved
    on the root template folder.
    """
    template_name = "about.html"
    page_title = 'A Propose | ' + settings.SITE_NAME
    context = {
        'page_title': page_title,
    }
    return render(request, template_name,context)



def faq(request):
    template_name = "faq_flat.html"
    page_title = "FAQ | " + settings.SITE_NAME
    context = {
        'page_title': page_title,
    }
    return render(request, template_name,context)


def customer_usage(request):
    template_name = "customer_usage.html"
    page_title =  "Customer Usage | " + settings.SITE_NAME
    context = {
        'page_title': page_title
    }
    return render(request, template_name,context)