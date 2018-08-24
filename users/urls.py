from django.conf.urls import url
from django.contrib.auth.views import login

from . import views

urlpatterns = [
    url(r'^private/$', views.private, name='private'),
    url(r'^register/$', views.CreateUser.as_view(), name='register'),
    url(r'^login/$', login,
        {'template_name': 'users/login.html'}, name='login'),
    url(r'^logout/$', views.logout_user, name='logout'),
]
