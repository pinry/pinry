from django.conf.urls import url

from users.views import login_user
from . import views

urlpatterns = [
    url(r'^private/$', views.private, name='private'),
    url(r'^register/$', views.CreateUser.as_view(), name='register'),
    url(r'^login/$', login_user, name='login'),
    url(r'^logout/$', views.logout_user, name='logout'),
]
