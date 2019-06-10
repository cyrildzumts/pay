from django.conf.urls import url, include
from django.urls import path, reverse_lazy
# from demosite import settings
from django.contrib.auth import views as auth_views
from accounts import views

app_name = 'accounts'
urlpatterns = [
    path('', views.user_account, name='account'),
    path('available_services/', views.available_services, name='available_services'),
    path('cases/', views.cases, name='cases'),
    path('cases/<int:pk>', views.case_details, name='case_details'),
    path('edit_account/<int:pk>/', views.edit_account, name='edit_account'),
    path('idcards/', views.idcards, name='idcards'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('password_change/', views.password_change_views, name='password_change'),
    path('password_change_done/', views.password_change_done_views, name='password_change_done'),
    path('password_reset/', auth_views.PasswordResetView.as_view(success_url=reverse_lazy('accounts:password_reset_done')), name='password_reset'),
    path('password_reset_done', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('register/', views.register, name='register'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(success_url=reverse_lazy('accounts:password_reset_complete')), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('reductions/', views.reductions, name='reductions'),
    path('reductions/<int:pk>', views.reduction_details, name='reduction_details'),
    path('services/', views.services, name='services'),
    path('services/<int:pk>', views.service_details, name='service_details'),
    path('transactions/', views.transactions, name='transactions'),
    path('transactions/<int:pk>', views.transaction_details, name='transaction_details'),
    path('transactions/done', views.transaction_done, name='transactions_done'),

    path('payments/', views.payments, name='payments'),
    path('payments/<int:pk>', views.payment_details, name='payment_details'),
    path('policies/', views.policies, name='policies'),
    path('policies/<int:pk>', views.policy_details, name='policy_details'),
    path('service_categories/', views.service_categories, name='service_categories'),
    path('service_categories/<int:pk>', views.service_category_details, name='service_categories_details'),
    

]