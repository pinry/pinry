from django.db import models
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile

from thumbs import ImageWithThumbsField

import urllib2


class Pin(models.Model):
    url = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    image = ImageWithThumbsField(upload_to='pins/pin', sizes=((200, 1000),))
    published = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.url

    def save(self, *args, **kwargs):
        if not self.image:
            temp_img = NamedTemporaryFile()
            temp_img.write(urllib2.urlopen(self.url).read())
            temp_img.flush()
            # pylint: disable-msg=E1101
            self.image.save(self.url.split('/')[-1], File(temp_img))
        super(Pin, self).save()

    class Meta:
        ordering = ['-id']
