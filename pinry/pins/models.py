from cStringIO import StringIO
import urllib2
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models

from django_images.models import Image as BaseImage
from taggit.managers import TaggableManager

from ..core.models import User


class ImageManager(models.Manager):
    # FIXME: Move this into an asynchronous task
    def create_for_url(self, url):
        file_name = url.split("/")[-1]
        buf = StringIO()
        buf.write(urllib2.urlopen(url).read())
        obj = InMemoryUploadedFile(buf, 'image', file_name, None, buf.tell(), None)
        return Image.objects.create(image=obj)


class Image(BaseImage):
    objects = ImageManager()

    class Meta:
        proxy = True


class Pin(models.Model):
    submitter = models.ForeignKey(User)
    url = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    image = models.ForeignKey(Image, related_name='pin')
    published = models.DateTimeField(auto_now_add=True)
    tags = TaggableManager()

    def __unicode__(self):
        return self.url
