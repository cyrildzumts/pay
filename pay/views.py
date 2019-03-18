from django.shortcuts import render, HttpResponseRedirect
from django.contrib import auth
# from django import forms
from django.contrib.auth.forms import UserCreationForm
from pay import settings



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


def login_view(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(username=username, password=password)
    print("login_view called")
    if user is not None and user.is_active:
        # correct password, and the user is marked "active"
        auth.login(request, user)
        # Redirect to a success page
        return HttpResponseRedirect("/account/loggedin/")
    else:
        # show an error page
        return HttpResponseRedirect("/account/invalid/")


def logout_view(request):
    auth.logout(request)
    # Redirect to a succes page
    return HttpResponseRedirect("/account/loggedout/")


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            return HttpResponseRedirect("/")
    else:
        form = UserCreationForm()
    return render(request, template_name="registration/register.html",
                  context=locals())




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
        'user_is_authenticated' : request.user.is_authenticated(),
        'site_name': settings.SITE_NAME
    }
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