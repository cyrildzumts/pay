from django import forms
from django.contrib.auth.models import User
from accounts.models import Account
from payments.models import (
    Payment, Transaction,Transfer, CaseIssue, Policy, Service, ServiceCategory,AvailableService, IDCard
)
from django.contrib.admin.widgets import AdminDateWidget
import datetime


class PolicyForm(forms.ModelForm):
    class Meta:
        model = Policy
        exclude = ['policy_id']


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
        exclude = ['created_at','is_active']


class AvailableServiceCreationForm(forms.ModelForm):
    class Meta:
        model = AvailableService
        exclude = ['created_at','is_active']


class ServiceCreationForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['name', 'operator', 'customer', 'customer_reference', 'reference_number', 'category', 'service_instance',
        'price', 'description', 'issued_at', 'commission']



class RechargeForm(forms.Form):
    voucher = forms.CharField(max_length=32, label="Voucher Code")

class PaymentForm(forms.ModelForm):

    class Meta:
        model = Payment
        exclude = [ 'created_at', 'validated_at']



class TransactionForm(forms.ModelForm):

    class Meta:
        model = Transaction
        exclude = [ 'created_at', 'validated_at']


class TransferForm(forms.ModelForm):

    class Meta:
        model = Transfer
        exclude = [ 'created_at']


class CaseIssueForm(forms.ModelForm):

    class Meta:
        model = CaseIssue
        exclude = [ 'created_at', 'closed_at', 'is_closed' ]

