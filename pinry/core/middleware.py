from django.conf import settings
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse


class Public(object):
    def process_request(self, request):
        if settings.PUBLIC == False and not request.user.is_authenticated():
            acceptable_paths = [
                '/login/',
                '/private/',
                '/register/',
            ]
            if request.path not in acceptable_paths:
                return HttpResponseRedirect(reverse('users:private'))
