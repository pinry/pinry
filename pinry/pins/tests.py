from django.core.urlresolvers import reverse
from django.test import TestCase

from pinry.core.models import User


class CreateImageTest(TestCase):
    fixtures = ['test_resources.json']

    def setUp(self):
        self.client.login(username='jdoe', password='password')

    def test_form_post_unauthenticated(self):
        post_data = {
            'image': 'foobar.jpg'
        }
        self.client.logout()
        response = self.client.post(reverse('pins:new-pin'), data=post_data)
        expected_url = '{login_url}?next={next_url}'.format(**{
            'login_url': reverse('core:login'),
            'next_url': reverse('pins:new-pin')
        })
        self.assertRedirects(response, expected_url=expected_url)

    def test_form_post_browser(self):
        post_data = {
            'image': 'foobar.jpg'
        }
        response = self.client.post(reverse('pins:new-pin'), data=post_data)
        self.assertEqual(response.status_code, 200)

    def test_form_post_ajax(self):
        post_data = {
            'image': 'foobar.jpg'
        }
        response = self.client.post(reverse('pins:new-pin'), data=post_data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)