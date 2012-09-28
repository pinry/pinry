from tastypie.resources import ModelResource
from tastypie import fields
from tastypie.authentication import BasicAuthentication
from tastypie.authorization import DjangoAuthorization

from django.contrib.auth.models import User

from pinry.pins.models import Pin


class PinResource(ModelResource):  # pylint: disable-msg=R0904
    tags = fields.ListField()

    class Meta:
        queryset = Pin.objects.all()
        resource_name = 'pin'
        include_resource_uri = False
        filtering = {
            'published': ['gt'],
        }

    def build_filters(self, filters=None):
        if filters is None:
            filters = {}

        orm_filters = super(PinResource, self).build_filters(filters)

        if 'tag' in filters:
            orm_filters['tags__name__in'] = filters['tag'].split(',')

        return orm_filters

    def dehydrate_tags(self, bundle):
        return map(str, bundle.obj.tags.all())

    def save_m2m(self, bundle):
        tags = bundle.data.get('tags', [])
        bundle.obj.tags.set(*tags)
        return super(PinResource, self).save_m2m(bundle)


class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'auth/user'
        excludes = ['email', 'password', 'is_superuser']
        # Add it here.
        authentication = BasicAuthentication()
        authorization = DjangoAuthorization()
