from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^thumbnail/(?P<image_id>\d+)/(?P<size>[^/]+)/$', views.thumbnail, name='image-thumbnail'),
]
