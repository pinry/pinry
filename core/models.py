import hashlib
import os

import PIL.Image

from io import BytesIO
from urllib.parse import urlparse

from django.conf import settings
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models, transaction
from django.dispatch import receiver

from django_images.models import Image as BaseImage, Thumbnail
from taggit.managers import TaggableManager

from core.fetch import fetch_url

from users.models import User


class ImageManager(models.Manager):
    # Formats whose most common extension isn't the first one Pillow lists.
    _preferred_extensions = {
        "JPEG": ".jpg",
        "MPO": ".jpg",
        "TIFF": ".tif",
    }

    @staticmethod
    def _is_valid_image(fp):
        return ImageManager._detect_format(fp) is not None

    @staticmethod
    def _detect_format(fp):
        fp.seek(0)
        try:
            image_format = PIL.Image.open(fp).format
        except (PIL.UnidentifiedImageError, PIL.Image.DecompressionBombError):
            image_format = None
        fp.seek(0)
        return image_format

    @classmethod
    def _extension_for_format(cls, image_format):
        if image_format in cls._preferred_extensions:
            return cls._preferred_extensions[image_format]
        for ext, fmt in PIL.Image.registered_extensions().items():
            if fmt == image_format:
                return ext
        return None

    @staticmethod
    def _base_name(url):
        file_name = urlparse(url).path.rsplit("/", 1)[-1]
        base = os.path.splitext(file_name)[0][:64]
        return base or "image"

    def lock_reusable(self, reusable, **lookup):
        """Return the first image in ``reusable`` matching ``lookup``, or None.

        The image row is locked, so when this runs in the transaction that
        saves a pin for it, its last other pin can't be deleted (taking the
        image with it) before the new pin is saved (issue #7).
        """
        pk = reusable.filter(**lookup).order_by('pk') \
            .values_list('pk', flat=True).first()
        if pk is None:
            return None
        with transaction.atomic():
            image = self.select_for_update().filter(pk=pk).first()
        # Check again now that it's locked: it may have been deleted, or
        # lost the pin that made it reusable, while we waited.
        if image is None or not reusable.filter(pk=pk).exists():
            return None
        return image

    # FIXME: Move this into an asynchronous task
    def create_for_url(self, url, referer=None, uploaded_by=None,
                       reusable=None):
        """Fetch ``url`` and store it as an Image.

        If an image in the ``reusable`` queryset already has the same
        content, return that instead of storing a copy (issue #8).

        Returns None if the content isn't an image Pillow can read; raises
        core.fetch.FetchError if the URL can't or mustn't be fetched.
        """
        buf = BytesIO(fetch_url(url, referer=referer))
        ext = self._extension_for_format(self._detect_format(buf))
        if ext is None:
            return None
        sha256 = hashlib.sha256(buf.getvalue()).hexdigest()
        if reusable is not None:
            existing = self.lock_reusable(reusable, sha256=sha256)
            if existing is not None:
                return existing
        # Name the file after the detected format, never the URL, so a
        # polyglot fetched from ".../x.html" isn't served as HTML.
        file_name = self._base_name(url) + ext
        size = len(buf.getvalue())
        obj = InMemoryUploadedFile(buf, 'image', file_name,
                                   None, size, None)
        # create the image and its thumbnails in one transaction, removing
        # a chance of getting Database into a inconsistent state when we
        # try to create thumbnails one by one later
        image = self.create(image=obj, uploaded_by=uploaded_by, sha256=sha256)
        Thumbnail.objects.get_or_create_at_sizes(image, settings.IMAGE_SIZES.keys())
        return image


class Image(BaseImage):
    objects = ImageManager()

    class Sizes:
        standard = "standard"
        thumbnail = "thumbnail"
        square = "square"

    class Meta:
        proxy = True

    @property
    def standard(self):
        return Thumbnail.objects.get(
            original=self, size=self.Sizes.standard
        )

    @property
    def thumbnail(self):
        return Thumbnail.objects.get(
            original=self, size=self.Sizes.thumbnail
        )

    @property
    def square(self):
        return Thumbnail.objects.get(
            original=self, size=self.Sizes.square
        )


class Board(models.Model):
    class Meta:
        unique_together = ("submitter", "name")

    submitter = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=128, blank=False, null=False)
    private = models.BooleanField(default=False, blank=False)
    pins = models.ManyToManyField("Pin", related_name="pins", blank=True)

    published = models.DateTimeField(auto_now_add=True)


class Pin(models.Model):
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["submitter", "source_id"],
                condition=models.Q(source_id__isnull=False),
                name="core_pin_unique_source_id",
            ),
        ]

    submitter = models.ForeignKey(User, on_delete=models.CASCADE)
    private = models.BooleanField(default=False, blank=False)
    url = models.CharField(null=True, blank=True, max_length=2048)
    referer = models.CharField(null=True, blank=True, max_length=2048)
    description = models.TextField(blank=True, null=True)
    image = models.ForeignKey(Image, related_name='pin', on_delete=models.CASCADE)
    published = models.DateTimeField(auto_now_add=True)
    # Where an imported pin came from, such as "pinterest:<pin id>", so a
    # second import of the same data skips it.
    source_id = models.CharField(null=True, blank=True, max_length=64)
    tags = TaggableManager()

    def tag_list(self):
        return self.tags.all()

    def __str__(self):
        return '%s - %s' % (self.submitter, self.published)


@receiver(models.signals.post_delete, sender=Pin)
def delete_pin_images(sender, instance, using, **kwargs):
    # Pins can share an image, so only delete it along with its last pin.
    # Lock the image row before counting its pins: otherwise two requests
    # deleting its last two pins at once each still see the other pin and
    # neither deletes it (issue #7). SQLite ignores the lock, but it runs
    # one write transaction at a time anyway.
    with transaction.atomic(using=using, savepoint=False):
        image = (Image.objects.using(using).select_for_update()
                 .filter(pk=instance.image_id).first())
        if image is None or \
                Pin.objects.using(using).filter(image_id=image.pk).exists():
            return
        image.delete()
