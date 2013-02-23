import os
import urllib2
from cStringIO import StringIO

from django.conf import settings
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models

from . import utils


class OriginalImageManager(models.Manager):
    def create_for_url(self, url):
        buf = StringIO()
        buf.write(urllib2.urlopen(url).read())
        fname = url.split('/')[-1]
        temporary_file = InMemoryUploadedFile(buf, "image", fname,
                                              content_type=None, size=buf.tell(), charset=None)
        temporary_file.name = fname
        return self.create(image=temporary_file)


class BaseImageManager(models.Manager):
    image_size = None

    def get_or_create_for(self, original):
        buf = StringIO()
        img = utils.scale_and_crop(original.image, settings.IMAGE_SIZES[self.image_size])
        img.save(buf, img.format, **img.info)
        original_dir, original_file = os.path.split(original.image.name)
        file_obj = InMemoryUploadedFile(buf, "image", original_file, None, buf.tell(), None)
        image = self.create(original=original, image=file_obj)

        return image


class StandardImageManager(BaseImageManager):
    image_size = 'standard'


class ThumbnailManager(BaseImageManager):
    image_size = 'thumbnail'
