from django.shortcuts import render
from rest_framework.generics import (
    ListCreateAPIView,
    ListAPIView,
    RetrieveUpdateDestroyAPIView
)
from rest_framework.permissions import IsAuthenticated
from api.serializers import AvailableServiceSerializer, AvailableService


# Create your views here.
# REST API Views
class AvailableServiceListAPIView(generics.ListAPIView):
    queryset =  AvailableService.objects.all()
    serializer_class =  AvailableServiceSerializer


class AvailableServiceListCreateAPIView(ListCreateAPIView):
    queryset = AvailableService.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class =  AvailableServiceSerializer


class AvailableServiceRetrieveUpdateCreateAPIView(RetrieveUpdateDestroyAPIView):
    queryset = AvailableService.objects.all()
    permission_classes = (IsAuthenticated, )
    serializer_class =  AvailableServiceSerializer