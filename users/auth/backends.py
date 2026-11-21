from django.contrib.auth.backends import ModelBackend
from django.core.exceptions import PermissionDenied

from users.auth.throttling import LoginRateThrottle
from users.models import User


class CombinedAuthBackend(ModelBackend):
    """
    Lets users log in with their email address as well as their username.

    Emails are not unique, so the password is checked against every active
    account with that email, and the login succeeds only when exactly one
    of them matches. Anything else returns None, so the next backend
    (ModelBackend) can still try the value as a username.

    This backend is listed first, so it also enforces the login throttle
    for every password check (the SPA login, the admin and api-auth
    logins, Basic auth): PermissionDenied makes Django skip the remaining
    backends.
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        if request is not None and not LoginRateThrottle().allow_request(request):
            raise PermissionDenied
        if not isinstance(username, str) or "@" not in username or password is None:
            return None
        matches = [
            user
            for user in User.objects.filter(email__iexact=username)
            if self.user_can_authenticate(user) and user.check_password(password)
        ]
        if len(matches) == 1:
            return matches[0]
        return None
