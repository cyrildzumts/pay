from django.conf.urls import url, include
from django.urls import path, reverse_lazy
# from demosite import settings
from dashboard import views

app_name = 'dashboard'
urlpatterns = [
    path('', views.dashboard, name='home'),
    path('available_services/', views.available_services, name='available_services'),
    path('available_services/create/', views.available_service_create, name='available_service_create'),
    path('available_services/update/<int:uuid>/', views.available_service_update, name='available_service_update'),
    path('available_services/remove/<int:uuid>/', views.available_service_remove, name='available_service_remove'),
    path('available_services/details/<int:uuid>/', views.available_service_details, name='available_service_details'),
    path('cases/', views.cases, name='cases'),
    path('cases/details/<int:uuid>/', views.case_details, name='case_details'),
    path('cases/close/<int:uuid>/', views.case_close, name='case_close'),

    path('services/', views.services, name='services'),
    path('services/details/<int:uuid>/', views.service_details, name='service_details'),
    path('transfers/', views.transfers, name='transfers'),
    path('transfers/details/<int:uuid>/', views.transfer_details, name='transfer_details'),
    path('payments/', views.payments, name='payments'),
    path('payments/details/<int:uuid>/', views.payment_details, name='payment_details'),
    path('policies/', views.policies, name='policies'),
    path('policies/details/<int:uuid>/', views.policy_details, name='policy_details'),
    path('policies/remove/<int:uuid>/', views.policy_remove, name='policy_remove'),
    path('policies/update/<int:uuid>/', views.policy_update, name='policy_update'),
    path('policies/create/', views.policy_create, name='policy_create'),
    path('category_services/', views.category_services, name='category_services'),
    path('category_services/details/<int:uuid>/', views.category_service_details, name='category_service_details'),
    path('category_services/remove/<int:uuid>/', views.category_service_remove, name='category_service_remove'),
    path('category_services/update/<int:uuid>/', views.category_service_update, name='category_service_update'),
    path('category_services/create/', views.category_service_create, name='category_service_create'),
    

]