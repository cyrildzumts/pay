from rest_framework import viewsets
from rest_framework.permissions import BasePermission, IsAuthenticated

from api.serializers import ( AvailableServiceSerializer, AvailableService, Account, AccountSerializer,
    Transfer, TransferSerializer, Payment, PaymentSerializer,CaseIssue, CaseIssueSerializer,
    CategorySerializer, ServiceCategory, Policy, PolicySerializer, Service, ServiceSerializer,
    VoucherSerializer, SoldVoucherSerializer, UsedVoucherSerializer, Voucher, SoldVoucher, UsedVoucher
 )


class AccountViewSet(viewsets.ReadOnlyModelViewSet):
     queryset = Account.objects.all()
     serializer_class = AccountSerializer
     permission_classes = [IsAuthenticated]


class BusinessAccountViewSet(viewsets.ReadOnlyModelViewSet):
     queryset = Account.objects.filter(account_type='B')
     serializer_class = AccountSerializer
     permission_classes = [IsAuthenticated]


class ActiveAccountViewSet(viewsets.ReadOnlyModelViewSet):
     queryset = Account.objects.filter(is_active_account=True)
     serializer_class = AccountSerializer
     permission_classes = [IsAuthenticated]


class ServiceViewSet(viewsets.ReadOnlyModelViewSet):
     queryset = Service.objects.all()
     serializer_class = ServiceSerializer
     permission_classes = [IsAuthenticated]



class TransferViewSet(viewsets.ReadOnlyModelViewSet):
     queryset = Transfer.objects.all()
     serializer_class = TransferSerializer
     permission_classes = [IsAuthenticated]


class PaymentViewSet(viewsets.ReadOnlyModelViewSet):
     queryset = Payment.objects.all()
     serializer_class = PaymentSerializer
     permission_classes = [IsAuthenticated]



class AvailableServiceViewSet(viewsets.ModelViewSet):
     queryset = AvailableService.objects.all()
     serializer_class = AvailableServiceSerializer
     permission_classes = [IsAuthenticated]


class ServiceCategoryViewSet(viewsets.ModelViewSet):
     permission_classes = [IsAuthenticated]
     queryset = ServiceCategory.objects.all()
     serializer_class = CategorySerializer


class PolicyViewSet(viewsets.ModelViewSet):
     permission_classes = [IsAuthenticated]
     queryset = Policy.objects.all()
     serializer_class = PolicySerializer


class CaseIssueViewSet(viewsets.ModelViewSet):
     permission_classes = [IsAuthenticated]
     queryset = CaseIssue.objects.all()
     serializer_class = CaseIssueSerializer



class VoucherViewSet(viewsets.ReadOnlyModelViewSet):
     queryset = Voucher.objects.all()
     serializer_class = VoucherSerializer
     permission_classes = [IsAuthenticated]



class UsedVoucherViewSet(viewsets.ReadOnlyModelViewSet):
     queryset = UsedVoucher.objects.all()
     serializer_class = UsedVoucherSerializer
     permission_classes = [IsAuthenticated]


class SoldVoucherViewSet(viewsets.ReadOnlyModelViewSet):
     queryset = SoldVoucher.objects.all()
     serializer_class = SoldVoucherSerializer
     permission_classes = [IsAuthenticated]