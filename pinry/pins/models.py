from django.db import models
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.contrib.auth.models import User

import urllib2
import hashlib
from PIL import Image


class Pin(models.Model):
    submitter = models.ForeignKey(User)
    url = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='pins/pin/originals/')
    thumbnail = models.ImageField(upload_to='pins/pin/thumbnails/')
    published = models.DateTimeField(auto_now_add=True)


    def __unicode__(self):
        return self.url


    def save(self, *args, **kwargs):
        if not self.image:
            temp_img = NamedTemporaryFile()
            temp_img.write(urllib2.urlopen(self.url).read())
            temp_img.flush()
            self.image.save(self.url.split('/')[-1], File(temp_img))
        else:
            super(Pin, self).save()

        if not self.thumbnail:
            if not self.image:
                image = Image.open(temp_img.name)
            else:
                image = Image.open(self.image.path)
            size = image.size
            prop = 200 / image.size[0]
            size = (prop*image.size[0], prop*image.size[1])
            image.resize(size, Image.ANTIALIAS)
            temp_thumb = NamedTemporaryFile()
            image.save(temp_thumb.name, 'JPEG')

            if self.url:
                name = self.url.split('/')[-1]
            else:
                name = self.image.name

            self.thumbnail.save(name, File(temp_thumb))

        super(Pin, self).save(*args, **kwargs)


    class Meta:
        ordering = ['-id']
