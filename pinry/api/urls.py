from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
    url(r'^pins/recent/(?P<page>\d*)/$', 'pinry.api.views.pins_recent', name='pins-recent'),
)
