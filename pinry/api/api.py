from tastypie.resources import ModelResource
from tastypie import fields
from tastypie.authentication import BasicAuthentication
from tastypie.authorization import DjangoAuthorization

from django.contrib.auth.models import User

from pinry.pins.models import Pin


class PinResource(ModelResource):  # pylint: disable-msg=R0904
    thumbnail = fields.CharField(readonly=True)

    class Meta:
        queryset = Pin.objects.all()
        resource_name = 'pin'
        include_resource_uri = False
        filtering = {
            'published': ['gt'],
        }

    def dehydrate_thumbnail(self, bundle):
        pin = Pin.objects.only('image').get(pk=bundle.data['id'])
        return pin.image.url_200x1000


class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'auth/user'
        excludes = ['email', 'password', 'is_superuser']
        # Add it here.
        authentication = BasicAuthentication()
        authorization = DjangoAuthorization()
