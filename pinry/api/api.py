from django.conf import settings


from django_images.models import Thumbnail
from tastypie.resources import ModelResource
from tastypie import fields
from tastypie.authorization import DjangoAuthorization

from pinry.core.models import User

from pinry.pins.models import Pin


class UserResource(ModelResource):
    gravatar = fields.CharField()

    def dehydrate_gravatar(self, bundle):
        return bundle.obj.gravatar

    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'
        excludes = ['password', 'is_superuser', 'first_name',
            'last_name', 'is_active', 'is_staff', 'last_login', 'date_joined']
        include_resource_uri = False


class PinResource(ModelResource):
    images = fields.DictField()
    tags = fields.ListField()
    submitter = fields.ForeignKey(UserResource, 'submitter', full=True)

    def dehydrate_images(self, bundle):
        original = bundle.obj.image
        images = {'original': {
            'url': original.get_absolute_url(), 'width': original.width, 'height': original.height}
        }
        for image in ['standard', 'thumbnail']:
            obj = Thumbnail.objects.get_or_create_at_size(original.pk, image)
            images[image] = {
                'url': obj.get_absolute_url(), 'width': obj.width, 'height': obj.height
            }
        return images

    class Meta:
        queryset = Pin.objects.all()
        resource_name = 'pin'
        include_resource_uri = False
        filtering = {
            'published': ['gt'],
            'submitter': ['exact']
        }
        fields = ['submitter', 'tags', 'published', 'description', 'url']
        authorization = DjangoAuthorization()

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
