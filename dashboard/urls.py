from django.conf.urls import url, include
from django.urls import path, reverse_lazy
# from demosite import settings
from dashboard import views

app_name = 'dashboard'
urlpatterns = [
    path('', views.dashboard, name='home'),
    path('available-services/', views.available_services, name='available-services'),
    path('available-services/create/', views.available_service_create, name='available-service-create'),
    path('available-services/update/<uuid:available_uuid>/', views.available_service_update, name='available-service-update'),
    path('available-services/remove/<uuid:available_uuid>/', views.available_service_remove, name='available-service-remove'),
    path('available-services/remove-all/', views.available_service_remove_all, name='available-service-remove-all'),
    path('available-services/detail/<uuid:available_uuid>/', views.available_service_details, name='available-service-detail'),
    path('cases/', views.cases, name='cases'),
    path('cases/detail/<issue_uuid>/', views.case_details, name='case-detail'),
    path('cases/close/<issue_uuid>/', views.case_close, name='case-close'),
    path('create-account/',views.create_account, name='create-account'),
    path('generate-token/', views.generate_token, name='generate-token'),
    path('group-create/',views.group_create, name='group-create'),
    path('group-detail/<int:pk>/',views.group_detail, name='group-detail'),
    path('group-delete/<int:pk>/',views.group_delete, name='group-delete'),
    path('group-update/<int:pk>/',views.group_update, name='group-update'),
    path('groups/',views.groups, name='groups'),
    path('services/', views.services, name='services'),
    path('services/detail/<service_uuid>/', views.service_details, name='service-detail'),
    path('transfers/', views.transfers, name='transfers'),
    path('transfers/detail/<uuid:transfer_uuid>/', views.transfer_details, name='transfer-detail'),
    path('payments/', views.payments, name='payments'),
    path('payments/detail/<uuid:payment_uuid>/', views.payment_details, name='payment-detail'),
    path('policies/', views.policies, name='policies'),
    path('policies/detail/<uuid:policy_uuid>/', views.policy_details, name='policy-detail'),
    path('policies/remove/<uuid:policy_uuid>/', views.policy_remove, name='policy-remove'),
    path('policies/remove-all/', views.policy_remove_all, name='policy-remove-all'),
    path('policies/update/<uuid:policy_uuid>/', views.policy_update, name='policy-update'),
    path('policies/create/', views.policy_create, name='policy-create'),

    path('policy-groups/', views.policy_groups, name='policy-groups'),
    path('policy-groups/detail/<uuid:group_uuid>/', views.policy_group_details, name='policy-group-detail'),
    path('policy-groups/remove/<uuid:group_uuid>/', views.policy_group_remove, name='policy-group-remove'),
    #path('policy-groups/remove-all/', views.policy_remove_all, name='policy-group-remove-all'),
    path('policy-groups/update/<uuid:group_uuid>/', views.policy_group_update, name='policy-group-update'),
    path('policy-groups/create/', views.policy_group_create, name='policy-group-create'),

    path('category-services/', views.category_services, name='category-services'),
    path('category-services/detail/<uuid:category_uuid>/', views.category_service_details, name='category-service-detail'),
    path('category-services/remove/<uuid:category_uuid>/', views.category_service_remove, name='category-service-remove'),
    path('category-services/remove-all/', views.category_service_remove_all, name='category-service-remove-all'),
    path('category-services/update/<uuid:category_uuid>/', views.category_service_update, name='category-service-update'),
    path('category-services/create/', views.category_service_create, name='category-service-create'),
    
]