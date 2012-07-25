from tastypie.resources import ModelResource
from tastypie import fields
from tastypie.authentication import BasicAuthentication
from tastypie.authorization import DjangoAuthorization

from django.contrib.auth.models import User

from pinry.pins.models import Pin


class PinResource(ModelResource):  # pylint: disable-msg=R0904
    class Meta:
        queryset = Pin.objects.all()
        resource_name = 'pin'
        include_resource_uri = False
        filtering = {
            'published': ['gt'],
        }


class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'auth/user'
        excludes = ['email', 'password', 'is_superuser']
        # Add it here.
        authentication = BasicAuthentication()
        authorization = DjangoAuthorization()
