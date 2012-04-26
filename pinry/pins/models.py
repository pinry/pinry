from django.db import models
from django.template.defaultfilters import slugify
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile

from thumbs import ImageWithThumbsField

import urllib2


class Pin(models.Model):
    url = models.TextField()
    title = models.CharField(max_length=70)
    image = ImageWithThumbsField(upload_to='pins/pin', sizes=((200,1000),))
    tags = models.ManyToManyField('Tag')

    def __unicode__(self):
        return self.title

    def save(self):
        if not self.image:
            temp_img = NamedTemporaryFile()
            temp_img.write(urllib2.urlopen(self.url).read())
            temp_img.flush()
            self.image.save(self.url.split('/')[-1], File(temp_img))
        if not self.title:
            self.title = self.url.split('/')[-1]
        super(Pin, self).save()


class Tag(models.Model):
    name = models.CharField(max_length=70)
    slug = models.SlugField()

    def __unicode__(self):
        return self.name

    def save(self):
        self.slug = slugify(self.name)
        super(Tag, self).save()
