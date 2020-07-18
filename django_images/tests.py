from io import BytesIO

import mock
import qrcode
from django.test import TestCase
from django.core.files.images import ImageFile
from django.conf import settings
from django_images.models import Image, Thumbnail
from django_images.templatetags.images import at_size
from django_images.utils import scale_and_crop_single
from PIL import Image as PILImage


class ImageModelTest(TestCase):
    def setUp(self):
        image_obj = BytesIO()
        qrcode_obj = qrcode.make('https://mirumee.com/')
        qrcode_obj.save(image_obj)
        self.image = Image.objects.create(width=370, height=370,
                                          image=ImageFile(image_obj, '01.png'))

    def test_get_by_size(self):
        size = list(settings.IMAGE_SIZES.keys())[0]
        Thumbnail.objects.get_or_create_at_sizes(self.image, [size])
        self.image.get_by_size(size)

    def test_get_absolute_url(self):
        url = self.image.get_absolute_url()
        self.assertEqual(url, self.image.image.url)
        # For thumbnail
        size = list(settings.IMAGE_SIZES.keys())[0]
        thumb = Thumbnail.objects.get_or_create_at_sizes(self.image, [size])[0]
        url = self.image.get_absolute_url(size)
        self.assertEqual(url, thumb.image.url)


class ThumbnailManagerModelTest(TestCase):
    def setUp(self):
        image_obj = BytesIO()
        qrcode_obj = qrcode.make('https://mirumee.com/')
        qrcode_obj.save(image_obj)
        self.image = Image.objects.create(width=370, height=370,
                                          image=ImageFile(image_obj, '01.png'))
        self.size = list(settings.IMAGE_SIZES.keys())[0]

    def test_unknown_size(self):
        self.assertRaises(ValueError, Thumbnail.objects.get_or_create_at_sizes,
                          self.image, ['foo'])

    # TODO: Test the image object and data
    def test_create(self):
        Thumbnail.objects.get_or_create_at_sizes(self.image, [self.size])
        self.assertEqual(self.image.thumbnail_set.count(), 1)

    def test_get(self):
        thumb = Thumbnail.objects.get_or_create_at_sizes(self.image, [self.size])[0]
        thumb2 = Thumbnail.objects.get_or_create_at_sizes(self.image, [self.size])[0]
        self.assertEqual(thumb.id, thumb2.id)


class ThumbnailModelTest(TestCase):
    def setUp(self):
        image_obj = BytesIO()
        qrcode_obj = qrcode.make('https://mirumee.com/')
        qrcode_obj.save(image_obj)
        self.image = Image.objects.create(width=370, height=370,
                                          image=ImageFile(image_obj, '01.png'))
        size = list(settings.IMAGE_SIZES.keys())[0]
        self.thumb = Thumbnail.objects.get_or_create_at_sizes(self.image, [size])[0]

    def test_get_absolute_url(self):
        url = self.thumb.get_absolute_url()
        self.assertEqual(url, self.thumb.image.url)


class PostSaveSignalOriginalChangedTestCase(TestCase):
    def setUp(self):
        image_obj = BytesIO()
        qrcode_obj = qrcode.make('https://mirumee.com/')
        qrcode_obj.save(image_obj)
        self.image = Image.objects.create(width=370, height=370,
                                          image=ImageFile(image_obj, '01.png'))
        size = list(settings.IMAGE_SIZES.keys())[0]
        self.thumb = Thumbnail.objects.get_or_create_at_sizes(self.image, [size])[0]

    def test_post_save_signal_original_changed(self):
        size = list(settings.IMAGE_SIZES.keys())[0]
        Thumbnail.objects.get_or_create_at_sizes(self.image, [size])
        self.image.delete()
        self.assertFalse(Thumbnail.objects.exists())


class PostDeleteSignalDeleteImageFileTest(TestCase):
    def setUp(self):
        image_obj = BytesIO()
        qrcode_obj = qrcode.make('https://mirumee.com/')
        qrcode_obj.save(image_obj)
        self.image = Image.objects.create(width=370, height=370,
                                          image=ImageFile(image_obj, '01.png'))
        size = list(settings.IMAGE_SIZES.keys())[0]
        self.thumb = Thumbnail.objects.get_or_create_at_sizes(self.image, [size])[0]

    @mock.patch('django_images.models.IMAGE_AUTO_DELETE', True)
    def test_post_delete_signal_delete_image_files_enabled(self):
        storage = self.image.image.storage
        image_name = self.image.image.name
        thumb_name = self.thumb.image.name
        self.image.delete()
        self.assertFalse(storage.exists(image_name))
        self.assertFalse(storage.exists(thumb_name))

    @mock.patch('django_images.models.IMAGE_AUTO_DELETE', False)
    def test_post_delete_signal_delete_image_files_disabled(self):
        storage = self.image.image.storage
        image_name = self.image.image.name
        thumb_name = self.thumb.image.name
        # Delete thumb
        self.thumb.delete()
        self.assertTrue(storage.exists(image_name))
        self.assertTrue(storage.exists(thumb_name))
        # Delete image
        self.image.delete()
        self.assertTrue(storage.exists(image_name))
        self.assertTrue(storage.exists(thumb_name))


class AtSizeTemplateTagTest(TestCase):
    def setUp(self):
        image_obj = BytesIO()
        qrcode_obj = qrcode.make('https://mirumee.com/')
        qrcode_obj.save(image_obj)
        self.image = Image.objects.create(width=370, height=370,
                                          image=ImageFile(image_obj, '01.png'))
        size = list(settings.IMAGE_SIZES.keys())[0]
        self.thumb = Thumbnail.objects.get_or_create_at_sizes(self.image, [size])[0]

    def test_at_size(self):
        size = list(settings.IMAGE_SIZES.keys())[0]
        url = at_size(self.image, size)
        self.assertEqual(url, self.thumb.image.url)


class UtilsScaleAndDropTest(TestCase):
    def setUp(self):
        image_obj = BytesIO()
        qrcode_obj = qrcode.make('https://mirumee.com/')
        qrcode_obj.save(image_obj)
        self.image = PILImage.open(image_obj)

    def test_change_size(self):
        new_size = (10, 10)
        image = scale_and_crop_single(self.image, new_size)
        self.assertEqual(new_size, image.size)

    def test_crop(self):
        new_size = (10, 10)
        image = scale_and_crop_single(self.image, new_size, crop=True)
        self.assertEqual(new_size, image.size)

    def test_disabled_upscale(self):
        image = scale_and_crop_single(self.image, (740, 740), upscale=False)
        self.assertLess(image.size[0], 371)
        self.assertLess(image.size[1], 371)

    def test_enaabled_upscale(self):
        image = scale_and_crop_single(self.image, (740, 740), upscale=True)
        self.assertGreater(image.size[0], 371)
        self.assertGreater(image.size[1], 371)

    def test_not_change_quality(self):
        image = scale_and_crop_single(self.image, (10, 10), quality=None)
        self.assertEqual(image.info.get('quality'), None)

    def test_change_quality(self):
        image = scale_and_crop_single(self.image, (10, 10), quality=50)
        self.assertEqual(image.info.get('quality'), 50)
