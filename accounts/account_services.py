from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as django_login, logout as django_logout
from django.contrib.auth.forms import PasswordChangeForm
from django.db import IntegrityError
from pay import utils, settings
from abc import ABCMeta, ABC
from accounts.forms import  RegistrationForm, AuthenticationForm, AccountForm, UserSignUpForm, AccountCreationForm
from accounts.models import Account, Policy



REDIRECT_URL = settings.LOGIN_REDIRECT_URL



def print_form(form=None):
    print("Printing Registration Form Fields")
    if form :
        items = form.items()
        for field, value in items:
            print(field + " : " + value)
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
        result_dict['user_created'] = False
        result_dict['next_url'] = REDIRECT_URL
        postdata = utils.get_postdata(request)
        #form = RegistrationForm(data=postdata)
        user_form = UserSignUpForm(postdata)
        account_form = AccountCreationForm(postdata)
        print_form(postdata)
        if user_form.is_valid() and account_form.is_valid():
            print("User creation data is valid")
            user = user_form.save()
            user.refresh_from_db()
            account_form = AccountCreationForm(postdata, instance=user.account)
            account_form.full_clean()
            account_form.save()
            result_dict['user_created'] = True
            
        else:
            print("User creation data is invalid")
            if user_form.is_valid():
                print("User creation Form is valid")
            else:
                print("User creation Form is invalid")
            if account_form.is_valid():
                print("Acount creation Form is valid")
            else:
                print("Account creation Form is invalid")

        return result_dict



    @staticmethod
    def create_account(accountdata=None, userdata=None):
        created = True
        if accountdata and userdata:
            try:
                user = User.objects.create(**userdata)
                #user.refresh_from_db()
                Account.objects.filter(user=user).update(**accountdata)
            
            except IntegrityError:
                created = False
        else:
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