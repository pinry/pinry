from django.conf import settings


def template_settings(request):
    return {
        'SITE_NAME': settings.SITE_NAME,
        'API_LIMIT_PER_PAGE': settings.API_LIMIT_PER_PAGE,
    }

