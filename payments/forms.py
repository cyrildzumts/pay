from django import forms
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from accounts.models import Account
from payments.models import (
    Payment, Transaction,Transfer, CaseIssue, Policy, Service, ServiceCategory,AvailableService, IDCard,
    Reduction, PaymentRequest, Refund
)
from django.contrib.admin.widgets import AdminDateWidget
import datetime

COMMISSION_MAX_VALUE = 1.00
COMMISSION_MIN_VALUE = 0.00000
COMMISSION_VALUE_ERROR_MSG = "Commission value must be in [0.00000 - 1.00] interval."


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
        fields = ['card_number', 'image', 'user', 'delivery_at', 'expire_at', 'delivery_place']


class ServiceCategoryCreationForm(forms.ModelForm):
    class Meta:
        model = ServiceCategory
        fields = ['category_name', 'category_code', 'is_active']


class AvailableServiceCreationForm(forms.ModelForm):
    class Meta:
        model = AvailableService
        fields = ['service_code', 'name', 'operator', 'category', 'is_active', 'description']
    
    def clean_operator(self):
        operator = self.cleaned_data.get('operator')
        if not operator or not operator.is_active:
            raise forms.ValidationError(message='You can not use a service offered by an inactive operator', code='invalid')
        return operator
    
    def clean_category(self):
        category = self.cleaned_data.get('category')
        if not category or not category.is_active:
            raise forms.ValidationError(message='You can not create this service. This service  category is deactivated', code='invalid')
        return category


class ServiceCreationForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['name', 'operator', 'customer', 'customer_reference', 'reference_number', 'category', 'service_instance',
        'price', 'description', 'issued_at', 'commission']

    def clean_commission(self):
        commission = self.cleaned_data.get('commission')
        if not commission or ( commission > COMMISSION_MAX_VALUE or commission < COMMISSION_MIN_VALUE):
            raise forms.ValidationError(message=COMMISSION_VALUE_ERROR_MSG, code='invalid')
        return commission
    

    def clean_operator(self):
        operator = self.cleaned_data.get('operator')
        if not operator or not operator.is_active:
            raise forms.ValidationError(message='You can not use a service of an inactive account', code='invalid')
        return operator
    
    def clean_customer(self):
        customer = self.cleaned_data.get('customer')
        if not customer or not customer.is_active:
            raise forms.ValidationError(message='You can not make use a service with an inactive account', code='invalid')
        return customer

    
    def clean_service_instance(self):
        service_instance = self.cleaned_data.get('service_instance')
        if not service_instance or not service_instance.is_active:
            raise forms.ValidationError(message='You can not make use a of this service. This service is deactivated', code='invalid')
        return service_instance

    def clean_category(self):
        category = self.cleaned_data.get('category')
        if not category or not category.is_active:
            raise forms.ValidationError(message='You can not make use a of this service. This service  category is deactivated', code='invalid')
        return category



    def clean(self):
        '''
            The operator must be the same as the operator found in service_instance.
        '''
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        operator = cleaned_data.get('operator')
        customer = cleaned_data.get('customer')
        available_service_instance = cleaned_data.get('service_instance')
        price = cleaned_data.get('price')
        if not name:
            raise forms.ValidationError(message="service name is missing", code='invalid')

        if operator and available_service_instance:
            if operator != available_service_instance.operator:
                raise forms.ValidationError(message='The selected operator is not the one offering this service', code='invalid')
            if hasattr(customer, 'balance') and customer.balance.balance < price:
                raise forms.ValidationError(message='customer balance is insufficient to process this payment', code='invalid')
        else:
            if not operator:
                self.add_error('operator', 'The operator is missing')
            if not available_service_instance:
                self.add_error('service_instance', 'service_instance is missing')
            
            
            
        
        

class TransactionVerificationForm(forms.Form):
    
    verification_code = forms.CharField(max_length=80, label="Verification Code", strip=True, required=False)
    operator_reference = forms.CharField(max_length=80, label="Operator Reference", strip=True, required=False)

    def clean(self):
        cleaned_data = super().clean()
        verificaion_code = cleaned_data.get('verification_code')
        operator_reference = cleaned_data.get('operator_reference')
        if not (verificaion_code or operator_reference):
            raise forms.ValidationError(message='Verification failed. You must fill at least one of the two fields.', code='invalid')


