import hashlib
import os.path

from django.conf import settings
from django.db import models, transaction
from django.utils import timezone
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.dispatch import receiver

from importlib import import_module

from django.urls import reverse

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
    # Who uploaded the file, so an image no pin uses yet can only be
    # claimed by its uploader (issue #6). Set by core on upload and fetch.
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True, editable=False,
        on_delete=models.SET_NULL, related_name='+',
    )
    # SHA-256 of the file as received, for finding duplicate uploads
    # (issue #8). Set once, when the image is first saved.
    sha256 = models.CharField(
        max_length=64, blank=True, default='', editable=False, db_index=True,
    )
    # When the image was stored, so prune_images can leave alone uploads
    # that may still be attached to a new pin (issue #7).
    created = models.DateTimeField(
        default=timezone.now, editable=False, db_index=True,
    )

    def save(self, *args, **kwargs):
        if not self.sha256 and self.image:
            self.sha256 = utils.file_sha256(self.image)
        super().save(*args, **kwargs)

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
    def get_or_create_at_sizes(self, image, sizes):
        sizes_to_create = list(sizes)
        sized = {}
        for size in sizes:
            if size not in IMAGE_SIZES:
                raise ValueError("Received unknown size: %s" % size)

            try:
                sized[size] = image.get_by_size(size)
            except Thumbnail.DoesNotExist:
                pass
            else:
                sizes_to_create.remove(size)

        if sizes_to_create:
            bufs = [
                utils.write_image_in_memory(img)
                for img in utils.scale_and_crop_iter(
                    image.image,
                    [IMAGE_SIZES[size] for size in sizes_to_create])
            ]
            for size, buf in zip(sizes_to_create, bufs, strict=True):
                # and save to storage
                original_dir, original_file = os.path.split(image.image.name)
                thumb_file = InMemoryUploadedFile(buf, "image", original_file,
                                                  None, buf.tell(), None)
                sized[size], created = image.thumbnail_set.get_or_create(
                    size=size, defaults={'image': thumb_file})

        # Make sure this is in the correct order
        return [sized[size] for size in sizes]


class Thumbnail(models.Model):
    original = models.ForeignKey(Image, on_delete=models.CASCADE)
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
def delete_image_files(sender, instance, using, **kwargs):
    if isinstance(instance, (Image, Thumbnail)) and IMAGE_AUTO_DELETE:
        storage, name = instance.image.storage, instance.image.name
        if not name:
            return

        # Only once the delete is committed, so a delete that rolls back
        # doesn't leave a row whose file is gone.
        def delete_file():
            if storage.exists(name):
                storage.delete(name)
        transaction.on_commit(delete_file, using=using)
