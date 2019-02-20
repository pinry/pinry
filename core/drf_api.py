from rest_framework import serializers, viewsets, routers, mixins
from rest_framework.viewsets import GenericViewSet
from taggit.models import Tag

from core.models import Image, Pin
from core.permissions import IsOwnerOrReadOnly
from django_images.models import Thumbnail
from django.conf import settings
from users.models import User


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            'gravatar',
            settings.DRF_URL_FIELD_NAME,
        )


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


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
        image = super(ImageSerializer, self).create(validated_data)
        for size in settings.IMAGE_SIZES:
            Thumbnail.objects.get_or_create_at_size(image.pk, size)
        return image


class ImageViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin, GenericViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ("name",)


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
            "tags",
        )


    tags = serializers.SlugRelatedField(
        many=True,
        source="tag_list",
        queryset=Tag.objects.all(),
        slug_field="name",
    )
    image = ImageSerializer(required=False)

    def create(self, validated_data):
        image_file = validated_data.pop('image')
        if validated_data['url']:
            image = Image.objects.create_for_url(
                validated_data['url'],
                validated_data['referer'],
            )
        else:
            image = Image.objects.create(image=image_file['image'])
        pin = Pin.objects.create(image=image, **validated_data)
        tags = validated_data.pop('tag_list')
        if tags:
            pin.tags.set(*tags)
        return pin

    def update(self, instance, validated_data):
        tags = validated_data.pop('tag_list')
        if tags:
            instance.tags.set(*tags)
        image_file = validated_data.pop('image', None)
        if image_file:
            image = Image.objects.create(image=image_file['image'])
            instance.image = image
        return super(PinSerializer, self).update(instance, validated_data)


class PinViewSet(viewsets.ModelViewSet):
    queryset = Pin.objects.all()
    serializer_class = PinSerializer
    filter_fields = ('submitter__username',)
    permission_classes = [IsOwnerOrReadOnly("submitter"), ]


drf_router = routers.DefaultRouter()
drf_router.register(r'users', UserViewSet)
drf_router.register(r'pins', PinViewSet)
drf_router.register(r'images', ImageViewSet)
