from django.conf import settings
from django.core.files.images import ImageFile
from django_images.models import Thumbnail

from taggit.models import Tag

from core.models import Pin, Image
from users.models import User


TEST_IMAGE_PATH = 'docs/src/imgs/logo-dark.png'


def create_user(username):
    user, _ = User.objects.get_or_create(
        username='user_{}'.format(username),
        defaults={
            "email": 'user_{}@example.com'.format(username)
        }
    )
    user.set_password("password")
    user.save()
    return user


def create_tag(name):
    return Tag.objects.get_or_create(
        name='tag_{}'.format(name),
        slug='tag_{}'.format(name),
    )


def create_image():
    image = Image.objects.create(image=ImageFile(open(TEST_IMAGE_PATH, 'rb')))
    Thumbnail.objects.get_or_create_at_sizes(image, settings.IMAGE_SIZES.keys())
    return image


def create_pin(user, image, tags):
    pin = Pin.objects.create(submitter=user, image=image)
    pin.tags.set(*tags)
    return pin
