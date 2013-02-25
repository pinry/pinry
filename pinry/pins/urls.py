from django.conf.urls import patterns, url

from .views import RecentPins
from .views import NewPin


urlpatterns = patterns('pinry.pins.views',
    url(r'^$', RecentPins.as_view(), name='recent-pins'),
    url(r'^tag/.+/$', RecentPins.as_view(), name='tag'),
    url(r'^new-pin/$', NewPin.as_view(), name='new-pin'),
)
