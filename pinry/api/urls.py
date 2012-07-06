from django.conf.urls import patterns, include, url

from .api import PinResource
from .api import UserResource


pin_resource = PinResource()
user_resource = UserResource()


urlpatterns = patterns('',
    url(r'', include(pin_resource.urls)),
    url(r'', include(user_resource.urls)),
)
