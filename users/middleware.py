from django.conf import settings
from django.http import HttpResponseForbidden


class Public:

    acceptable_paths = (
        "/api/v2/profile/",
    )

    def __init__(self, get_response):
        self.get_response = get_response

    def process_request(self, request):
        if settings.PUBLIC is False and not request.user.is_authenticated():
            for path in self.acceptable_paths:
                if not request.path.startswith(path):
                    return HttpResponseForbidden()
