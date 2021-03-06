from django.shortcuts import render
from django.utils.translation import gettext_lazy as _
from django.db.models.functions import ExtractDay, ExtractMonth, ExtractYear
from django.db.models import Count, Avg, F, Q, Sum, Max, Min
from django.forms.models import model_to_dict
from django.urls import reverse, resolve
from rest_framework import filters
from django.views.decorators.csrf import csrf_exempt
from rest_framework.generics import (
    ListCreateAPIView,
    ListAPIView,
    RetrieveUpdateDestroyAPIView
)
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from api.serializers import ( AvailableServiceSerializer, AccountSerializer,
    TransferSerializer, PaymentSerializer, CaseIssueSerializer,
    CategorySerializer, PolicySerializer, ServiceSerializer, UserSerializer
 )
from django.contrib.auth.models import User
from accounts.models import Account
from payments.models import Transfer, Payment, PaymentRequest, Service, CaseIssue, AvailableService, Policy, Refund
from voucher.models import Voucher
from payments.forms import PaymentRequestForm
from payments import payment_service
from pay import utils
from django.utils import timezone
from operator import itemgetter
import logging
logger = logging.getLogger(__name__)

# Create your views here.
# REST API Views

class UserSearchByNameView(ListAPIView):
     #permission_classes = [IsAuthenticated]
     serializer_class = UserSerializer
     search_fields = ['last_name', 'first_name','username']
     filter_backends = [filters.SearchFilter]
     queryset = User.objects.filter(is_superuser=False)
     """
     def get_queryset(self):
          user_search = self.request.POST.get('user-search', "")
          if len(user_search) > 0 :
               return UserSerializer.Meta.model.objects.filter(last_name__icontains=user_search)
          return UserSerializer.Meta.model.objects.none()
     """

class UserSearchView(ListAPIView):
     serializer_class = UserSerializer
     search_fields = ['last_name', 'first_name', 'username']
     filter_backends = [filters.SearchFilter]
     queryset = User.objects.filter(is_superuser=False)
     """
     def get_queryset(self):
          user_search = self.request.POST.get('user-search', "")
          if len(user_search) > 0 :
               return UserSerializer.Meta.model.objects.filter(last_name__icontains=user_search)
          return UserSerializer.Meta.model.objects.none()
     """


class AvailableServiceListAPIView(ListAPIView):
    queryset =  AvailableService.objects.all()
    serializer_class =  AvailableServiceSerializer


class AvailableServiceListCreateAPIView(ListCreateAPIView):
    queryset = AvailableService.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class =  AvailableServiceSerializer


class AvailableServiceRetrieveUpdateCreateAPIView(RetrieveUpdateDestroyAPIView):
    queryset = AvailableService.objects.all()
    #permission_classes = (IsAuthenticated, )
    serializer_class =  AvailableServiceSerializer
    lookup_field = 'pk'


