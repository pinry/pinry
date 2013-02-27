from django.conf.urls import patterns, url
from django.views.generic import TemplateView

from .views import CreateImage


urlpatterns = patterns('pinry.pins.views',
    url(r'^pin-form/$', TemplateView.as_view(template_name='core/pin_form.html'),
        name='pin-form'),
    url(r'^upload-pin/$', CreateImage.as_view(), name='upload-pin'),
    url(r'^tag/(?P<tag>(\w|-)+)/$', TemplateView.as_view(template_name='core/pins.html'),
        name='tag-pins'),
    url(r'^$', TemplateView.as_view(template_name='core/pins.html'),
        name='recent-pins'),
)
