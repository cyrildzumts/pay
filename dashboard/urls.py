from django.conf.urls import url, include
from django.urls import path, reverse_lazy
# from demosite import settings
from dashboard import views

app_name = 'dashboard'
urlpatterns = [
    path('', views.dashboard, name='home'),
    path('available_services/', views.available_services, name='available_services'),
    path('available_services/create', views.available_service_create, name='available_service_create'),
    path('available_services/update/<int:pk>/', views.available_service_update, name='available_service_update'),
    path('available_services/remove/<int:pk>/', views.available_service_remove, name='available_service_remove'),
    path('available_services/details/<int:pk>/', views.available_service_details, name='available_service_details'),
    path('cases/', views.cases, name='cases'),
    path('cases/details/<int:pk>/', views.case_details, name='case_details'),
    path('cases/close/<int:pk>/', views.case_close, name='case_close'),

    path('services/', views.services, name='services'),
    path('services/details/<int:pk>/', views.service_details, name='service_details'),
    path('transfers/', views.transfers, name='transfers'),
    path('transfers/details/<int:pk>/', views.transfer_details, name='transfer_details'),
    path('payments/', views.payments, name='payments'),
    path('payments/details/<int:pk>/', views.payment_details, name='payment_details'),
    path('policies/', views.policies, name='policies'),
    path('policies/details/<int:pk>/', views.policy_details, name='policy_details'),
    path('policies/remove/<int:pk>/', views.policy_remove, name='policy_remove'),
    path('policies/update/<int:pk>/', views.policy_update, name='policy_update'),
    path('policies/create/', views.policy_create, name='policy_create'),
    path('service_categories/', views.category_services, name='service_categories'),
    path('service_categories/details/<int:pk>/', views.category_service_details, name='service_categories_details'),
    path('service_categories/remove/<int:pk>/', views.category_service_remove, name='category_service_remove'),
    path('service_categories/update/<int:pk>/', views.category_service_update, name='category_service_update'),
    path('service_categories/create/', views.category_service_create, name='category_service_create'),
    

]