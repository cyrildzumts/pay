from django.conf.urls import url, include
from django.urls import path, reverse_lazy
# from demosite import settings
from django.contrib.auth import views as auth_views
from accounts import views

app_name = 'accounts'
urlpatterns = [
    path('', views.user_account, name='account'),
    path('account_details/<int:pk>/', views.account_details, name='account_details'),
    path('available_services/', views.available_services, name='available_services'),
    path('available_service_details/<int:pk>/', views.available_service_details, name='available_service_details'),
    path('cases/', views.cases, name='cases'),
    path('cases/<int:pk>/', views.case_details, name='case_details'),
    #path('edit_account/<int:pk>/', views.edit_account, name='edit_account'),
    path('idcards/', views.idcards, name='idcards'),
    path('idcards/<int:pk>/', views.idcard_details, name='idcard_details'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('new_transaction/', views.new_transaction, name='new_transaction'),
    path('new_transfer/', views.new_transfer, name='new_transfer'),
    path('new_payment/', views.new_payment, name='new_payment'),
    path('new_service/', views.new_service, name='new_service'),
    path('password_change/', views.password_change_views, name='password_change'),
    path('password_change_done/', views.password_change_done_views, name='password_change_done'),
    path('password_reset/', auth_views.PasswordResetView.as_view(success_url=reverse_lazy('accounts:password_reset_done')), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('register/', views.register, name='register'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(success_url=reverse_lazy('accounts:password_reset_complete')), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('reductions/', views.reductions, name='reductions'),
    path('reductions/<int:pk>', views.reduction_details, name='reduction_details'),
    path('service_done/', views.service_done, name='service_done'),
    path('services/', views.services, name='services'),
    path('services/<int:pk>/', views.service_details, name='service_details'),
    path('transaction_done/', views.transaction_done, name='transaction_done'),
    path('transfer_done/', views.transfer_done, name='transfer_done'),
    path('transactions/', views.transactions, name='transactions'),
    path('transfers/', views.transfers, name='transfers'),
    path('transactions/<int:pk>/', views.transaction_details, name='transaction_details'),
    path('transfer/<int:pk>/', views.transfer_details, name='transfer_details'),
    path('payments/', views.payments, name='payments'),
    path('payment_done/', views.payment_done, name='payment_done'),
    path('payments/<int:pk>/', views.payment_details, name='payment_details'),
    path('policies/', views.policies, name='policies'),
    path('policies/<int:pk>', views.policy_details, name='policy_details'),
    path('service_categories/', views.service_categories, name='service_categories'),
    path('service_categories/<int:pk>/', views.service_category_details, name='service_categories_details'),
    

]