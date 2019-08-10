from django.conf.urls import url, include
from django.urls import path, reverse_lazy
# from demosite import settings
from dashboard import views

app_name = 'dashboard'
urlpatterns = [
    path('', views.dashboard, name='home'),
    path('available_services/', views.available_services, name='available_services'),
    path('available_service_details/<int:pk>/', views.available_service_details, name='available_service_details'),
   # path('cases/', views.cases, name='cases'),
   # path('cases/<int:pk>/', views.case_details, name='case_details'),
   # path('idcards/', views.idcards, name='idcards'),
   # path('idcards/<int:pk>/', views.idcard_details, name='idcard_details'),
   # path('reductions/', views.reductions, name='reductions'),
   # path('reductions/<int:pk>/', views.reduction_details, name='reduction_details'),
    path('services/', views.services, name='services'),
    path('services/<int:pk>/', views.service_details, name='service_details'),
    #path('transactions/', views.transactions, name='transactions'),
    path('transfers/', views.transfers, name='transfers'),
    #path('transactions/<int:pk>/', views.transaction_details, name='transaction_details'),
   # path('transfer/<int:pk>/', views.transfer_details, name='transfer_details'),
    #path('upload_idcard/', views.upload_idcard, name='upload_idcard'),
   # path('idcard/update/<int:pk>/', views.update_idcard, name='idcard_update'),
   # path('payments/', views.payments, name='payments'),
   # path('payments/<int:pk>/', views.payment_details, name='payment_details'),
    path('policies/', views.policies, name='policies'),
    path('policies/<int:pk>/', views.policy_details, name='policy_details'),
   # path('recharge/', views.recharge, name='recharge'),
    path('service_categories/', views.service_categories, name='service_categories'),
    path('service_categories/<int:pk>/', views.service_category_details, name='service_categories_details'),
    

]