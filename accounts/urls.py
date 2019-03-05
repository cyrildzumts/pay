from django.conf.urls import url, include
from django.urls import path
# from demosite import settings
from django.contrib.auth import views as auth_views
from accounts import views

app_name = 'accounts'
urlpatterns = [
    path('', views.user_account, name='account'),
    path('register/', views.register, name='register'),
    path('edit_user/<int:pk>/', views.edit_account, name='edit_account'),
    #url(r'^login', views.login, name='login'),
    #url(r'^logout', views.logout, name='logout'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeView.as_view(), name='password_change_done'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetView.as_view(), name='password_reset_done'),
]