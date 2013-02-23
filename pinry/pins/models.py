import hashlib
import os
import urllib2

from cStringIO import StringIO
from django.db import models
from django.conf import settings
from django.core.files.uploadedfile import InMemoryUploadedFile
from taggit.managers import TaggableManager

from pinry.core.models import User
from . import utils


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


class OriginalImageManager(models.Manager):
    def create_for_url(self, url):
        buf = StringIO()
        buf.write(urllib2.urlopen(url).read())
        fname = url.split('/')[-1]
        temporary_file = InMemoryUploadedFile(buf, "image", fname,
                                              content_type=None, size=buf.tell(), charset=None)
        temporary_file.name = fname
        return OriginalImage.objects.create(image=temporary_file)


class BaseImageManager(models.Manager):
    def get_or_create_for_id_class(self, original_id, cls, image_size):
        original = OriginalImage.objects.get(pk=original_id)
        buf = StringIO()
        img = utils.scale_and_crop(original.image, image_size)
        img.save(buf, img.format, **img.info)
        original_dir, original_file = os.path.split(original.image.name)
        file_obj = InMemoryUploadedFile(buf, "image", original_file, None, buf.tell(), None)
        image = cls.objects.create(original=original, image=file_obj)

        return image

    def get_or_create_for_id(self, original_id):
        raise NotImplementedError()


class StandardImageManager(BaseImageManager):
    def get_or_create_for_id(self, original_id):
        return self.get_or_create_for_id_class(original_id, StandardImage, settings.IMAGE_SIZES['standard'])


class ThumbnailManager(BaseImageManager):
    def get_or_create_for_id(self, original_id):
        return self.get_or_create_for_id_class(original_id, Thumbnail, settings.IMAGE_SIZES['thumbnail'])


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
            self.standard = StandardImage.objects.get_or_create_for_id(self.original.pk)
            self.thumbnail = Thumbnail.objects.get_or_create_for_id(self.original.pk)
        super(Pin, self).save(*args, **kwargs)

    class Meta:
        ordering = ['-id']
