import hashlib
import os.path
from io import BytesIO

from django.db import models
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.urlresolvers import reverse
from django.dispatch import receiver
import PIL

try:
    from importlib import import_module
except ImportError:
    from django.utils.importlib import import_module

from . import utils
from .settings import IMAGE_SIZES, IMAGE_PATH, IMAGE_AUTO_DELETE


def hashed_upload_to(instance, filename, **kwargs):
    image_type = 'original' if isinstance(instance, Image) else 'thumbnail'
    prefix = 'image/%s/by-md5/' % (image_type,)
    hasher = hashlib.md5()
    for chunk in instance.image.chunks():
        hasher.update(chunk)
    hash_ = hasher.hexdigest()
    base, ext = os.path.splitext(filename)
    return '%(prefix)s%(first)s/%(second)s/%(hash)s/%(base)s%(ext)s' % {
        'prefix': prefix,
        'first': hash_[0],
        'second': hash_[1],
        'hash': hash_,
        'base': base,
        'ext': ext,
    }


if IMAGE_PATH is None:
    upload_to = hashed_upload_to
else:
    if callable(IMAGE_PATH):
        upload_to = IMAGE_PATH
    else:
        parts = IMAGE_PATH.split('.')
        module_name = '.'.join(parts[:-1])
        module = import_module(module_name)
        upload_to = getattr(module, parts[-1])


class Image(models.Model):
    image = models.ImageField(upload_to=upload_to,
                              height_field='height', width_field='width',
                              max_length=255)
    height = models.PositiveIntegerField(default=0, editable=False)
    width = models.PositiveIntegerField(default=0, editable=False)

    def get_by_size(self, size):
        return self.thumbnail_set.get(size=size)

    def get_absolute_url(self, size=None):
        if not size:
            return self.image.url
        try:
            return self.get_by_size(size).image.url
        except Thumbnail.DoesNotExist:
            return reverse('image-thumbnail', args=(self.id, size))


class ThumbnailManager(models.Manager):
    def get_or_create_at_size(self, image_id, size):
        image = Image.objects.get(id=image_id)
        if size not in IMAGE_SIZES:
            raise ValueError("Received unknown size: %s" % size)
        try:
            thumbnail = image.get_by_size(size)
        except Thumbnail.DoesNotExist:
            img = utils.scale_and_crop(image.image, **IMAGE_SIZES[size])
            # save to memory
            buf = BytesIO()
            try:
                img.save(buf, img.format, **img.info)
            except IOError:
                if img.info.get('progression'):
                    orig_MAXBLOCK = PIL.ImageFile.MAXBLOCK
                    temp_MAXBLOCK = 1048576
                    if orig_MAXBLOCK >= temp_MAXBLOCK:
                        raise
                    PIL.ImageFile.MAXBLOCK = temp_MAXBLOCK
                    try:
                        img.save(buf, img.format, **img.info)
                    finally:
                        PIL.ImageFile.MAXBLOCK = orig_MAXBLOCK
                else:
                    raise
            # and save to storage
            original_dir, original_file = os.path.split(image.image.name)
            thumb_file = InMemoryUploadedFile(buf, "image", original_file,
                                              None, buf.tell(), None)
            thumbnail, created = image.thumbnail_set.get_or_create(
                size=size, defaults={'image': thumb_file})
        return thumbnail


class Thumbnail(models.Model):
    original = models.ForeignKey(Image)
    image = models.ImageField(upload_to=upload_to,
                              height_field='height', width_field='width',
                              max_length=255)
    size = models.CharField(max_length=100)
    height = models.PositiveIntegerField(default=0, editable=False)
    width = models.PositiveIntegerField(default=0, editable=False)

    objects = ThumbnailManager()

    class Meta:
        unique_together = ('original', 'size')

    def get_absolute_url(self):
        return self.image.url


@receiver(models.signals.post_save)
def original_changed(sender, instance, created, **kwargs):
    if isinstance(instance, Image):
        instance.thumbnail_set.all().delete()


@receiver(models.signals.post_delete)
def delete_image_files(sender, instance, **kwargs):
    if isinstance(instance, (Image, Thumbnail)) and IMAGE_AUTO_DELETE:
        if instance.image.storage.exists(instance.image.name):
            instance.image.delete(save=False)
