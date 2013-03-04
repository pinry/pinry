from django.conf import settings
from django.contrib.auth.models import Permission
from django.core.files import File

import factory
from taggit.models import Tag

from ..models import Image, Pin
from ...users.models import User


TEST_IMAGE_PATH = settings.SITE_ROOT + 'screenshot.png'


class UserFactory(factory.Factory):
    FACTORY_FOR = User

    username = factory.Sequence(lambda n: 'user_{}'.format(n))
    email = factory.Sequence(lambda n: 'user_{}@example.com'.format(n))

    @classmethod
    def _prepare(cls, create, **kwargs):
        password = kwargs.pop('password', None)
        user = super(UserFactory, cls)._prepare(create, **kwargs)
        user.user_permissions = Permission.objects.filter(codename__in=['add_pin', 'add_image'])
        if password:
            user.set_password(password)
            if create:
                user.save()
        return user


class TagFactory(factory.Factory):
    FACTORY_FOR = Tag

    name = factory.Sequence(lambda n: 'tag_{}'.format(n))


class ImageFactory(factory.Factory):
    FACTORY_FOR = Image

    image = factory.LazyAttribute(lambda a: File(open(TEST_IMAGE_PATH)))


class PinFactory(factory.Factory):
    FACTORY_FOR = Pin

    submitter = factory.SubFactory(UserFactory)
    image = factory.SubFactory(ImageFactory)

    @classmethod
    def _prepare(cls, create, **kwargs):
        pin = super(PinFactory, cls)._prepare(create, **kwargs)
        pin.tags.add(TagFactory())
        return pin