class ServiceListView(ListAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    #permission_classes = (IsAuthenticated, )


class PolicyListView(ListAPIView):
    queryset = Policy.objects.all()
    serializer_class = PolicySerializer



class PolicyRetrieveUpdateCreateAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Policy.objects.all()
    #permission_classes = (IsAuthenticated, )
    serializer_class =  PolicySerializer
    lookup_field = 'pk'


class TransferListAPIView(ListAPIView):
    queryset = Transfer.objects.all()
    #permission_classes = (IsAuthenticated, )
    serializer_class =  TransferSerializer
    lookup_field = 'pk'

class TransferRetrieveUpdateCreateAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Transfer.objects.all()
    #permission_classes = (IsAuthenticated, )
    serializer_class =  TransferSerializer
    lookup_field = 'pk'


@api_view(['GET', 'POST'])
def payment_request(request, username, token):
    logger.debug(f"New Payment Request - usernme \"{username}\" - token \"{token}\"")
    auth_token = None
    if not username or not token :
        logger.error("PAYMENT REQUEST API : username or token missing")
        return Response({'error': 'username or token missing'})
        
    try:
        auth_token = Token.objects.get(key=token, user__username=username)
    except Token.DoesNotExist as e:
        logger.error('PAYMENT REQUEST API : User not found')
        return Response({'error': f'Request user {username} not found'}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'POST':
        postdata = request.POST.copy()
        postdata['seller'] = auth_token.user.pk
        form = PaymentRequestForm(postdata)
        logger.info(f"POSTDATA")
        logger.info(postdata)
            
        if form.is_valid(): 
            p_request = form.save()
            logger.info(f"PAYMENT REQUEST API : Created Payment Request from user \"{username}\"")
            url = request.build_absolute_uri(reverse('payments:payment-request', kwargs={'request_uuid':p_request.request_uuid}))
            return Response({'token':p_request.request_uuid, 'url': url, 'verification_code': p_request.verification_code}, status=status.HTTP_200_OK)
        else:
            logger.error(f"PAYMENT REQUEST API : Payment Request from user \"{username}\" is invalid")
            for k,v in form.errors.items():
                logger.info(f" P - Key: {k} - Value: {v}")
            return Response({'error': 'Submitted data is invalid'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        logger.info(f"PAYMENT REQUEST API : Payment Request from user \"{username}\" rejected. Method GET not allowed")
        return Response({'error': 'Bad Request'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET'])
def analytics_data(request):
    data = []
    payment_count = Payment.objects.count()
    transfer_count = Transfer.objects.count()
    payment_request_count = PaymentRequest.objects.count()
    service_count = Service.objects.count()
    user_count = User.objects.count()
    sold_voucher_count = Voucher.objects.filter(is_sold=True).count()
    voucher_count = Voucher.objects.count()

    data.append({'label':_('Payments'), 'count': payment_count})
    data.append({'label':_('Transfers'), 'count': transfer_count})
    data.append({'label':_('Payment Requests'), 'count': payment_request_count})
    data.append({'label':_('Users'), 'count': user_count})
    data.append({'label':_('Services'), 'count': service_count})
    data.append({'label':_('Vouchers'), 'count': voucher_count, 'sold': sold_voucher_count})
    return Response(data, status=status.HTTP_200_OK)

@api_view(['GET'])
def transaction_reports(request):
    data = []
    payment_report = Payment.objects.aggregate(total_count=Count('id'), total_paid=Sum('amount'), avg_paid=Avg('amount'), max_paid=Max('amount'), min_paid=Min('amount'))
    transfer_report = Transfer.objects.aggregate(total_count=Count('id'), total_paid=Sum('amount'), avg_paid=Avg('amount'), max_paid=Max('amount'), min_paid=Min('amount'))
    payment_request_report = PaymentRequest.objects.aggregate(total_count=Count('id'), total_paid=Sum('amount'), avg_paid=Avg('amount'), max_paid=Max('amount'), min_paid=Min('amount'))
    service_report = Service.objects.aggregate(total_count=Count('id'), total_paid=Sum('price'), avg_paid=Avg('price'), max_paid=Max('price'), min_paid=Min('price'))
    sold_voucher_report = Voucher.objects.filter(is_sold=True).aggregate(total_count=Count('id'), total_paid=Sum('amount'), avg_paid=Avg('amount'), max_paid=Max('amount'), min_paid=Min('amount'))
    
    data.append({'label':_('Payments'), 'report': payment_report})
    data.append({'label':_('Transfers'), 'report': transfer_report})
    data.append({'label':_('Payment Requests'), 'report': payment_request_report})
    data.append({'label':_('Services'), 'report': service_report})
    data.append({'label':_('Vouchers'), 'report': sold_voucher_report})
    return Response(data, status=status.HTTP_200_OK)


@api_view(['GET'])
def analytics_monthly_data(request,year=None, month=None):
    year = year or timezone.now().year
    month = month or timezone.now().month

    datefield = 'created_at'
    user_datefield = 'date_joined'
    yearfield = 'year'
    monthfield = 'month'
    dayfield = 'day'

    payment_set = Payment.objects.filter(created_at__year=year, created_at__month=month).annotate(year=ExtractYear(datefield), month=ExtractMonth(datefield), day=ExtractDay(datefield))
    transfer_set = Transfer.filter(created_at__year=year, created_at__month=month).objects.annotate(year=ExtractYear(datefield), month=ExtractMonth(datefield), day=ExtractDay(datefield))
    payment_request_set = PaymentRequest.objects.filter(created_at__year=year, created_at__month=month).annotate(year=ExtractYear(datefield), month=ExtractMonth(datefield), day=ExtractDay(datefield))
    service_set = Service.objects.filter(created_at__year=year, created_at__month=month).annotate(year=ExtractYear(datefield), month=ExtractMonth(datefield), day=ExtractDay(datefield))
    user_set = User.objects.filter(date_joined__year=year, date_joined__month=month).annotate(year=ExtractYear(user_datefield), month=ExtractMonth(user_datefield), day=ExtractDay(user_datefield))
    
    data = []
    data.append({'label':_('Payments'), 'datasets': list(payment_set.values(yearfield, monthfield).annotate(count=Count(monthfield)))})
    data.append({'label':_('Transfers'), 'datasets': list(transfer_set.values(yearfield, monthfield).annotate(count=Count(monthfield)))})
    data.append({'label':_('Payments Request'), 'datasets': list(payment_request_set.values(yearfield, monthfield).annotate(count=Count(monthfield)))})
    data.append({'label':_('Users'), 'datasets': list(user_set.values(yearfield, monthfield).annotate(count=Count(monthfield)))})
    return Response(data, status=status.HTTP_200_OK)


@api_view(['GET'])
def analytics_yearly_data(request, year=None):
    year = year or timezone.now().year
    datefield = 'created_at'
    user_datefield = 'date_joined'
    yearfield = 'year'
    monthfield = 'month'
    dayfield = 'day'
    data = []
    payment_set = Payment.objects.filter(created_at__year=year).annotate(year=ExtractYear(datefield), month=ExtractMonth(datefield), day=ExtractDay(datefield))
    transfer_set = Transfer.filter(created_at__year=year).objects.annotate(year=ExtractYear(datefield), month=ExtractMonth(datefield), day=ExtractDay(datefield))
    payment_request_set = PaymentRequest.objects.filter(created_at__year=year).annotate(year=ExtractYear(datefield), month=ExtractMonth(datefield), day=ExtractDay(datefield))
    service_set = Service.objects.filter(created_at__year=year).annotate(year=ExtractYear(datefield), month=ExtractMonth(datefield), day=ExtractDay(datefield))
    user_set = User.objects.filter(date_joined__year=year).annotate(year=ExtractYear(user_datefield), month=ExtractMonth(user_datefield), day=ExtractDay(user_datefield))
    
    data.append({'label':_('Payments'), 'datasets': list(payment_set.values(yearfield, monthfield).annotate(count=Count(yearfield)))})
    data.append({'label':_('Transfers'), 'datasets': list(transfer_set.values(yearfield, monthfield).annotate(count=Count(yearfield)))})
    data.append({'label':_('Payments Request'), 'datasets': list(payment_request_set.values(yearfield, monthfield).annotate(count=Count(yearfield)))})
    data.append({'label':_('Users'), 'datasets': list(user_set.values(yearfield, monthfield).annotate(count=Count(yearfield)))})
    return Response(data, status=status.HTTP_200_OK)


@api_view(['GET'])
def analytics_daily_data(request, year=None, month=None, day=None):
    year = year or timezone.now().year
    month = month or timezone.now().month
    day = day or timezone.now().day

    datefield = 'created_at'
    user_datefield = 'date_joined'
    yearfield = 'year'
    monthfield = 'month'
    dayfield = 'day'

    data = []
    payment_set = Payment.objects.filter(created_at__year=year, created_at__month=month, created_at__day=day).annotate(year=ExtractYear(datefield), month=ExtractMonth(datefield), day=ExtractDay(datefield))
    transfer_set = Transfer.filter(created_at__year=year, created_at__month=month, created_at__day=day).objects.annotate(year=ExtractYear(datefield), month=ExtractMonth(datefield), day=ExtractDay(datefield))
    payment_request_set = PaymentRequest.objects.filter(created_at__year=year, created_at__month=month, created_at__day=day).annotate(year=ExtractYear(datefield), month=ExtractMonth(datefield), day=ExtractDay(datefield))
    service_set = Service.objects.filter(created_at__year=year, created_at__month=month, created_at__day=day).annotate(year=ExtractYear(datefield), month=ExtractMonth(datefield), day=ExtractDay(datefield))
    user_set = User.objects.filter(date_joined__year=year, date_joined__month=month, date_joined__day=day).annotate(year=ExtractYear(user_datefield), month=ExtractMonth(user_datefield), day=ExtractDay(user_datefield))
    
    data.append({'label':_('Payments'), 'datasets': list(payment_set.values(yearfield, monthfield).annotate(count=Count(monthfield)))})
    data.append({'label':_('Transfers'), 'datasets': list(transfer_set.values(yearfield, monthfield).annotate(count=Count(monthfield)))})
    data.append({'label':_('Payments Request'), 'datasets': list(payment_request_set.values(yearfield, monthfield).annotate(count=Count(monthfield)))})
    data.append({'label':_('Users'), 'datasets': list(user_set.values(yearfield, monthfield).annotate(count=Count(monthfield)))})
    return Response(data, status=status.HTTP_200_OK)



@api_view(['GET'])
def payments(request):
    payment_queryset = payment_service.get_payments(request.user)
    return Response(data={'success' : True, 'payments': payment_queryset})


@api_view(['GET'])
def get_payment(request):
    details = request.GET.get('details', None)
    if details:
        payment = payment_service.find_payment_from_description(request.user, details)
        return Response(data={
                'success' : True,
                'payment_uuid': payment.payment_uuid,
                'amount': payment.amount,
                'fee' : payment.fee,
                'created_at':payment.created_at,
                'verification_code': payment.verification_code,
                'details': payment.details, 
                'sender': payment.sender.get_full_name(),
                'recipient': payment.recipient.get_full_name()
                }, status=status.HTTP_200_OK)
    return Response(data={'success' : False, 'message': 'no payment found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def refund_create(request, payment_uuid):
    payment = None
    try:
        payment = Payment.objects.get(payment_uuid=payment_uuid)
    except Payment.DoesNotExist as e:
        logger.warning(f"No payment found with uuid \"{payment_uuid}\"")
        return Response({'message': 'No payment found'}, status=status.HTTP_404_NOT_FOUND)
    data = {'amount' : payment.amount, 'payment': payment.pk}
    refund = payment_service.create_refund(data)
    logger.info(f"payment found with uuid \"{payment_uuid}\"")
    if refund:
        logger.info(f"Refund created for payment with uuid \"{payment_uuid}\"")
        return Response(data={'success' : True, 'refund': refund.refund_uuid, 'payment': payment.payment_uuid, 'created': True, 'accepted': False }, status=status.HTTP_200_OK)
    else:
        logger.warn(f"Refund not created for payment with uuid \"{payment_uuid}\"")
        return Response(data={'success' : False, 'payment': payment.payment_uuid, 'created': False}, status=status.HTTP_200_OK)



@api_view(['POST'])
def client_refund_create(request, payment_uuid):
    payment = None
    auth_token = None

    try:
        payment = Payment.objects.get(payment_uuid=payment_uuid)
    except Payment.DoesNotExist as e:
        logger.warning(f"No payment found with uuid \"{payment_uuid}\"")
        return Response({'message': 'No payment found'}, status=status.HTTP_404_NOT_FOUND)
    

    refund = payment_service.create_accept_refund(request.user, payment)
    logger.info(f"payment found with uuid \"{payment_uuid}\"")
    if refund:
        logger.info(f"Refund created for payment with uuid \"{payment_uuid}\"")
        return Response(data={'refund': refund.refund_uuid, 'payment': payment.payment_uuid, 'created': True, 'status': refund.status, 'declined_reason' : refund.declined_reason }, status=status.HTTP_200_OK)
    else:
        logger.warn(f"Refund not created for payment with uuid \"{payment_uuid}\"")
        return Response(data={'payment': payment.payment_uuid, 'created': False}, status=status.HTTP_200_OK)



@api_view(['POST'])
def client_accept_refund(request, payment_uuid):
    auth_token = None

    try:
        payment = Payment.objects.get(payment_uuid=payment_uuid)
    except Payment.DoesNotExist as e:
        logger.warning(f"No payment found with uuid \"{payment_uuid}\"")
        return Response({'success' : False,'message': 'No payment found'}, status=status.HTTP_404_NOT_FOUND)
    

    refunded = payment_service.accept_refund(request.user, payment)
    if refunded:
        logger.info(f"Refund accepted for payment with uuid \"{payment_uuid}\"")

    else:
        logger.warn(f"Refund not accepted for payment with uuid \"{payment_uuid}\"")
    return Response(data={'success' : refunded,'payment': payment.payment_uuid, 'accepted': refunded}, status=status.HTTP_200_OK)



@api_view(['POST'])
def client_declined_refund(request, payment_uuid):

    try:
        payment = Payment.objects.get(payment_uuid=payment_uuid)
    except Payment.DoesNotExist as e:
        logger.warning(f"No payment found with uuid \"{payment_uuid}\"")
        return Response({'message': 'No payment found'}, status=status.HTTP_404_NOT_FOUND)
    

    declined = payment_service.declined_refund(request.user, payment)
    if declined:
        logger.info(f"Refund declined for payment with uuid \"{payment_uuid}\"")

    else:
        logger.warn(f"Refund not declined for payment with uuid \"{payment_uuid}\"")
    return Response(data={'success' : declined,'payment': payment.payment_uuid, 'declined': declined}, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_refunds(request, status):
    queryset = payment_service.client_refunds(request.user, status)
    data = list(queryset.values())
    return Response(data={'success' : True, 'refunds': data})
    



@api_view(['GET', 'POST'])
def dummy(request):
    logger.info("api dummy request")
    data = utils.get_postdata(request)
    logger.info(f"Dummy Submitted Data : {data}")
    return Response({'dummy': 'request dummy', 'test': 'test result', 'user': request.user.username, 'submitted_data': data})


@api_view(['POST'])
def make_payment(request):
    logger.info("api make payment")
    data = utils.get_postdata(request)
    payment = payment_service.create_payment(data)
    response_data = None
    if payment:
        response_data = {
            'success' : True,
            'amount': payment.amount,
            'redirect_url' : reverse('payments:payment-home')
        }
    else:
        response_data = {
            'success' : False,
            'redirect_url' : reverse('payments:payment-home')
        }
    return Response(response_data)


@api_view(['POST'])
def make_transfer(request):
    data = utils.get_postdata(request)
    transfer = payment_service.create_transfer(data)
    response_data = None
    if transfer:
        response_data = {
            'success' : True,
            'amount': transfer.amount,
            'redirect_url' : reverse('payments:payment-home')
        }
    else:
        response_data = {
            'success' : False,
            'redirect_url' : reverse('payments:payment-home')
        }
    return Response(response_data)