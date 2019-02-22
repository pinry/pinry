from django.conf import settings


def template_settings(request):
    return {
        'API_LIMIT_PER_PAGE': settings.API_LIMIT_PER_PAGE,
    }
