from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as django_login, logout as django_logout
from pay import utils, settings
from abc import ABCMeta, ABC
from accounts.forms import  RegistrationForm, AuthenticationForm


REDIRECT_URL = settings.LOGIN_REDIRECT_URL

class AccountService(ABC):

    @staticmethod
    def get_authentication_form(initial_content=False):
        return AuthenticationForm()
    
    @staticmethod
    def get_registration_form():
        return RegistrationForm()

    @staticmethod
    def process_login_request(request):
        result_dict = {}
        result_dict['user_logged'] = False
        result_dict['next_url'] = REDIRECT_URL
        postdata = utils.get_postdata(request)
        form = AuthenticationForm(data=postdata)
        if form.is_valid():
            str_url = postdata['next']
            if len(str_url) > 0 :
                result_dict['next_url'] = str_url
            
            user = auth.authenticate(username=postdata['username'],
                                    password=postdata['password'])

            if user is not None:
                if user.is_active:
                    auth.login(request, user)
                    result_dict['user_logged'] = True

        return result_dict
    

    @staticmethod
    def process_registration_request(request):
        result_dict = {}
        result_dict['user_logged'] = False
        result_dict['next_url'] = REDIRECT_URL
        postdata = utils.get_postdata(request)
        form = RegistrationForm(data=postdata)
        if form.is_valid():
            form.save()
            username = postdata['username']
            password = postdata['password1']
            user = auth.authenticate(username=username, password=password)

            if user and user.is_active:
                auth.login(request, user)
                result_dict['user_logged'] = True
        
        return result_dict


