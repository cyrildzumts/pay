from pay import settings


def site_context(request):
    context = {
        'site_name' : settings.SITE_NAME,
        'meta_keywords': settings.META_KEYWORDS,
        'meta_description': settings.META_DESCRIPTION,
        'redirect_to' : '/'
    }
    return context