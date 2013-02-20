from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = patterns('',
    url(r'^api/', include('pinry.api.urls', namespace='api')),
    url(r'^pins/', include('pinry.pins.urls', namespace='pins')),
    url(r'', include('pinry.core.urls', namespace='core')),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
