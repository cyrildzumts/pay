from django.conf.urls import url, include
from django.urls import path, reverse_lazy
from rest_framework.routers import DefaultRouter
from api import views, viewsets

app_name = 'api'
router = DefaultRouter()
router.register(r'services', viewsets.ServiceViewSet)
router.register(r'transfers', viewsets.TransferViewSet)

urlpatterns = [
    path('', include(router.urls)),
    
]