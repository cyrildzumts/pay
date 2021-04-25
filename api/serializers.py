from rest_framework import serializers
from django.contrib.auth.models import User
from accounts.models import Account
from payments.models import (
    Transfer, Payment, CaseIssue, AvailableService, ServiceCategory, Service, Policy, Refund
)
from voucher.models import (
    Voucher, SoldVoucher, UsedVoucher
)


class AvailableServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = AvailableService
        fields = ['service_code', 'name', 'operator', 'category', 'created_at', 'created_by', 'description', 'is_active']



class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['name', 'operator', 'customer', 'customer_reference', 'reference_number', 'category', 'service_instance',
        'price', 'description', 'issued_at', 'created_at','commission']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceCategory
        fields = ["category_name", "category_code",'created_at', "is_active"]


class PolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = Policy
        fields = ["daily_limit","weekly_limit", "monthly_limit",'created_at', "commission"]



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name']

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ["user","date_of_birth","telefon",
                  "newsletter","account_type","email_validated"]




class PaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = [ 'amount', 'sender', 'recipient','is_validated','validated_at','created_at', 'details']




class TransferSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transfer
        fields = [ 'amount', 'sender', 'recipient','created_at', 'details']


class CaseIssueSerializer(serializers.ModelSerializer):

    class Meta:
        model = CaseIssue
        fields = [ 'participant_1', 'participant_2', 'amount', 'subject', 'description', 'is_closed' ]



class VoucherSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Voucher
        fields = ('name','voucher_code', 'amount', 'is_used', 'created_at', 'activated', 'activated_at', )



class UsedVoucherSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = UsedVoucher
        fields = ("customer","voucher", "used_at", )



class SoldVoucherSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = SoldVoucher
        fields = ("seller","voucher", "sold_at", )



class RefundSerializer(serializers.ModelSerializer):
    class Meta:
        model = Refund
        fields = ['amount', 'status', 'declined_reason', 'payment', 'created_at', 'last_changed_at', 'refund_uuid']