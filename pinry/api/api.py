from tastypie.resources import ModelResource
from tastypie import fields

from pinry.pins.models import Pin


class PinResource(ModelResource):
    thumbnail = fields.CharField(readonly=True)

    class Meta:
        queryset = Pin.objects.all()
        resource_name = 'pin'
        include_resource_uri = False

    def dehydrate_thumbnail(self, bundle):
        return Pin.objects.only('image').get(pk=bundle.data['id']).image.url_200x1000
