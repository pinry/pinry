from django.conf.urls import patterns, include, url
from .api import PinResource

pin_resource = PinResource()

urlpatterns = patterns('',
    url(r'', include(pin_resource.urls)),
)
