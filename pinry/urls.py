from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = patterns('',
                       url(r'', include('pinry.core.urls', namespace='core')),
                       url(r'', include('pinry.users.urls', namespace='users')),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
