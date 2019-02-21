from django.conf.urls import url
from django.views.generic import TemplateView


urlpatterns = [
    url(r'^pins/pin-form/$', TemplateView.as_view(template_name='core/pin_form.html'),
        name='pin-form'),
    url(r'^pins/tags/(?P<tag>(\w|-)+)/$', TemplateView.as_view(template_name='core/pins.html'),
        name='tag-pins'),
    url(r'^pins/users/(?P<username>(\w|-)+)/$', TemplateView.as_view(template_name='core/pins.html'),
        name='user-pins'),
    url(r'^(?P<pin>[0-9]+)/$', TemplateView.as_view(template_name='core/pins.html'),
        name='pin-detail'),
    url(r'^$', TemplateView.as_view(template_name='core/pins.html'),
        name='recent-pins'),
]
