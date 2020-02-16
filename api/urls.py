from django.conf.urls import url, include
from django.urls import path, reverse_lazy
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views as drf_api_views
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


urlpatterns = [
    path('', include(router.urls)),
    path('api-token-auth/', drf_api_views.obtain_auth_token, name='api-token-auth'),
    path('user-search/', views.UserSearchView.as_view(), name="user-search"),
    path('payment-request/<str:username>/<str:token>/')
]