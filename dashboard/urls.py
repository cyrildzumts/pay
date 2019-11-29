from django.conf.urls import url, include
from django.urls import path, reverse_lazy
# from demosite import settings
from dashboard import views

app_name = 'dashboard'
urlpatterns = [
    path('', views.dashboard, name='home'),
    path('available_services/', views.available_services, name='available_services'),
    path('available_services/create/', views.available_service_create, name='available_service_create'),
    path('available_services/update/<uuid:available_uuid>/', views.available_service_update, name='available_service_update'),
    path('available_services/remove/<uuid:available_uuid>/', views.available_service_remove, name='available_service_remove'),
    path('available_services/detail/<uuid:available_uuid>/', views.available_service_details, name='available_service_detail'),
    path('cases/', views.cases, name='cases'),
    path('cases/detail/<issue_uuid>/', views.case_details, name='case_detail'),
    path('cases/close/<issue_uuid>/', views.case_close, name='case_close'),
    path('generate-token/', views.generate_token, name='generate-token'),
    path('group-create/',views.group_create, name='group-create'),
    path('services/', views.services, name='services'),
    path('services/detail/<service_uuid>/', views.service_details, name='service_detail'),
    path('transfers/', views.transfers, name='transfers'),
    path('transfers/detail/<uuid:transfer_uuid>/', views.transfer_details, name='transfer_detail'),
    path('payments/', views.payments, name='payments'),
    path('payments/detail/<uuid:payment_uuid>/', views.payment_details, name='payment_detail'),
    path('policies/', views.policies, name='policies'),
    path('policies/detail/<uuid:policy_uuid>/', views.policy_details, name='policy_detail'),
    path('policies/remove/<uuid:policy_uuid>/', views.policy_remove, name='policy_remove'),
    path('policies/update/<uuid:policy_uuid>/', views.policy_update, name='policy_update'),
    path('policies/create/', views.policy_create, name='policy_create'),
    path('category_services/', views.category_services, name='category_services'),
    path('category_services/detail/<uuid:category_uuid>/', views.category_service_details, name='category_service_detail'),
    path('category_services/remove/<uuid:category_uuid>/', views.category_service_remove, name='category_service_remove'),
    path('category_services/update/<uuid:category_uuid/', views.category_service_update, name='category_service_update'),
    path('category_services/create/', views.category_service_create, name='category_service_create'),
    

]