"""
WSGI config for pay project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
import logging

logger = logging.getLogger(__name__)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pay.settings')
logger.debug(f"DATABASE HOST : {os.environ['PAY_DATABASE_HOST']}")

application = get_wsgi_application()
