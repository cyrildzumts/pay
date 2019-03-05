from django import forms
from django.contrib.auth.models import User
from accounts.models import Account, IDCard
from payments.models import Payment, Transaction, CaseIssue
from django.contrib.admin.widgets import AdminDateWidget
import datetime


class PaymentForm(forms.ModelForm):

    class Meta:
        model = Payment
        exclude = [ 'created_at', 'validated_at']



class TransactionForm(forms.ModelForm):

    class Meta:
        model = Transaction
        exclude = [ 'created_at', 'validated_at']


class CaseIssueForm(forms.ModelForm):

    class Meta:
        model = CaseIssue
        exclude = [ 'created_at', 'closed_at', 'is_closed' ]

