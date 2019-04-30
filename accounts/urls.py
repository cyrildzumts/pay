from django.conf.urls import url, include
from django.urls import path
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
    path('services/', views.services, name='services'),
    path('transactions/', views.transactions, name='transactions'),
]