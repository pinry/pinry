from django.conf import settings
from django.conf.urls import include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
from django.views.static import serve
from rest_framework.documentation import include_docs_urls

from core.views import drf_router


admin.autodiscover()


urlpatterns = [
    # drf api
    url(r'^api/v2/', include(drf_router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace="rest_framework")),
    url(r'^api/v2/docs/', include_docs_urls(title='PinryAPI', schema_url='/')),

    # old api and views
    url(r'^admin/', include(admin.site.urls)),
    url(r'', include('core.urls', namespace='core')),
    url(r'', include('users.urls', namespace='users')),
]


if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += [
        url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT, }),
    ]

if settings.IS_TEST:
    urlpatterns += staticfiles_urlpatterns()
