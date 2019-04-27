from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as django_login, logout as django_logout
from django.db import IntegrityError
from pay import utils, settings
from abc import ABCMeta, ABC
from accounts.forms import  RegistrationForm, AuthenticationForm, AccountForm
from accounts.models import Account, Policy



REDIRECT_URL = settings.LOGIN_REDIRECT_URL



def print_form(form=None):
    print("Printing Registration Form Fields")
    if form :
        for field in form:
            print(field.label + " : " + field.value)
    else :
        print("form is not defined")


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
        username = postdata['username']
        password = postdata['password']
        if form.is_valid():
            print("User Login : Submitted Form is valid")
            user = auth.authenticate(username=username,
                                    password=password)

            if user is not None:
                print("User Login : User authenticated : username : {} - password : {}".format(username, password))
                if user.is_active:
                    auth.login(request, user)
                    result_dict['user_logged'] = True
                    print("User Logged In")
            else:
                print("User Login : User not authenticated : username : {} - password : {}".format(username, password))
        else :
            print("User Login : Submitted Form is not valid")
        return result_dict
    

    @staticmethod
    def process_registration_request(request):
        result_dict = {}
        result_dict['user_logged'] = False
        result_dict['next_url'] = REDIRECT_URL
        postdata = utils.get_postdata(request)
        form = RegistrationForm(data=postdata)
        print_form(form)
        if form.is_valid():
            form.save()
            username = postdata['username']
            password = postdata['password1']
            user = auth.authenticate(username=username, password=password)

            if user and user.is_active:
                auth.login(request, user)
                result_dict['user_logged'] = True
        
        return result_dict



    @staticmethod
    def create_account(accountdata=None, userdata=None):
        created = False
        if accountdata and userdata:
            try:
                user = User.objects.create(**userdata)
                Account.objects.filter(user=user).update(**accountdata)
                created = True
            
            except IntegrityError:
                created = False
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