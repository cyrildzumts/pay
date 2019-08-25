from django.conf.urls import url, include
from django.urls import path, reverse_lazy
# from demosite import settings
from dashboard import views

app_name = 'dashboard'
urlpatterns = [
    path('', views.dashboard, name='home'),
    path('available_services/', views.available_services, name='available_services'),
    path('available_services/create/', views.available_service_create, name='available_service_create'),
    path('available_services/update/<int:pk>/', views.available_service_update, name='available_service_update'),
    path('available_services/remove/<int:pk>/', views.available_service_remove, name='available_service_remove'),
    path('available_services/detail/<int:pk>/', views.available_service_details, name='available_service_detail'),
    path('cases/', views.cases, name='cases'),
    path('cases/detail/<int:pk>/', views.case_details, name='case_detail'),
    path('cases/close/<int:pk>/', views.case_close, name='case_close'),

    path('services/', views.services, name='services'),
    path('services/detail/<int:pk>/', views.service_details, name='service_detail'),
    path('transfers/', views.transfers, name='transfers'),
    path('transfers/detail/<int:pk>/', views.transfer_details, name='transfer_detail'),
    path('payments/', views.payments, name='payments'),
    path('payments/detail/<int:pk>/', views.payment_details, name='payment_detail'),
    path('policies/', views.policies, name='policies'),
    path('policies/detail/<int:pk>/', views.policy_details, name='policy_detail'),
    path('policies/remove/<int:pk>/', views.policy_remove, name='policy_remove'),
    path('policies/update/<int:pk>/', views.policy_update, name='policy_update'),
    path('policies/create/', views.policy_create, name='policy_create'),
    path('category_services/', views.category_services, name='category_services'),
    path('category_services/detail/<int:pk>/', views.category_service_details, name='category_service_detail'),
    path('category_services/remove/<int:pk>/', views.category_service_remove, name='category_service_remove'),
    path('category_services/update/<int:pk>/', views.category_service_update, name='category_service_update'),
    path('category_services/create/', views.category_service_create, name='category_service_create'),
    

]