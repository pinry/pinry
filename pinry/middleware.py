from django.middleware.csrf import get_token


class ForceCSRFCookieMiddleware:
    def process_request(self, request):
        if "CSRF_TOKEN" not in request.META:
            get_token(request)
        else:
            if request.method != "GET":
                get_token(request)
                return
