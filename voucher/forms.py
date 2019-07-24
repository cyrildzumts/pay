from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from voucher.models import Voucher, SoldVoucher, UsedVoucher
from django.contrib.admin.widgets import AdminDateWidget
import datetime



class VoucherForm(forms.ModelForm):
    
    class Meta:
        model = Voucher
        fields = ("name","voucher_code", "amount", )


class VoucherCreationForm(forms.Form):
    name = forms.CharField(max_length=32, label="Voucher Card Name")
    amount = forms.IntegerField(label="Voucher Credit value")
    number = forms.IntegerField(label="Number of voucher to generate")
    

