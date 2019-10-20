from rest_framework import viewsets
from rest_framework.permissions import BasePermission, IsAuthenticated
from api.permissions import (
     CanAddVoucherPermission, CanChangeVoucherPermission, CanDeleteVoucherPermission, CanReadVoucherPermission
)

from api.serializers import ( AvailableServiceSerializer, AvailableService, Account, AccountSerializer,
    Transfer, TransferSerializer, Payment, PaymentSerializer,CaseIssue, CaseIssueSerializer,
    CategorySerializer, ServiceCategory, Policy, PolicySerializer, Service, ServiceSerializer,
    VoucherSerializer, SoldVoucherSerializer, UsedVoucherSerializer, Voucher, SoldVoucher, UsedVoucher,
    UserSerializer
 )


class AccountViewSet(viewsets.ReadOnlyModelViewSet):
     queryset = AccountSerializer.Meta.model.objects.all()
     serializer_class = AccountSerializer
     permission_classes = [IsAuthenticated]


class BusinessAccountViewSet(viewsets.ReadOnlyModelViewSet):
     queryset = AccountSerializer.Meta.model.objects.filter(account_type='B')
     serializer_class = AccountSerializer
     permission_classes = [IsAuthenticated]


class ActiveAccountViewSet(viewsets.ReadOnlyModelViewSet):
     queryset = AccountSerializer.Meta.model.objects.filter(is_active_account=True)
     serializer_class = AccountSerializer
     permission_classes = [IsAuthenticated]


class ServiceViewSet(viewsets.ReadOnlyModelViewSet):
     queryset = ServiceSerializer.Meta.model.objects.all()
     serializer_class = ServiceSerializer
     permission_classes = [IsAuthenticated]



class TransferViewSet(viewsets.ReadOnlyModelViewSet):
     queryset = TransferSerializer.Meta.model.objects.all()
     serializer_class = TransferSerializer
     permission_classes = [IsAuthenticated]


class PaymentViewSet(viewsets.ReadOnlyModelViewSet):
     queryset = PaymentSerializer.Meta.model.objects.all()
     serializer_class = PaymentSerializer
     permission_classes = [IsAuthenticated]



class AvailableServiceViewSet(viewsets.ModelViewSet):
     queryset = AvailableServiceSerializer.Meta.model.objects.all()
     serializer_class = AvailableServiceSerializer
     permission_classes = [IsAuthenticated]


class ServiceCategoryViewSet(viewsets.ModelViewSet):
     permission_classes = [IsAuthenticated]
     queryset = CategorySerializer.Meta.model.objects.all()
     serializer_class = CategorySerializer


class PolicyViewSet(viewsets.ModelViewSet):
     permission_classes = [IsAuthenticated]
     queryset = Policy.objects.all()
     serializer_class = PolicySerializer


class CaseIssueViewSet(viewsets.ModelViewSet):
     permission_classes = [IsAuthenticated]
     queryset = CaseIssueSerializer.Meta.model.objects.all()
     serializer_class = CaseIssueSerializer



class VoucherViewSet(viewsets.ReadOnlyModelViewSet):
     queryset = VoucherSerializer.Meta.model.objects.all()
     serializer_class = VoucherSerializer
     permission_classes = [IsAuthenticated|CanReadVoucherPermission|CanDeleteVoucherPermission]



class UsedVoucherViewSet(viewsets.ReadOnlyModelViewSet):
     queryset = UsedVoucherSerializer.Meta.model.objects.all()
     serializer_class = UsedVoucherSerializer
     permission_classes = [IsAuthenticated]


class SoldVoucherViewSet(viewsets.ReadOnlyModelViewSet):
     queryset = SoldVoucherSerializer.Meta.model.objects.all()
     serializer_class = SoldVoucherSerializer
     permission_classes = [IsAuthenticated]