from django.conf.urls import url, include
from django.urls import path, reverse_lazy
from django.views.generic.dates import ArchiveIndexView
from django.contrib.auth import views as auth_views
from payments import views

app_name = 'payments'
urlpatterns = [
    path('', views.payment_home, name='payment-home'),
    path('available-services/', views.available_services, name='available-services'),
    path('available-service-detail/<uuid:available_uuid>/', views.available_service_details, name='available-service-detail'),
    path('activities/', views.activities , name='activities'),
    path('activities/details/<uuid:history_uuid>/', views.activity_details , name='activity-details'),
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

    path('services/archive/', views.ServiceArchiveIndexView.as_view(), name='service-archive'),
    path('services/archive/<int:year>/', views.ServiceYearArchiveView.as_view(), name='service-year-archive'),
    path('services/archive/<int:year>/<int:month>/', views.ServiceMonthArchiveView.as_view(month_format="%m"), name='service-month-archive'),
    path('services/archive/<int:year>/<str:month>/', views.ServiceMonthArchiveView.as_view(), name='service-month-archive'),

    path('services/archive/<int:year>/<int:month>/<int:day>/', views.ServiceDayArchiveView.as_view(month_format="%m"), name='service-day-archive'),
    path('services/archive/<int:year>/<str:month>/<int:day>/', views.ServiceDayArchiveView.as_view(), name='service-day-archive'),

    path('transaction-done/<redirected_from>/', views.transaction_done, name='transaction-done'),
    path('transfer-done/', views.transfer_done, name='transfer-done'),
    path('transaction-done/', views.transaction_done, name='transaction-done'),
    path('transactions/', views.transactions, name='transactions'),
    path('transactions/archive/', views.transaction_archive, name='transaction-archive'),
    path('transfers/', views.transfers, name='transfers'),
    path('transfers/archive/', views.TransferArchiveIndexView.as_view(), name='transfer-archive'),
    path('transfers/archive/<int:year>/', views.TransferYearArchiveView.as_view(), name='transfer-year-archive'),
    path('transfers/archive/<int:year>/<int:month>/', views.TransferMonthArchiveView.as_view(month_format="%m"), name='transfer-month-archive'),
    path('transfers/archive/<int:year>/<str:month>/', views.TransferMonthArchiveView.as_view(), name='transfer-month-archive'),

    path('transfers/archive/<int:year>/<int:month>/<int:day>/', views.TransferDayArchiveView.as_view(month_format="%m"), name='transfer-day-archive'),
    path('transfers/archive/<int:year>/<str:month>/<int:day>/', views.TransferDayArchiveView.as_view(), name='transfer-day-archive'),
    
    path('transfers/archive/today/', views.TransferTodayArchiveView.as_view(), name='transfer-today-archive'),
    path('transactions/<uuid:transaction_uuid>/', views.transaction_details, name='transaction-detail'),
    path('transfer/<uuid:transfer_uuid>/', views.transfer_details, name='transfer-detail'),
    path('upload-idcard/', views.upload_idcard, name='upload-idcard'),
    path('idcard/update/<uuid:idcard_uuid>/', views.update_idcard, name='idcard-update'),
    path('upload-idcard/upload-idcard-done/', views.upload_idcard_done, name='upload-idcard-done'),
    path('payments/', views.payments, name='payments'),
    path('payment-done/', views.payment_done, name='payment-done'),
    path('payments/<uuid:payment_uuid>/', views.payment_details, name='payment-detail'),
    path('refunds/', views.refunds, name='refunds'),
    path('refund/<uuid:refund_uuid>/', views.refund_detail, name='refund-detail'),
    path('refund/create/<uuid:payment_uuid>/', views.create_refund, name='create-refund'),
    path('refund/accept/<uuid:payment_uuid>/', views.accept_refund, name='accept-refund'),
    path('refund/decline/<uuid:payment_uuid>/', views.declined_refund, name='decline-refund'),

    path('payment-request/<uuid:request_uuid>/', views.payment_request, name='payment-request'),
    path('payment-requests/decline/<uuid:request_uuid>/', views.decline_payment_request, name="payment-request-decline"),
    path('payment-requests/accept/<uuid:request_uuid>/', views.accept_payment_request, name="payment-request-accept"),
    path('payment-requests/done/<uuid:request_uuid>/<int:succeed>/', views.payment_request_done, name="payment-request-done"),

    path('payments/archive/', ArchiveIndexView.as_view(model=views.Payment,date_field="created_at"), name='payment-archive'),
    path('payments/archive/<int:year>/', views.PaymentYearArchiveView.as_view(), name='payment-year-archive'),
    path('payments/archive/<int:year>/<int:month>/', views.PaymentMonthArchiveView.as_view(month_format="%m"), name='payment-month-archive'),
    path('payments/archive/<int:year>/<str:month>/', views.PaymentMonthArchiveView.as_view(), name='payment-month-archive'),
    
    path('payments/archive/<int:year>/<int:month>/<int:day>/', views.PaymentDayArchiveView.as_view(month_format="%m"), name='payment-day-archive'),
    path('payments/archive/<int:year>/<str:month>/<int:day>/', views.PaymentDayArchiveView.as_view(), name='payment-day-archive'),
    path('payments/payment-verification/', views.payment_verify, name='payment-verification'),
    path('payments/service-verification/', views.service_verify, name='service-verification'),
    path('payments/transfer-verification/', views.transfer_verify, name='transfer-verification'),
    path('payments/transaction-verification/', views.transaction_verification, name='transaction-verification'),
    path('policies/', views.policies, name='policies'),
    path('policies/<uuid:policy_uuid>/', views.policy_details, name='policy-detail'),
    path('policy-group-update/', views.seller_policygroup_update, name='policy-group-update'),
    path('recharge/', views.recharge, name='recharge'),
    path('service-categories/', views.service_categories, name='service-categories'),
    path('service-categories/<uuid:category_uuid>/', views.service_category_details, name='service-categories-detail'),

]