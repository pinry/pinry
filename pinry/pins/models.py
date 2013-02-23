import hashlib

from django.db import models

from taggit.managers import TaggableManager

from ..core.models import User
from .managers import OriginalImageManager
from .managers import StandardImageManager
from .managers import ThumbnailManager


def hashed_upload_to(prefix, instance, filename):
    md5 = hashlib.md5()
    for chunk in instance.image.chunks():
        md5.update(chunk)
    file_hash = md5.hexdigest()
    arguments = {
        'prefix': prefix,
        'first': file_hash[0],
        'second': file_hash[1],
        'hash': file_hash,
        'filename': filename
    }
    return "{prefix}/{first}/{second}/{hash}/{filename}".format(**arguments)


def original_upload_to(instance, filename):
    return hashed_upload_to('image/original/by-md5', instance, filename)


def thumbnail_upload_to(instance, filename):
    return hashed_upload_to('image/thumbnail/by-md5', instance, filename)


def standard_upload_to(instance, filename):
    return hashed_upload_to('image/standard/by-md5', instance, filename)


class Image(models.Model):
    height = models.PositiveIntegerField(default=0, editable=False)
    width = models.PositiveIntegerField(default=0, editable=False)

    class Meta:
        abstract = True


class OriginalImage(Image):
    image = models.ImageField(upload_to=original_upload_to,
                              height_field='height', width_field='width', max_length=255)
    objects = OriginalImageManager()


class StandardImage(Image):
    original = models.ForeignKey(OriginalImage, related_name='standard')
    image = models.ImageField(upload_to=standard_upload_to,
                              height_field='height', width_field='width', max_length=255)
    objects = StandardImageManager()


class Thumbnail(Image):
    original = models.ForeignKey(OriginalImage, related_name='thumbnail')
    image = models.ImageField(upload_to=thumbnail_upload_to,
                              height_field='height', width_field='width', max_length=255)
    objects = ThumbnailManager()


class Pin(models.Model):
    submitter = models.ForeignKey(User)
    url = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    original = models.ForeignKey(OriginalImage, related_name='pin')
    standard = models.ForeignKey(StandardImage, related_name='pin')
    thumbnail = models.ForeignKey(Thumbnail, related_name='pin')
    published = models.DateTimeField(auto_now_add=True)
    tags = TaggableManager()

    def __unicode__(self):
        return self.url

    def save(self, *args, **kwargs):
        if not self.pk:
            self.original = OriginalImage.objects.create_for_url(self.url)
            self.standard = StandardImage.objects.get_or_create_for(self.original)
            self.thumbnail = Thumbnail.objects.get_or_create_for(self.original)
        super(Pin, self).save(*args, **kwargs)

    class Meta:
        ordering = ['-id']
