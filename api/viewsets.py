from rest_framework import viewsets

from rest_framework.permissions import IsAuthenticated
from api.serializers import ( AvailableServiceSerializer, AvailableService, Account, AccountSerializer,
    Transfer, TransferSerializer, Payment, PaymentSerializer,CaseIssue, CaseIssueSerializer,
    CategorySerializer, ServiceCategory, Policy, PolicySerializer, Service, ServiceSerializer
 )



class ServiceViewSet(viewsets.ReadOnlyModelViewSet):
     queryset = Service.objects.all()
     serializer_class = ServiceSerializer
     permission_classes = ['IsAuthenticated']



class TransferViewSet(viewsets.ReadOnlyModelViewSet):
     queryset = Transfer.objects.all()
     serializer_class = TransferSerializer
     permission_classes = ['IsAuthenticated']


class PaymentViewSet(viewsets.ReadOnlyModelViewSet):
     queryset = Payment.objects.all()
     serializer_class = PaymentSerializer
     permission_classes = ['IsAuthenticated']