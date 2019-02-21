from rest_framework import viewsets, mixins, routers
from rest_framework.viewsets import GenericViewSet

from core import drf_api as api
from core.models import Image, Pin
from core.permissions import IsOwnerOrReadOnly
from users.models import User


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = api.UserSerializer


class ImageViewSet(mixins.CreateModelMixin, GenericViewSet):
    queryset = Image.objects.all()
    serializer_class = api.ImageSerializer

    def create(self, request, *args, **kwargs):
        return super(ImageViewSet, self).create(request, *args, **kwargs)


class PinViewSet(viewsets.ModelViewSet):
    queryset = Pin.objects.all()
    serializer_class = api.PinSerializer
    filter_fields = ('submitter__username',)
    permission_classes = [IsOwnerOrReadOnly("submitter"), ]


drf_router = routers.DefaultRouter()
drf_router.register(r'users', UserViewSet)
drf_router.register(r'pins', PinViewSet)
drf_router.register(r'images', ImageViewSet)
