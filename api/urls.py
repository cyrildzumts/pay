from django.conf.urls import url, include
from django.urls import path, reverse_lazy
from rest_framework.routers import DefaultRouter
from api import views, viewsets

app_name = 'api'
router = DefaultRouter()
router.register(r'accounts', viewsets.AccountViewSet)
router.register(r'business_accounts', viewsets.BusinessAccountViewSet)
router.register(r'available_service', viewsets.AvailableServiceViewSet)
router.register(r'caseissues', viewsets.CaseIssueViewSet)
router.register(r'services', viewsets.ServiceViewSet)
router.register(r'transfers', viewsets.TransferViewSet)
router.register(r'services', viewsets.ServiceViewSet)
router.register(r'policies', viewsets.PolicyViewSet)
router.register(r'categories', viewsets.ServiceCategoryViewSet)
router.register(r'vouchers', viewsets.VoucherViewSet)
router.register(r'used_vouchers', viewsets.UsedVoucherViewSet)
router.register(r'sold_vouchers', viewsets.SoldVoucherViewSet)
router.register(r'user-search', viewsets.UserSearchViewSet)

urlpatterns = [
    path('', include(router.urls)),
    
]