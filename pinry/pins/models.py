from django.db import models

from django_images.models import Image
from taggit.managers import TaggableManager

from ..core.models import User


class Pin(models.Model):
    submitter = models.ForeignKey(User)
    url = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    image = models.ForeignKey(Image, related_name='pin')
    published = models.DateTimeField(auto_now_add=True)
    tags = TaggableManager()

    def __unicode__(self):
        return self.url

    class Meta:
        ordering = ['-id']
