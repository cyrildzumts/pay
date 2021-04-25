from pay import settings
from django.contrib.auth.models import User

def site_context(request):
    is_dashboard_allowed = False
    if request.user.is_authenticated:
        is_dashboard_allowed = request.user.has_perm('dashboard.can_view_dashboard')
    
    banner = len(list(filter(lambda path: path in request.path, settings.PATH_ACCEPTING_BANNER))) > 0
    context = {
        'site_name' : settings.SITE_NAME,
        'SITE_NAME': settings.SITE_NAME,
        'meta_keywords': settings.META_KEYWORDS,
        'meta_description': settings.META_DESCRIPTION,
        'redirect_to' : '/',
        'is_dashboard_allowed' : is_dashboard_allowed,
        'dev_mode' : settings.DEV_MODE,
        'CURRENCY' : settings.CURRENCY,
        'banner' : banner
    }
    return context