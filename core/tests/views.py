from django.core.urlresolvers import reverse
from django.test import TestCase

from core.models import Image
from core.tests import create_user
from users.models import User


__all__ = ['CreateImageTest']


class CreateImageTest(TestCase):
    def setUp(self):
        self.user = create_user("default")
        self.client.login(username=self.user.username, password='password')

    def tearDown(self):
        User.objects.all().delete()
        Image.objects.all().delete()

    def test_post(self):
        with open('logo.png', mode='rb') as image:
            response = self.client.post(reverse('image-list'), {'image': image})
        image = Image.objects.latest('pk')
        self.assertEqual(response.json()['id'], image.pk)

    def test_post_error(self):
        response = self.client.post(reverse('image-list'), {'image': None})
        self.assertEqual(
            response.json(),
            {
                'image': [
                    'The submitted data was not a file. '
                    'Check the encoding type on the form.'
                ]
            }
        )