class PaymentVerificationForm(forms.Form):
    
    verification_code = forms.CharField(max_length=80, label="Verification Code", strip=True, required=False)
    operator_reference = forms.CharField(max_length=80, label="Operator Reference", strip=True, required=False)

    def clean(self):
        cleaned_data = super().clean()
        verificaion_code = cleaned_data.get('verification_code')
        operator_reference = cleaned_data.get('operator_reference')
        if not (verificaion_code or operator_reference):
            raise forms.ValidationError(message='Verification failed. You must fill at least one of the two fields.', code='invalid')

class RechargeForm(forms.Form):
    voucher = forms.CharField(max_length=32, label="Voucher Code")


class PaymentForm(forms.ModelForm):

    class Meta:
        model = Payment
        fields = ['amount', 'sender', 'recipient', 'details']
    
    def clean_sender(self):
        sender = self.cleaned_data.get('sender')
        if not sender or not sender.is_active:
            raise forms.ValidationError(message='You can not make a payment from an inactive account', code='invalid')
        return sender
    
    def clean_recipient(self):
        recipient = self.cleaned_data.get('recipient')
        if not recipient or not recipient.is_active:
            raise forms.ValidationError(message='You can not make a payment to an inactive account', code='invalid')
        return recipient
    
    def clean(self):
        super().clean()
        amount = self.cleaned_data.get('amount')
        sender = self.cleaned_data.get('sender')
        recipient = self.cleaned_data.get('recipient')
        if sender == recipient:
            raise forms.ValidationError(message=f'Sender \"{sender.username}\" and recipient \"{sender.username}\" are the same.', code="invalid")
        if not recipient.policygroup_set.exists():
            raise forms.ValidationError(message=f"recipient {recipient.username} has no policy group")
        if sender.balance and sender.balance.balance < amount:
            raise forms.ValidationError(message=f"sender {sender.username} has not enough money on his balance")


class RefundForm(forms.ModelForm):
    class Meta:
        model = Refund
        fields = ['amount','status','declined_reason', 'payment']

    


    




class PaymentRequestForm(forms.ModelForm):
    
    class Meta:
        model = PaymentRequest
        fields = ['payment', 'seller', 'amount', 'unit_price','quantity', 'tva', 'commission',
        'country', 'status', 'product_name', 'customer_name', 'description', 'requester_name', 
        'redirect_success_url', 'redirect_failed_url', 'failed_reason'
        ]
    """
    def clean_token(self):
        token = self.cleaned_data.get('token')
        if not Token.objects.exists(key=token):
            raise forms.ValidationError(message='Invalid Token', code='invalid')

        return token
    """

class TransactionForm(forms.ModelForm):

    class Meta:
        model = Transaction
        fields = ['amount', 'sender', 'recipient', 'details', 'transaction_type', 'reduction', 'policy']


class TransferForm(forms.ModelForm):

    class Meta:
        model = Transfer
        fields = ['amount', 'sender', 'recipient', 'details']

    def clean_sender(self):
        sender = self.cleaned_data.get('sender')
        if not sender or not sender.is_active:
            raise forms.ValidationError(message='You can not make a transfer from an inactive account', code='invalid')
        return sender
    
    def clean_recipient(self):
        recipient = self.cleaned_data.get('recipient')
        if not recipient or not recipient.is_active:
            raise forms.ValidationError(message='You can not make a transfer to an inactive account', code='invalid')
        return recipient
    
    def clean(self):
        super().clean()
        amount = self.cleaned_data.get('amount')
        sender = self.cleaned_data.get('sender')
        recipient = self.cleaned_data.get('recipient')
        if sender == recipient:
            raise forms.ValidationError(message=f'Sender \"{sender.username}\" and recipient \"{sender.username}\" are the same.', code="invalid")
        if recipient.policygroup_set.exists():
            raise forms.ValidationError(message=f"Transfer to business user is not allowed")
        if sender.balance and sender.balance.balance < amount:
            raise forms.ValidationError(message=f"sender {sender.username} has not enough money on his balance")



class CaseIssueForm(forms.ModelForm):

    class Meta:
        model = CaseIssue
        fields = ['participant_1', 'participant_2','amount', 'subject', 'description', 'is_closed']

"""
class ClaimForm(forms.ModelForm):

    class Meta:
        model = CaseIssue
        fields = ['reporter', 'operator','amount', 'subject', 'description', 'is_closed']
"""

class ReductionForm(forms.ModelForm):

    class Meta:
        model = Reduction
        fields = ['code', 'percent', 'user']
