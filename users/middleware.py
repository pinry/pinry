from django.conf import settings
from django.http import HttpResponseForbidden
from django.utils.deprecation import MiddlewareMixin
from rest_framework.authentication import SessionAuthentication
from rest_framework.exceptions import APIException
from rest_framework.request import Request
from rest_framework.settings import api_settings


def is_api_authenticated(request):
    """
    True if the request's Authorization header (a token, or Basic auth when
    it is enabled) is valid. DRF authenticates in the view, after this
    middleware, so request.user only knows about session logins here.
    """
    if "HTTP_AUTHORIZATION" not in request.META:
        return False
    authenticators = [
        cls() for cls in api_settings.DEFAULT_AUTHENTICATION_CLASSES
        if not issubclass(cls, SessionAuthentication)
    ]
    try:
        user = Request(request, authenticators=authenticators).user
    except APIException:
        return False
    return user.is_authenticated


class Public(MiddlewareMixin):

    acceptable_paths = (
        "/api/v2/profile/",
        "/admin/login/",
    )

    def process_request(self, request):
        if settings.PUBLIC is not False or request.user.is_authenticated:
            return None
        if any(request.path.startswith(path) for path in self.acceptable_paths):
            return None
        if is_api_authenticated(request):
            return None
        return HttpResponseForbidden()
