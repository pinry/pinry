from django.conf import settings
from django.conf.urls import include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
from django.views.static import serve

admin.autodiscover()


urlpatterns = [
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
    # For test running of django_images
    urlpatterns += [
        url(r'^__images/', include('django_images.urls')),
    ]
