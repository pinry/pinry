from django.conf.urls import patterns, include, url

from tastypie.api import Api

from .api import ImageResource, ThumbnailResource, PinResource, UserResource
from .views import CreateUser


v1_api = Api(api_name='v1')
v1_api.register(ImageResource())
v1_api.register(ThumbnailResource())
v1_api.register(PinResource())
v1_api.register(UserResource())


urlpatterns = patterns('',
)


urlpatterns = patterns('',
    url(r'^api/', include(v1_api.urls, namespace='api')),

    url(r'^$', 'pinry.core.views.home', name='home'),

    url(r'^private/$', 'pinry.core.views.private', name='private'),
    url(r'^login/$', 'django.contrib.auth.views.login',
        {'template_name': 'user/login.html'}, name='login'),
    url(r'^logout/$', 'pinry.core.views.logout_user', name='logout'),
    url(r'^register/$', CreateUser.as_view(), name='register'),
)
