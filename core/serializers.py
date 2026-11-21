from django.conf import settings
from django.db import transaction
from django.db.models import Q
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_field
from urllib.parse import urlparse
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from taggit.models import Tag

from core.fetch import FetchError
from core.models import Image, Board
from core.models import Pin
from django_images.models import Thumbnail
from django_images.utils import file_sha256
from users.serializers import PublicUserSerializer
from users.models import User


def filter_private_pin(request, query):
    if request.user.is_authenticated:
        query = query.exclude(~Q(submitter=request.user), private=True)
    else:
        query = query.exclude(private=True)
    return query.select_related('image', 'submitter')


def reusable_images(request):
    """
    Images the requester may attach to a pin: their own uploads that no pin
    uses yet (issue #6), and images used by pins they can see.
    """
    visible_pins = filter_private_pin(request, Pin.objects.all())
    if request.user.is_authenticated:
        own_unattached = Q(pin__isnull=True, uploaded_by=request.user)
    else:
        own_unattached = Q(pk__in=[])
    return Image.objects.filter(
        own_unattached | Q(pin__in=visible_pins),
    ).distinct()


def validate_http_url(value):
    # Pin links are rendered as hrefs, so only allow http(s) schemes.
    if not value:
        return value
    if urlparse(value.strip()).scheme.lower() not in ("http", "https"):
        raise ValidationError("Only http and https URLs are allowed.")
    return value


def filter_private_board(request, query):
    if request.user.is_authenticated:
        query = query.exclude(~Q(submitter=request.user), private=True)
    else:
        query = query.exclude(private=True)
    return query


class ThumbnailSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Thumbnail
        fields = (
            "image",
            "width",
            "height",
        )


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = (
            "id",
            "image",
            "width",
            "height",
            "standard",
            "thumbnail",
            "square",
        )
        extra_kwargs = {
            "width": {"read_only": True},
            "height": {"read_only": True},
        }

    standard = ThumbnailSerializer(read_only=True)
    thumbnail = ThumbnailSerializer(read_only=True)
    square = ThumbnailSerializer(read_only=True)

    def create(self, validated_data):
        # Reuse an image the uploader could already attach rather than store
        # a second copy (issue #8). Images they can't see are never reused,
        # so an upload doesn't reveal that someone else has the same file.
        sha256 = file_sha256(validated_data['image'])
        existing = Image.objects.lock_reusable(
            reusable_images(self.context['request']), sha256=sha256,
        )
        if existing is not None:
            return existing
        image = super(ImageSerializer, self).create(
            dict(validated_data, sha256=sha256),
        )
        Thumbnail.objects.get_or_create_at_sizes(image, settings.IMAGE_SIZES.keys())
        return image


class TagSerializer(serializers.SlugRelatedField):
    class Meta:
        model = Tag
        fields = ("name",)

    queryset = Tag.objects.all()

    def __init__(self, **kwargs):
        super(TagSerializer, self).__init__(
            slug_field="name",
            **kwargs
        )

    def to_internal_value(self, data):
        obj, _ = self.get_queryset().get_or_create(
            defaults={self.slug_field: data, "slug": data},
            **{self.slug_field: data}
        )
        return obj


@extend_schema_field(OpenApiTypes.INT)
class ReusableImageField(serializers.PrimaryKeyRelatedField):
    """
    Accept an image only if it is the requester's own upload that no pin uses
    yet, or is used by a pin the requester can see. Any other image is
    rejected as if it didn't exist, so a private image's existence isn't
    revealed and nobody can claim someone else's upload (issue #6).
    """

    def get_queryset(self):
        return reusable_images(self.context['request'])


class PinSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Pin
        fields = (
            settings.DRF_URL_FIELD_NAME,
            "private",
            "id",
            "submitter",
            "url",
            "description",
            "referer",
            "image",
            "image_by_id",
            "tags",
        )

    submitter = PublicUserSerializer(read_only=True)
    tags = TagSerializer(
        many=True,
        source="tag_list",
        required=False,
    )
    image = ImageSerializer(required=False, read_only=True)
    image_by_id = ReusableImageField(
        write_only=True,
        required=False,
    )

    def validate_url(self, value):
        return validate_http_url(value)

    def validate_referer(self, value):
        return validate_http_url(value)

    @transaction.atomic
    def create(self, validated_data):
        if 'url' not in validated_data and\
                'image_by_id' not in validated_data:
            raise ValidationError(
                detail={
                    "url-or-image": "Either url or image_by_id is required."
                },
            )

        request = self.context['request']
        submitter = request.user
        if 'url' in validated_data and validated_data['url']:
            url = validated_data['url']
            try:
                image = Image.objects.create_for_url(
                    url,
                    validated_data.get('referer', url),
                    uploaded_by=submitter,
                    reusable=reusable_images(request),
                )
            except FetchError as e:
                raise ValidationError({"url": str(e)}) from e
            if not image:
                raise ValidationError({"url": "invalid image content"})
        else:
            pk = validated_data.pop("image_by_id").pk
            # Lock it so it can't be deleted before the pin is saved.
            image = Image.objects.lock_reusable(reusable_images(request), pk=pk)
            if image is None:
                field = self.fields['image_by_id']
                raise ValidationError({"image_by_id": [
                    field.error_messages['does_not_exist'].format(pk_value=pk),
                ]})
        tags = validated_data.pop('tag_list', [])
        pin = Pin.objects.create(submitter=submitter, image=image, **validated_data)
        if tags:
            pin.tags.set(tags)
        return pin

    def update(self, instance, validated_data):
        tags = validated_data.pop('tag_list', None)
        if tags:
            instance.tags.set(tags)
        else:
            instance.tags.clear()
        # change for image-id or image is not allowed
        validated_data.pop('image_by_id', None)
        return super(PinSerializer, self).update(instance, validated_data)


class PinIdListField(serializers.ListField):
    child = serializers.IntegerField(
        min_value=1
    )


class BoardAutoCompleteSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Board
        fields = (
            settings.DRF_URL_FIELD_NAME,
            'id',
            'name',
        )


class BoardSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Board
        fields = (
            settings.DRF_URL_FIELD_NAME,
            "id",
            "name",
            "private",
            "total_pins",
            "cover",
            "published",
            "submitter",
            "pins_to_add",
            "pins_to_remove",
        )
        read_only_fields = ('submitter', 'published')
        extra_kwargs = {
            'submitter': {"view_name": "users:user-detail"},
        }

    submitter = PublicUserSerializer(read_only=True)
    total_pins = serializers.SerializerMethodField(
        read_only=True,
    )
    cover = serializers.SerializerMethodField(
        read_only=True,
    )
    pins_to_add = PinIdListField(
        max_length=10,
        write_only=True,
        required=False,
        allow_empty=False,
        help_text="only patch method works for this field",
    )
    pins_to_remove = PinIdListField(
        max_length=10,
        write_only=True,
        required=False,
        allow_empty=False,
        help_text="only patch method works for this field"
    )

    def get_total_pins(self, instance) -> int:
        query = instance.pins.all()
        request = self.context['request']
        query = filter_private_pin(request, query)
        return query.count()

    @extend_schema_field(PinSerializer(allow_null=True))
    def get_cover(self, instance: Board):
        pin = filter_private_pin(
            self.context['request'], instance.pins.all(),
        ).first()
        if pin is None:
            return None
        return PinSerializer(pin, context=self.context).data

    @staticmethod
    def _get_list(pins_id, submitter: User):
        pins = Pin.objects.filter(id__in=pins_id)
        valid_pins = []
        for pin in pins:
            if pin.private and pin.submitter != submitter:
                continue
            valid_pins.append(pin)
        return valid_pins

    def update(self, instance: Board, validated_data):
        pins_to_add = validated_data.pop("pins_to_add", [])
        pins_to_remove = validated_data.pop("pins_to_remove", [])
        board = Board.objects.filter(
            submitter=instance.submitter,
            name=validated_data.get('name', None)
        ).first()
        if board and board.id != instance.id:
            raise ValidationError(
                detail={'name': "Board with this name already exists"}
            )
        instance = super(BoardSerializer, self).update(instance, validated_data)
        changed = False
        if pins_to_add:
            changed = True
            for pin in self._get_list(pins_to_add, instance.submitter):
                instance.pins.add(pin)
        if pins_to_remove:
            changed = True
            for pin in self._get_list(pins_to_remove, instance.submitter):
                instance.pins.remove(pin)
        if changed:
            instance.save()
        return instance

    def create(self, validated_data):
        validated_data.pop('pins_to_remove', None)
        validated_data.pop('pins_to_add', None)
        user = self.context['request'].user
        if Board.objects.filter(name=validated_data['name'], submitter=user).exists():
            raise ValidationError(
                detail={"name": "board with this name already exists."}
            )
        validated_data['submitter'] = user
        return super(BoardSerializer, self).create(validated_data)


class TagAutoCompleteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('name', )
