"""pay URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import url, include
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from pay import views


urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('accounts/', include('accounts.urls')),
    path('admin/', admin.site.urls),
    path('api/', include('api.urls', namespace='api')),
    path('api/api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('dashboard/',include('dashboard.urls')),
    path('faq/', views.faq, name='faq'),
    path('index/', views.home, name='index'),
    path('i18n/', include('django.conf.urls.i18n')),
    path('voucher/', include('voucher.urls')),
#   path('issues/', include('issues.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
