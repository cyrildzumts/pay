"""
Django settings for pay project.

Generated by 'django-admin startproject' using Django 2.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os
from django.utils.translation import ugettext_lazy as _

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

LOGIN_REDIRECT_URL = '/'
IDENTIFICATION_DOC_NAME_PREFIX = "pay_ident"

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY          =  os.environ['PAY_SECRET_KEY']

# SITE NAME SETTING
SITE_NAME           =  os.environ['PAY_SITE_NAME']

META_KEYWORDS       = "Pay, payment, buy, online-pay, africa-pay, payment solution"
META_DESCRIPTION    = "Pay Atalaku is your african solution for online payments"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG               = True
CELERY_BROKER_URL   = os.environ['PAY_CELERY_BROKER_URL']
CELERY_BACKEND      = os.environ['PAY_CELERY_BACKEND']

CELERY_DEFAULT_QUEUE = "pay-default"
CELERY_DEFAULT_EXCHANGE = "pay-default"
CELERY_DEFAULT_ROUTING_KEY = "pay-default"

CELERY_OUTGOING_MAIL_QUEUE = "pay-outgoing-mails"
CELERY_OUTGOING_MAIL_EXCHANGE = "pay-mail"
CELERY_OUTGOING_MAIL_ROUTING_KEY = "pay.mail.outgoing"

CELERY_VOUCHER_GENERATE_QUEUE = "pay-voucher-generation"
CELERY_VOUCHER_EXCHANGE = "pay-voucher"
CELERY_VOUCHER_ROUTING_KEY = "pay.voucher.generate"

CELERY_IDENTIFICATION_QUEUE = "pay-ident"
CELERY_IDENTIFICATION_EXCHANGE = "pay-ident"
CELERY_IDENTIFICATION_ROUTING_KEY = "pay.identification"
CELERY_DEFAULT_EXCHANGE_TYPE = 'direct'

CELERY_NAMESPACE = 'CELERY'

ALLOWED_HOSTS = ['localhost','http://pay-atalaku.com', 'www.pay-atalaku.com', 'pay-atalaku.com', os.environ['PAY_ALLOWED_HOST']]

#EMAIL SETTINGS
EMAIL_HOST = os.environ['PAY_EMAIL_HOST']
EMAIL_PORT = os.environ['PAY_EMAIL_PORT']
EMAIL_HOST_PASSWORD = os.environ['PAY_EMAIL_PASSWORD']
EMAIL_HOST_USER = os.environ['PAY_EMAIL_USER']
CONTACT_MAIL =  os.environ['PAY_CONTACT_MAIL']
EMAIL_USE_SSL = True
#EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

ACCOUNTS = {
    'ACCOUNT_TYPE' :  (
        ('A', 'Admin'),
        ('B', 'Business'),
        ('D', 'Developer'), # create a group Developer instead
        ('I', 'Individual'),
        ('M', 'Manager'), # create a group Manager instead
        ('P', 'Partner'), # create a group Partner instead
        ('S', 'Staff'), # create a group Staff instead
        ('R', 'Recharge'),
        ('X', 'PAY ACCOUNT'),
    )
}


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'accounts',
    'payments.apps.PaymentsConfig',
    'rest_framework',
    'rest_framework.authtoken',
    'api.apps.ApiConfig',
    'voucher.apps.VoucherConfig',
    'dashboard.apps.DashboardConfig',
    'pay.apps.PayConfig',
]

# RESTFRAMEWORK SETTINGS
REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        #'rest_framework.permissions.IsAdminUser',
        #'rest_framework.permissions.IsAuthenticated',
        #'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly',
    ],
    
    'DEFAULT_AUTHENTICATION_CLASSES': [
        #'rest_framework.authentication.BasicAuthentication',
        #'rest_framework.authentication.SessionAuthentication',
        #'rest_framework.authentication.TokenAuthentication',
    ]
}


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'pay.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.i18n',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'pay.context_processors.site_context',
                'accounts.context_processors.account_context'
            ],
        },
    },
]

WSGI_APPLICATION = 'pay.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'dev': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    },
    'production': {
	'ENGINE': 'django.db.backends.postgresql',
	'NAME'	:  os.environ['PAY_DATABASE_NAME'],
	'USER'	:  os.environ['PAY_DATABASE_USERNAME'],
	'PASSWORD':  os.environ['PAY_DATABASE_PW'],
	'HOST'	:  os.environ['PAY_DATABASE_HOST'] ,
	'PORT' 	:  os.environ['PAY_DATABASE_PORT'],
    'OPTIONS' : {
        'sslmode': 'require'
    },
    'TEST'  :{
        'NAME': 'test_db',
    },
   },

}

DEFAULT_DATABASE = os.environ.get('DJANGO_DATABASE', 'dev')
DATABASES['default'] = DATABASES[DEFAULT_DATABASE]
DEV_MODE = True

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# LOGGER
"""
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
        },
    },
}
"""
###############

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'console': {
            'format': '{asctime} {levelname} {module} {message}',
            'style': '{',
        },
        'file': {
            'format': '{asctime} {levelname} {module} {message}',
            'style': '{',
        },
    },

    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'console'
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'formatter': 'file',
            'filename':'pay.log'
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        '' : {
            'level': 'DEBUG',
            'handlers': ['console', 'file'],
            'propagate': False,
        },
        'django': {
            'level': 'INFO',
            'handlers': ['file'],
            'propagate': True,
        },
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        }
    }
}

###############

# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'fr'
LANGUAGES = (
    ('en',_('English')),
    ('fr',_('French')),
)
LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'conf/locale')
]
TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "static/")
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "staticfiles"),
)
