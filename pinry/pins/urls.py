from django.conf.urls import patterns, url


urlpatterns = patterns('pinry.pins.views',
    url(r'^$', 'recent_pins', name='recent-pins'),
    url(r'^tag/.+/$', 'recent_pins', name='tag'),
    url(r'^new-pin/$', 'new_pin', name='new-pin'),
    url(r'^delete-pin/(?P<pin_id>\d+)/$', 'delete_pin', name='delete-pin'),
)
