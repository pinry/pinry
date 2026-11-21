from datetime import timedelta
from io import StringIO

from django.core.management import call_command, CommandError
from django.test import TestCase
from django.utils import timezone

from .helpers import create_image, create_pin, create_user
from core.models import Image


class PruneImagesTests(TestCase):
    def _old_image(self, hours=48):
        image = create_image()
        Image.objects.filter(pk=image.pk).update(
            created=timezone.now() - timedelta(hours=hours))
        return image

    def _prune(self, *args):
        out = StringIO()
        with self.captureOnCommitCallbacks(execute=True):
            call_command("prune_images", *args, stdout=out)
        return out.getvalue()

    def _files(self, image):
        return [image.image] + [t.image for t in image.thumbnail_set.all()]

    def test_should_delete_old_unused_image_and_files(self):
        image = self._old_image()
        files = self._files(image)
        out = self._prune("--delete")
        self.assertIn("Deleted 1 unused images.", out)
        self.assertFalse(Image.objects.filter(pk=image.pk).exists())
        for f in files:
            self.assertFalse(f.storage.exists(f.name), f.name)

    def test_should_only_list_without_delete(self):
        image = self._old_image()
        out = self._prune("--verbosity", "2")
        self.assertIn("Would delete image %d" % image.pk, out)
        self.assertIn("1 unused images would be deleted.", out)
        self.assertTrue(Image.objects.filter(pk=image.pk).exists())

    def test_should_keep_recent_unused_image(self):
        image = self._old_image(hours=1)
        self._prune("--delete")
        self.assertTrue(Image.objects.filter(pk=image.pk).exists())

    def test_should_keep_old_image_with_pin(self):
        image = self._old_image()
        create_pin(create_user("default"), image, [])
        self._prune("--delete")
        self.assertTrue(Image.objects.filter(pk=image.pk).exists())

    def test_older_than_should_change_grace_period(self):
        image = self._old_image(hours=1)
        self._prune("--delete", "--older-than", "0.5")
        self.assertFalse(Image.objects.filter(pk=image.pk).exists())

    def test_should_reject_negative_older_than(self):
        with self.assertRaises(CommandError):
            call_command("prune_images", "--older-than", "-1")

    def test_new_image_should_get_created_time(self):
        before = timezone.now()
        image = create_image()
        self.assertGreaterEqual(image.created, before)
