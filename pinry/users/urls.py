from django.conf.urls import patterns, url

from .views import CreateUser

urlpatterns = patterns('',
    url(r'^private/$', 'pinry.users.views.private', name='private'),
    url(r'^register/$', CreateUser.as_view(), name='register'),
    url(r'^login/$', 'django.contrib.auth.views.login',
        {'template_name': 'users/login.html'}, name='login'),
    url(r'^logout/$', 'pinry.users.views.logout_user', name='logout'),
)
