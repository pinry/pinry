from django.conf import settings
from django.http import HttpResponseForbidden
from django.utils.deprecation import MiddlewareMixin


class Public(MiddlewareMixin):

    acceptable_paths = (
        "/api/v2/profile/",
    )

    def process_request(self, request):
        if settings.PUBLIC is False and not request.user.is_authenticated:
            for path in self.acceptable_paths:
                if not request.path.startswith(path):
                    return HttpResponseForbidden()
