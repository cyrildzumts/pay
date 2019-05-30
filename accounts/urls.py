from django.conf.urls import url, include
from django.urls import path, reverse_lazy
# from demosite import settings
from django.contrib.auth import views as auth_views
from accounts import views

app_name = 'accounts'
urlpatterns = [
    path('', views.user_account, name='account'),
    path('register/', views.register, name='register'),
    path('edit_account/<int:pk>/', views.edit_account, name='edit_account'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('password_change/', views.password_change_views, name='password_change'),
    path('password_change_done/', views.password_change_done_views, name='password_change_done'),
    path('password_reset/', auth_views.PasswordResetView.as_view(success_url=reverse_lazy('accounts:password_reset_done')), name='password_reset'),
    path('password_reset_done', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(success_url=reverse_lazy('accounts:password_reset_complete')), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('services/', views.services, name='services'),
    path('transactions/', views.transactions, name='transactions'),
    path('transactions/done', views.transaction_done, name='transactions_done'),
]