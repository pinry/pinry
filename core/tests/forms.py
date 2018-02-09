from django.test import TestCase
from ..forms import ImageForm


__all__ = ['ImageFormTest']

class ImageFormTest(TestCase):
    def test_image_field_prefix(self):
        """Assert that the image field has a proper name"""
        form = ImageForm()
        self.assertInHTML("<input id='id_qqfile' name='qqfile' type='file' />", str(form))