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



class SellVoucherForm(forms.Form):
    seller = forms.CharField(max_length=32, label="Voucher Card Seller")
    amount = forms.IntegerField(label="Voucher Credit value")


class RechargeCustomerAccountByStaff(forms.Form):
    seller = forms.IntegerField(label="Seller Name")
    custormer = forms.IntegerField(label="Customer")
    amount = forms.IntegerField(label="Voucher Credit value")

class RechargeCustomerAccount(forms.Form):
    seller = forms.IntegerField(label="Seller Name")
    custormer = forms.IntegerField(label="Customer")
    recharged_by = forms.IntegerField()
    amount = forms.IntegerField(label="Voucher Credit value")
    

