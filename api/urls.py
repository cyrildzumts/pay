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

partners_urlpatterns = [
    path('V1/payments/',views.dummy),
    path('V1/payments/<str:description>/',views.dummy),
    path('V1/payments/<uuid:payment_uuid>/',views.dummy),
    path('V1/payments/refund/<uuid:payment_uuid>/',views.dummy),

    path('V1/transfers/<str:description>/',views.dummy),
    path('V1/transfers/<uuid:transfer_uuid>/',views.dummy),

    path('V1/refunds/',views.dummy),
    path('V1/refunds/<uuid:refund_uuid>/',views.dummy),
    path('V1/refunds/<uuid:refund_uuid>/accept/',views.dummy),
    path('V1/refunds/<uuid:refund_uuid>/decline/',views.dummy),
    path('V1/refunds/accept/',views.dummy),
    path('V1/refunds/decline/',views.dummy),

    path('V1/refunds/accepted/',views.dummy),
    path('V1/refunds/declined/',views.dummy),

    path('V1/refunds/<uuid:refund_uuid>/',views.dummy),
    path('V1/refunds/<uuid:payment_uuid>/',views.dummy),

    path('V1/recharge/<str:username>/',views.dummy),
    path('V1/transfers/<uuid:transfer_uuid>/',views.dummy),
    path('V1/transfers/refund/<uuid:transfer_uuid>/',views.dummy),

    path('V1/user-search/', views.UserSearchView.as_view()),
    path('V1/payment-request/<str:username>/<str:token>/', views.payment_request)
]

urlpatterns = [
    path('', include(router.urls)),
    path('analytics/', views.analytics_data, name='analytics'),
    path('api-token-auth/', drf_api_views.obtain_auth_token, name='api-token-auth'),
    path('dummy/', views.dummy, name='dummy'),
    path('user-search/', views.UserSearchView.as_view(), name="user-search"),
    path('payment-request/<str:username>/<str:token>/', views.payment_request, name="payment-request")
]