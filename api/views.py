from django.shortcuts import render
from rest_framework import filters

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
from api.serializers import ( AvailableServiceSerializer, AvailableService, Account, AccountSerializer,
    Transfer, TransferSerializer, Payment, PaymentSerializer,CaseIssue, CaseIssueSerializer,
    CategorySerializer, ServiceCategory, Policy, PolicySerializer, Service, ServiceSerializer, UserSerializer
 )
from payments.forms import PaymentRequestForm
from pay import utils

import logging
logger = logging.getLogger(__name__)

# Create your views here.
# REST API Views

class UserSearchByNameView(ListAPIView):
     #permission_classes = [IsAuthenticated]
     serializer_class = UserSerializer
     search_fields = ['last_name', 'first_name','username']
     filter_backends = [filters.SearchFilter]
     queryset = UserSerializer.Meta.model.objects.filter(is_superuser=False)
     """
     def get_queryset(self):
          user_search = self.request.POST.get('user-search', "")
          if len(user_search) > 0 :
               return UserSerializer.Meta.model.objects.filter(last_name__icontains=user_search)
          return UserSerializer.Meta.model.objects.none()
     """

class UserSearchView(ListAPIView):
     #permission_classes = [IsAuthenticated]
     serializer_class = UserSerializer
     search_fields = ['last_name', 'first_name', 'username']
     filter_backends = [filters.SearchFilter]
     queryset = UserSerializer.Meta.model.objects.filter(is_superuser=False)
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
    p_token = None
    if not username or not token :
        logger.warning("PAYMENT REQUEST API : username or token missing")
        return Response({'error': 'username or token missing'})
    
    is_authenticated = Token.objects.filter(key=token, user__username=username)
    if not is_authenticated:
        logger.info('PAYMENT REQUEST API : User not found')
        return Response({'error': 'user not found'}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'POST':
        logger.info("API POST")
        postdata = request.POST.copy()
        form = PaymentRequestForm(postdata)
        if form.is_valid(): 
            logger.info("API POST : FORM IS VALID")
            p_token = utils.generate_token_10()
            logger.info("API POST : TOKEN FOR P REQUEST CREATED")
            form.cleaned_data['token'] = p_token
            logger.info("API POST : FORM UPDATED WITH TOKEN FOR P REQUEST")
            logger.info(form.cleaned_data)
            logger.info(postdata)
            logger.info(form.errors)
            try:
                p_request = form.save()
            except Exception as e:
                logger.info(f"PAYMENT REQUEST API : ERROR ON form.save()")
                return Response({'error': 'ERROR ON form.save()'}, status=status.HTTP_400_BAD_REQUEST)
            
            logger.info(f"PAYMENT REQUEST API : Created Payment Request from user \"{username}\"")
            return Response({'token':p_token}, status=status.HTTP_200_OK)
        else:
            logger.info(f"PAYMENT REQUEST API : Payment Request from user \"{username}\" is invalid")
            return Response({'error': 'Submitted data is invalid'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        logger.info(f"PAYMENT REQUEST API : Payment Request from user \"{username}\" rejected. Method not GET not allowed")
        return Response({'error': 'Bad Request'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


