from rest_framework import serializers
from accounts.models import AvailableService, ServiceCategory, Service, Policy, Account
from payments.models import Transfer, Payment, CaseIssue


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



class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ["user","date_of_birth","country", "city","province","address","zip_code","telefon",
                  "newsletter","is_active_account","solde","account_type","policy","email_validated"]




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