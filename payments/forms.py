from django import forms
from django.contrib.auth.models import User
from accounts.models import Account
from payments.models import (
    Payment, Transaction,Transfer, CaseIssue, Policy, Service, ServiceCategory,AvailableService, IDCard,
    Reduction
)
from django.contrib.admin.widgets import AdminDateWidget
import datetime

COMMISSION_MAX_VALUE = 1.00
COMMISSION_MIN_VALUE = 0.00
COMMISSION_VALUE_ERROR_MSG = "Commission value must be in [0.00 - 1.00] interval."


class PolicyForm(forms.ModelForm):
    class Meta:
        model = Policy
        fields = ['daily_limit', 'weekly_limit', 'monthly_limit', 'commission']

    def clean_commission(self):
        commission = self.cleaned_data['commission']
        if commission > COMMISSION_MAX_VALUE or commission < COMMISSION_MIN_VALUE:
            raise forms.ValidationError(message=COMMISSION_VALUE_ERROR_MSG, code='invalid')
        return commission


class UpdateIDCardForm(forms.ModelForm):
    
    class Meta:
        model = IDCard
        fields = ("card_number", "image", "delivery_at", "delivery_place", "expire_at",)


class IDCardForm(forms.ModelForm):
    class Meta:
        model = IDCard
        fields = ['card_number', 'image', 'user']


class ServiceCategoryCreationForm(forms.ModelForm):
    class Meta:
        model = ServiceCategory
        fields = ['category_name', 'category_code', 'is_active']


class AvailableServiceCreationForm(forms.ModelForm):
    class Meta:
        model = AvailableService
        fields = ['service_code', 'name', 'operator', 'category', 'is_active', 'description']


class ServiceCreationForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['name', 'operator', 'customer', 'customer_reference', 'reference_number', 'category', 'service_instance',
        'price', 'description', 'issued_at', 'commission']

    def clean_commission(self):
        commission = self.cleaned_data.get('commission')
        if commission > COMMISSION_MAX_VALUE or commission < COMMISSION_MIN_VALUE:
            raise forms.ValidationError(message=COMMISSION_VALUE_ERROR_MSG, code='invalid')
        return commission
    
    
    def clean(self):
        '''
            The operator must be the same as the operator found in service_instance.
        '''
        cleaned_data = super().clean()

        operator = cleaned_data.get('operator') # this is the pk value
        available_service_instance = cleaned_data.get('service_instance')
        if operator and available_service_instance:
            if operator.pk != available_service_instance.pk:
                self.add_error('operator', 'This operator is offering this service')
                self.add_error('service_instance', 'The operator offering this service must be the same as the operator field')
                #raise forms.ValidationError(message='The submitted service operator is invalid', code='invalid')
        else:
            if not operator:
                self.add_error('operator', 'This operator is offering this service')
            if not available_service_instance:
                self.add_error('service_instance', 'The operator offering this service must be the same as the operator field')
            
            
            
        
        




class RechargeForm(forms.Form):
    voucher = forms.CharField(max_length=32, label="Voucher Code")

class PaymentForm(forms.ModelForm):

    class Meta:
        model = Payment
        fields = ['amount', 'sender', 'recipient', 'details']



class TransactionForm(forms.ModelForm):

    class Meta:
        model = Transaction
        fields = ['amount', 'sender', 'recipient', 'details', 'transaction_type', 'reduction', 'policy']


class TransferForm(forms.ModelForm):

    class Meta:
        model = Transfer
        fields = ['amount', 'sender', 'recipient', 'details']


class CaseIssueForm(forms.ModelForm):

    class Meta:
        model = CaseIssue
        fields = ['participant_1', 'participant_2','amount', 'subject', 'description', 'is_closed']

class ReductionForm(forms.ModelForm):

    class Meta:
        model = Reduction
        fields = ['code', 'percent', 'user']
