from django.conf import settings
from django.contrib.auth.signals import user_login_failed
from django.dispatch import receiver
from rest_framework.authentication import BasicAuthentication
from rest_framework.exceptions import Throttled
from rest_framework.throttling import SimpleRateThrottle


class LoginRateThrottle(SimpleRateThrottle):
    """
    Limits failed password checks per client address.

    Only failures count, so people sharing an address (or a reverse proxy)
    are not locked out by each other's successful logins. The rate is
    REST_FRAMEWORK["DEFAULT_THROTTLE_RATES"]["login"].
    """
    scope = "login"

    def get_cache_key(self, request, view):
        return self.cache_format % {
            "scope": self.scope,
            "ident": self.get_ident(request),
        }

    def allow_request(self, request, view=None):
        if self.rate is None:
            return True
        self.key = self.get_cache_key(request, view)
        self.history = self.cache.get(self.key, [])
        self.now = self.timer()
        while self.history and self.history[-1] <= self.now - self.duration:
            self.history.pop()
        return len(self.history) < self.num_requests

    def record_failure(self):
        self.history.insert(0, self.now)
        self.cache.set(self.key, self.history, self.duration)


@receiver(user_login_failed)
def count_login_failure(sender, credentials, request=None, **kwargs):
    if request is None:
        return
    throttle = LoginRateThrottle()
    # Failures while already throttled are not stored, so a flood of
    # attempts can't grow the history without bound.
    if throttle.allow_request(request):
        throttle.record_failure()


class OptionalBasicAuthentication(BasicAuthentication):
    """
    HTTP Basic auth, only when settings.ALLOW_BASIC_AUTH is True. Answers
    429 instead of 401 while the client address is throttled.
    """

    def authenticate(self, request):
        if not getattr(settings, "ALLOW_BASIC_AUTH", False):
            return None
        auth = request.META.get("HTTP_AUTHORIZATION", "")
        if not auth.lower().startswith("basic "):
            return None
        throttle = LoginRateThrottle()
        if not throttle.allow_request(request):
            raise Throttled(wait=throttle.wait())
        return super().authenticate(request)

    def authenticate_header(self, request):
        if not getattr(settings, "ALLOW_BASIC_AUTH", False):
            return None
        return super().authenticate_header(request)
