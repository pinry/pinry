from django.conf.urls import patterns, include, url

from tastypie.api import Api

from .api import ImageResource, ThumbnailResource, PinResource, UserResource


v1_api = Api(api_name='v1')
v1_api.register(ImageResource())
v1_api.register(ThumbnailResource())
v1_api.register(PinResource())
v1_api.register(UserResource())


urlpatterns = patterns('',
    url(r'^api/', include(v1_api.urls)),
)
