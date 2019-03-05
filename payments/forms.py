from django import forms
from django.contrib.auth.models import User
from accounts.models import Account, IDCard
from payments.models import Payment, Transaction, CaseIssue
from django.contrib.admin.widgets import AdminDateWidget
import datetime


class PaymentForm(forms.ModelForm):

    class Meta:
        model = Payment



class TransactionForm(forms.ModelForm):

    class Meta:
        model = Transaction


class CaseIssueForm(forms.ModelForm):

    class Meta:
        model = CaseIssue

