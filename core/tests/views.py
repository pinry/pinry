from django.conf import settings
from django.core.urlresolvers import reverse
from django.template import TemplateDoesNotExist
from django.test import TestCase

from .api import UserFactory
from ...core.models import Image


__all__ = ['CreateImageTest']


class CreateImageTest(TestCase):
    def setUp(self):
        self.user = UserFactory(password='password')
        self.client.login(username=self.user.username, password='password')

    def test_get_browser(self):
        response = self.client.get(reverse('core:create-image'))
        self.assertRedirects(response, reverse('core:recent-pins'))

    def test_get_xml_http_request(self):
        with self.assertRaises(TemplateDoesNotExist):
            self.client.get(reverse('core:create-image'), HTTP_X_REQUESTED_WITH='XMLHttpRequest')

    def test_post(self):
        with open(settings.SITE_ROOT + 'logo.png', mode='rb') as image:
            response = self.client.post(reverse('core:create-image'), {'qqfile': image})
        image = Image.objects.latest('pk')
        self.assertJSONEqual(response.content, {'success': {'id': image.pk}})

    def test_post_error(self):
        response = self.client.post(reverse('core:create-image'), {'qqfile': None})
        self.assertJSONEqual(response.content, {
            'error': {'image': ['This field is required.']}
        })
