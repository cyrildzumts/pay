from django import forms
from django.contrib.auth.models import Group, Permission
from accounts.models import Account
from payments.models import (
    Service, ServiceCategory, Policy, AvailableService, IDCard, Payment, Transaction,
    Transfer, Reduction, PolicyGroup, PolicyMembership
)



class PolicyForm(forms.ModelForm):
    
    class Meta:
        model = Policy
        fields = ("daily_limit","weekly_limit", "monthly_limit", "commission",)

class PolicyGroupForm(forms.ModelForm):

    class Meta:
        model = PolicyGroup
        fields = ('name', 'policy',)

class PolicyGroupUpdateForm(forms.ModelForm):
    
    class Meta:
        model = PolicyGroup
        fields = ('name', 'policy', 'members',)

class PolicyGroupUpdateMembersForm(forms.ModelForm):
    
    class Meta:
        model = PolicyGroup
        fields = ('members',)

class ServiceCategoryForm(forms.ModelForm):
    
    class Meta:
        model = ServiceCategory
        fields = ("category_name", "category_code", "is_active",)



class AvailableServiceForm(forms.ModelForm):
    
    class Meta:
        model = AvailableService
        fields = ("service_code", "name", "operator", "category", "is_active", "description",)


class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = (  'name', 'operator', 'customer', 'customer_reference', 
                    'reference_number', 'category', 'service_instance',
                    'price', 'description', 'issued_at', 'commission',)

class IDCardForm(forms.ModelForm):
    
    class Meta:
        model = IDCard
        fields = ("user","card_number", "is_valid","delivery_at","expire_at","delivery_place",)




class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ("user","date_of_birth","telefon",
                  "newsletter","is_active","account_type",
                  "email_validated", )
        


class TokenForm(forms.Form):
    user = forms.IntegerField()


class GroupFormCreation(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name', 'permissions']