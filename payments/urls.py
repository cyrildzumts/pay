from django.conf.urls import url, include
from django.urls import path, reverse_lazy
# from demosite import settings
from django.contrib.auth import views as auth_views
from payments import views

app_name = 'payments'
urlpatterns = [
    path('', views.payment_home, name='payment-home'),
    path('available-services/', views.available_services, name='available-services'),
    path('available-service-detail/<uuid:available_uuid>/', views.available_service_details, name='available-service-detail'),
    path('cases/', views.cases, name='cases'),
    path('cases/<uuid:issue_uuid>/', views.case_details, name='case-detail'),
    path('idcards/', views.idcards, name='idcards'),
    path('idcards/<uuid:idcard_uuid>/', views.idcard_details, name='idcard-detail'),

    path('new-transaction/', views.new_transaction, name='new-transaction'),
    path('new-transfer/', views.new_transfer, name='new-transfer'),
    path('new-payment/', views.new_payment, name='new-payment'),
    path('new-service/<uuid:available_service_uuid>/', views.new_service, name='new-service'),
    path('reductions/', views.reductions, name='reductions'),
    path('reductions/<uuid:reduction_uuid>/', views.reduction_details, name='reduction-detail'),
    path('service-done/', views.service_done, name='service-done'),
    path('services/', views.services, name='services'),
    path('services/<uuid:service_uuid>/', views.service_details, name='service-detail'),
    path('transaction-done/<redirected_from>/', views.transaction_done, name='transaction-done'),
    path('transfer-done/', views.transfer_done, name='transfer-done'),
    path('transactions/', views.transactions, name='transactions'),
    path('transfers/', views.transfers, name='transfers'),
    path('transactions/<uuid:transaction_uuid>/', views.transaction_details, name='transaction-detail'),
    path('transfer/<uuid:transfer_uuid>/', views.transfer_details, name='transfer-detail'),
    path('upload_idcard/', views.upload_idcard, name='upload-idcard'),
    path('idcard/update/<uuid:idcard_uuid>/', views.update_idcard, name='idcard-update'),
    path('upload-idcard/upload-idcard-done/', views.upload_idcard_done, name='upload-idcard-done'),
    path('payments/', views.payments, name='payments'),
    path('payment-done/', views.payment_done, name='payment-done'),
    path('payments/<uuid:payment_uuid>/', views.payment_details, name='payment_detail'),
    path('policies/', views.policies, name='policies'),
    path('policies/<uuid:policy_uuid>/', views.policy_details, name='policy-detail'),
    path('recharge/', views.recharge, name='recharge'),
    path('service-categories/', views.service_categories, name='service-categories'),
    path('service-categories/<uuid:category_uuid>/', views.service_category_details, name='service-categories-detail'),
    

]