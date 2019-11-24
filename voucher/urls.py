from django.conf.urls import url, include
from django.urls import path, reverse_lazy
# from demosite import settings
from django.contrib.auth import views as auth_views
from voucher import views

app_name = 'voucher'

urlpatterns = [
    path('', views.voucher_home, name='voucher-home'),
    path('activate/<uuid:voucher_uuid>/', views.voucher_activate, name='activate'),
    path('vouchers/', views.vouchers, name='vouchers'),
    path('voucher-detail/<uuid:voucher_uuid>/', views.voucher_details, name='voucher-detail'),

    path('used-vouchers/', views.used_vouchers, name='used-vouchers'),
    path('used-voucher-detail/<uuid:voucher_uuid>/', views.used_voucher_details, name='used-voucher-detail'),

    path('sold-vouchers/', views.sold_vouchers, name='sold-vouchers'),
    path('sold-voucher-detail/<uuid:voucher_uuid>/', views.sold_voucher_details, name='sold-voucher-detail'),
    path('generate/', views.voucher_generate, name='voucher-generate'),
    path('recharge/', views.recharge_user_account_view, name='recharge'),
    path('recharges/', views.recharges, name='recharges'),
    path('recharges/<uuid:recharge_uuid>/', views.recharge_details, name='recharge-detail'),

    
]