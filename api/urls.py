from django.conf.urls import url, include
from django.urls import path, reverse_lazy
from api import views

app_name = 'api'

urlpatterns = [
    path('', views.AvailableServiceListCreateAPIView.as_view(), name='pay_rest_api'),
    path('available_service/', views.AvailableServiceRetrieveUpdateCreateAPIView.as_view(), name='pay_rest_api'),
]