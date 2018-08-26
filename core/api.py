from django.core.exceptions import ObjectDoesNotExist
from tastypie import fields
from tastypie.authorization import DjangoAuthorization
from tastypie.constants import ALL, ALL_WITH_RELATIONS
from tastypie.exceptions import Unauthorized
from tastypie.resources import ModelResource
from django_images.models import Thumbnail

from .models import Pin, Image
from users.models import User


def _is_pin_owner(obj_or_list, user):
    assert obj_or_list is not None
    if not isinstance(obj_or_list, (tuple, list)):
        obj_or_list = (obj_or_list,)
    results = tuple(
        obj.submitter == user
        for obj in obj_or_list
        if isinstance(obj, Pin)
    )
    if len(results) <= 0:
        raise ValueError(
            "You should never check permission on %s with this function."
            % obj_or_list
        )
    return all(results)


def _is_authenticated_and_owner(object_list, bundle):
    if bundle.request.user.is_anonymous():
        return object_list.none()
    return object_list.filter(submitter=bundle.request.user)


class PinryAuthorization(DjangoAuthorization):
    """
    Pinry-specific Authorization backend with object-level permission checking.
    """
    def _is_obj_owner(self, object_list, bundle):
        klass = self.base_checks(bundle.request, bundle.obj.__class__)

        if klass is False:
            raise Unauthorized("You are not allowed to access that resource.")
        return _is_pin_owner(bundle.obj, bundle.request.user)

    def read_list(self, object_list, bundle):
        # This assumes a ``QuerySet`` from ``ModelResource``.
        return object_list

    def read_detail(self, object_list, bundle):
        """
        User can always read detail of any Pin object.
        """
        return True

    def create_detail(self, object_list, bundle):
        return self._is_obj_owner(object_list, bundle)

    def update_detail(self, object_list, bundle):
        return self._is_obj_owner(object_list, bundle)

    def delete_detail(self, object_list, bundle):
        return self._is_obj_owner(object_list, bundle)

    def update_list(self, object_list, bundle):
        return _is_authenticated_and_owner(object_list, bundle)

    def delete_list(self, object_list, bundle):
        return _is_authenticated_and_owner(object_list, bundle)


class ImageAuthorization(DjangoAuthorization):
    """
    Pinry-specific Authorization backend with object-level permission checking.
    """
    def __init__(self):
        DjangoAuthorization.__init__(self)

    def read_list(self, object_list, bundle):
        return object_list

    def read_detail(self, object_list, bundle):
        """
        User can always read detail of any Pin object.
        """
        return True

    def create_detail(self, object_list, bundle):
        return bundle.request.user.is_authenticated()

    def update_detail(self, object_list, bundle):
        return bundle.request.user.is_authenticated()

    def delete_detail(self, object_list, bundle):
        return bundle.request.user.is_authenticated()

    def update_list(self, object_list, bundle):
        if not bundle.request.user.is_authenticated():
            return object_list.none()
        return object_list

    def delete_list(self, object_list, bundle):
        if not bundle.request.user.is_authenticated():
            return object_list.none()
        return object_list


class UserResource(ModelResource):
    gravatar = fields.CharField(readonly=True)

    def dehydrate_gravatar(self, bundle):
        return bundle.obj.gravatar

    class Meta:
        list_allowed_methods = ['get']
        filtering = {
            'username': ALL
        }
        queryset = User.objects.all()
        resource_name = 'user'
        fields = ['username']
        include_resource_uri = False


def filter_generator_for(size):
    def wrapped_func(bundle, **kwargs):
        if hasattr(bundle.obj, '_prefetched_objects_cache') and 'thumbnail' in bundle.obj._prefetched_objects_cache:
            for thumbnail in bundle.obj._prefetched_objects_cache['thumbnail']:
                if thumbnail.size == size:
                    return thumbnail
            raise ObjectDoesNotExist()
        else:
            return bundle.obj.get_by_size(size)
    return wrapped_func


class ThumbnailResource(ModelResource):
    class Meta:
        list_allowed_methods = ['get']
        fields = ['image', 'width', 'height']
        queryset = Thumbnail.objects.all()
        resource_name = 'thumbnail'
        include_resource_uri = False


class ImageResource(ModelResource):
    standard = fields.ToOneField(
        ThumbnailResource, full=True,
        attribute=lambda bundle: filter_generator_for('standard')(bundle),
        related_name='thumbnail',
    )
    thumbnail = fields.ToOneField(
        ThumbnailResource, full=True,
        attribute=lambda bundle: filter_generator_for('thumbnail')(bundle),
        related_name='thumbnail',
    )
    square = fields.ToOneField(
        ThumbnailResource, full=True,
        attribute=lambda bundle: filter_generator_for('square')(bundle),
        related_name='thumbnail',
    )

    class Meta:
        fields = ['image', 'width', 'height']
        include_resource_uri = False
        resource_name = 'image'
        queryset = Image.objects.all()
        authorization = ImageAuthorization()


class PinResource(ModelResource):
    submitter = fields.ToOneField(UserResource, 'submitter', full=True)
    image = fields.ToOneField(ImageResource, 'image', full=True)
    tags = fields.ListField()

    def hydrate_image(self, bundle):
        url = bundle.data.get('url', None)
        if url:
            image = Image.objects.create_for_url(
                url,
                referer=bundle.data.get('referer', None),
            )
            bundle.data['image'] = '/api/v1/image/{}/'.format(image.pk)
        return bundle

    def hydrate(self, bundle):
        """Run some early/generic processing

        Make sure that user is authorized to create Pins first, before
        we hydrate the Image resource, creating the Image object in process
        """
        submitter = bundle.data.get('submitter', None)
        if not submitter:
            bundle.data['submitter'] = '/api/v1/user/{}/'.format(bundle.request.user.pk)
        else:
            if not '/api/v1/user/{}/'.format(bundle.request.user.pk) == submitter:
                raise Unauthorized("You are not authorized to create Pins for other users")
        return bundle

    def dehydrate_tags(self, bundle):
        return list(map(str, bundle.obj.tags.all()))

    def build_filters(self, filters=None, ignore_bad_filters=False):
        orm_filters = super(PinResource, self).build_filters(filters, ignore_bad_filters=ignore_bad_filters)
        if filters and 'tag' in filters:
            orm_filters['tags__name__in'] = filters['tag'].split(',')
        return orm_filters

    def save_m2m(self, bundle):
        tags = bundle.data.get('tags', None)
        if tags:
            bundle.obj.tags.set(*tags)
        return super(PinResource, self).save_m2m(bundle)

    class Meta:
        fields = ['id', 'url', 'origin', 'description', 'referer']
        ordering = ['id']
        filtering = {
            'submitter': ALL_WITH_RELATIONS
        }
        queryset = Pin.objects.all().select_related('submitter', 'image'). \
            prefetch_related('image__thumbnail_set', 'tags')
        resource_name = 'pin'
        include_resource_uri = False
        always_return_data = True
        authorization = PinryAuthorization()
