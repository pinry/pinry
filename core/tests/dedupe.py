import hashlib
from io import StringIO
from unittest import mock

from django.core.management import call_command
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .api import _teardown_models, mock_fetch_url
from .helpers import TEST_IMAGE_PATH, create_image, create_pin, create_user
from core.models import Image, Pin


class ImageDedupeTests(APITestCase):

    def setUp(self):
        self.owner = create_user("owner")
        self.other = create_user("other")
        self.client.force_login(self.owner)

    def tearDown(self):
        _teardown_models()

    def _upload(self):
        with open(TEST_IMAGE_PATH, 'rb') as f:
            response = self.client.post(
                reverse("image-list"), {'image': f}, format="multipart",
            )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        return response.json()['id']

    def _pin_url(self):
        response = self.client.post(
            reverse("pin-list"),
            {'url': 'http://testserver.com/mocked/logo.png'},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.json())
        return Pin.objects.get(pk=response.json()['id'])

    def _pin_image(self, image_pk):
        return self.client.post(
            reverse("pin-list"), {'image_by_id': image_pk}, format="json",
        )

    def test_should_record_hash_on_upload(self):
        image = Image.objects.get(pk=self._upload())
        with open(TEST_IMAGE_PATH, 'rb') as f:
            self.assertEqual(image.sha256, hashlib.sha256(f.read()).hexdigest())

    def test_should_reuse_own_unattached_upload(self):
        self.assertEqual(self._upload(), self._upload())
        self.assertEqual(Image.objects.count(), 1)

    def test_should_not_reuse_others_unattached_upload(self):
        first = self._upload()
        self.client.force_login(self.other)
        second = self._upload()
        self.assertNotEqual(first, second)
        self.assertEqual(Image.objects.get(pk=second).uploaded_by, self.other)
        response = self._pin_image(second)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.json())

    def test_should_reuse_image_of_visible_pin(self):
        image = create_image(uploaded_by=self.other)
        create_pin(self.other, image, [])
        self.assertEqual(self._upload(), image.pk)
        response = self._pin_image(image.pk)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.json())
        self.assertEqual(Image.objects.count(), 1)

    def test_should_not_reuse_image_of_others_private_pin(self):
        image = create_image(uploaded_by=self.other)
        pin = create_pin(self.other, image, [])
        pin.private = True
        pin.save()
        self.assertNotEqual(self._upload(), image.pk)
        self.assertEqual(Image.objects.count(), 2)

    def test_should_reuse_image_of_own_private_pin(self):
        image = create_image(uploaded_by=self.owner)
        pin = create_pin(self.owner, image, [])
        pin.private = True
        pin.save()
        self.assertEqual(self._upload(), image.pk)

    @mock.patch('core.models.fetch_url', mock_fetch_url)
    def test_should_reuse_image_for_same_url_content(self):
        first = self._pin_url()
        second = self._pin_url()
        self.assertEqual(first.image_id, second.image_id)
        self.assertEqual(Image.objects.count(), 1)
        self.client.delete(reverse("pin-detail", kwargs={"pk": first.pk}))
        image = Image.objects.get(pk=second.image_id)
        self.assertTrue(image.image.storage.exists(image.image.name))

    @mock.patch('core.models.fetch_url', mock_fetch_url)
    def test_url_pin_should_not_reuse_image_of_others_private_pin(self):
        image = create_image(uploaded_by=self.other)
        pin = create_pin(self.other, image, [])
        pin.private = True
        pin.save()
        self.assertNotEqual(self._pin_url().image_id, image.pk)

    @mock.patch('core.models.fetch_url', mock_fetch_url)
    def test_url_pin_should_reuse_image_of_others_public_pin(self):
        image = create_image(uploaded_by=self.other)
        create_pin(self.other, image, [])
        self.assertEqual(self._pin_url().image_id, image.pk)

    def test_should_reject_image_deleted_before_pin_is_saved(self):
        image_pk = self._upload()
        with mock.patch.object(
            Image.objects, 'lock_reusable', return_value=None,
        ):
            response = self._pin_image(image_pk)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('image_by_id', response.json())
        self.assertEqual(Pin.objects.count(), 0)


class ImagesHashCommandTests(APITestCase):

    def setUp(self):
        self.owner = create_user("owner")
        self.other = create_user("other")

    def tearDown(self):
        _teardown_models()

    def _run(self, *args):
        out = StringIO()
        call_command('images_hash', *args, stdout=out, stderr=StringIO())
        return out.getvalue()

    def test_should_fill_in_missing_hashes(self):
        image = create_image()
        expected = image.sha256
        thumbnails = image.thumbnail_set.count()
        Image.objects.filter(pk=image.pk).update(sha256='')
        self._run()
        image.refresh_from_db()
        self.assertEqual(image.sha256, expected)
        self.assertEqual(image.thumbnail_set.count(), thumbnails)

    def test_should_skip_unreadable_files(self):
        image = create_image()
        image.image.storage.delete(image.image.name)
        Image.objects.filter(pk=image.pk).update(sha256='')
        self.assertIn("Hashed 0 image(s), 1 unreadable", self._run())

    def test_should_only_report_without_merge(self):
        create_pin(self.owner, create_image(), [])
        create_pin(self.owner, create_image(), [])
        self.assertIn("1 duplicate image(s) can be merged", self._run())
        self.assertEqual(Image.objects.count(), 2)

    def test_should_merge_duplicates_of_same_user(self):
        keep = create_image()
        duplicate = create_image()
        pin_a = create_pin(self.owner, keep, [])
        pin_b = create_pin(self.owner, duplicate, [])
        files = [duplicate.image] + [t.image for t in duplicate.thumbnail_set.all()]
        # Files are deleted on commit (#20).
        with self.captureOnCommitCallbacks(execute=True):
            self._run('--merge')
        self.assertEqual(list(Image.objects.values_list('pk', flat=True)), [keep.pk])
        pin_a.refresh_from_db()
        pin_b.refresh_from_db()
        self.assertEqual(pin_a.image_id, keep.pk)
        self.assertEqual(pin_b.image_id, keep.pk)
        for f in files:
            self.assertFalse(f.storage.exists(f.name), f.name)

    def test_should_not_merge_across_users_or_unattached(self):
        create_pin(self.owner, create_image(), [])
        create_pin(self.other, create_image(), [])
        create_image(uploaded_by=self.owner)
        self._run('--merge')
        self.assertEqual(Image.objects.count(), 3)
