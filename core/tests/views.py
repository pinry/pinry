from django.test import TestCase

from core.models import Image
from core.tests import create_user, reverse
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
        with open('docs/src/imgs/logo-dark.png', mode='rb') as image:
            response = self.client.post(reverse('image-list'), {'image': image})
        image = Image.objects.latest('pk')
        self.assertEqual(response.json()['id'], image.pk)

    def test_post_error(self):
        response = self.client.post(reverse('image-list'), {'image': ''})
        self.assertEqual(
            response.json(),
            {
                'image': [
                    'The submitted data was not a file. '
                    'Check the encoding type on the form.'
                ]
            }
        )


class TestDocs(TestCase):
    def test_should_doc_api_available_without_error(self):
        response = self.client.get("/api/v2/docs")
        self.assertEqual(response.status_code, 200)
