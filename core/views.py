from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, mixins, routers
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.viewsets import GenericViewSet

from core import serializers as api
from core.models import Image, Pin, Board
from core.permissions import IsOwnerOrReadOnly
from users.models import User


class UserViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    serializer_class = api.UserSerializer
    pagination_class = None

    def get_queryset(self):
        if self.request.user.is_anonymous:
            return User.objects.none()
        return User.objects.filter(id=self.request.user.id)


class ImageViewSet(mixins.CreateModelMixin, GenericViewSet):
    queryset = Image.objects.all()
    serializer_class = api.ImageSerializer

    def create(self, request, *args, **kwargs):
        return super(ImageViewSet, self).create(request, *args, **kwargs)


class PinViewSet(viewsets.ModelViewSet):
    queryset = Pin.objects.all().select_related('image', 'submitter')
    serializer_class = api.PinSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filter_fields = ("submitter__username", 'tags__name', )
    ordering_fields = ('-id', )
    ordering = ('-id', )
    permission_classes = [IsOwnerOrReadOnly("submitter"), ]


class BoardViewSet(viewsets.ModelViewSet):
    queryset = Board.objects.all()
    serializer_class = api.BoardSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filter_fields = ("submitter__username", )
    ordering_fields = ('-id', )
    ordering = ('-id', )
    permission_classes = [IsOwnerOrReadOnly("submitter"), ]


drf_router = routers.DefaultRouter()
drf_router.register(r'users', UserViewSet, base_name="user")
drf_router.register(r'pins', PinViewSet)
drf_router.register(r'images', ImageViewSet)
drf_router.register(r'boards', BoardViewSet)
