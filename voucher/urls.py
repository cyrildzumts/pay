from django.conf.urls import url, include
from django.urls import path, reverse_lazy
# from demosite import settings
from django.contrib.auth import views as auth_views
from voucher import views

app_name = 'voucher'

urlpatterns = [
    path('', views.voucher_home, name='voucher_home'),
    path('vouchers/', views.vouchers, name='vouchers'),
    path('voucher_details/<int:pk>/', views.voucher_details, name='voucher_details'),

    path('used_vouchers/', views.used_vouchers, name='used_vouchers'),
    path('used_voucher_details/<int:pk>/', views.used_voucher_details, name='used_voucher_details'),

    path('sold_vouchers/', views.sold_vouchers, name='sold_vouchers'),
    path('sold_voucher_details/<int:pk>/', views.sold_voucher_details, name='sold_voucher_details'),
]