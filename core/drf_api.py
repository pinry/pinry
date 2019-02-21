from django.conf import settings
from rest_framework import serializers
from taggit.models import Tag

from core.models import Image
from core.models import Pin
from django_images.models import Thumbnail
from users.models import User


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            'gravatar',
            settings.DRF_URL_FIELD_NAME,
        )


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
            "image": {"read_only": True},
        }

    standard = ThumbnailSerializer(read_only=True)
    thumbnail = ThumbnailSerializer(read_only=True)
    square = ThumbnailSerializer(read_only=True)

    def create(self, validated_data):
        image = super(ImageSerializer, self).create(validated_data)
        for size in settings.IMAGE_SIZES:
            Thumbnail.objects.get_or_create_at_size(image.pk, size)
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
            **{self.slug_field: data},
            defaults={self.slug_field: data, "slug": data}
        )
        return obj


class PinSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Pin
        fields = (
            settings.DRF_URL_FIELD_NAME,
            "id",
            "submitter",
            "url",
            "origin",
            "description",
            "referer",
            "image",
            "image_by_id",
            "tags",
        )
        extra_kwargs = {
            "submitter": {"read_only": True},
        }

    tags = TagSerializer(
        many=True,
        source="tag_list",
    )
    image = ImageSerializer(required=False, read_only=True)
    image_by_id = serializers.PrimaryKeyRelatedField(
        queryset=Image.objects.all(),
        write_only=True,
    )

    def create(self, validated_data):
        submitter = self.context['request'].user
        image = validated_data.pop("image_by_id")
        if 'url' in validated_data and validated_data['url']:
            image = Image.objects.create_for_url(
                validated_data['url'],
                validated_data['referer'],
            )
        tags = validated_data.pop('tag_list')
        pin = Pin.objects.create(submitter=submitter, image=image, **validated_data)
        if tags:
            pin.tags.set(*tags)
        return pin

    def update(self, instance, validated_data):
        tags = validated_data.pop('tag_list')
        if tags:
            instance.tags.set(*tags)
        validated_data.pop('image_id')
        return super(PinSerializer, self).update(instance, validated_data)
