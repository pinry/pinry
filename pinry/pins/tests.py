from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse


# pylint: disable-msg=E1103
# pylint: disable-msg=R0904


class RecentPinsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('pins:recent-pins')

    def test_url(self):
        self.assertEqual(self.url, '/pins/')

    def test_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)


class NewPinTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('pins:new-pin')

    def test_url(self):
        self.assertEqual(self.url, '/pins/new-pin/')

    def test_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_new_pin(self):
        response = self.client.post(self.url, {
            'url': 'https://github.com/overshard/pinry/raw/master/'
                   'screenshot.png',
        })
        self.assertEqual(response.status_code, 302)

    def test_new_pin_invalid_protocol(self):
        response = self.client.post(self.url, {
            'url': 'ftp://github.com/overshard/pinry/raw/master/'
                   'screenshot.png',
        })
        self.assertEqual(response.status_code, 200)

    def test_new_pin_invalid_file_type(self):
        response = self.client.post(self.url, {
            'url': 'https://raw.github.com/overshard/pinry/master/README.md',
        })
        self.assertEqual(response.status_code, 200)

    def test_new_pin_already_pinned(self):
        response = self.client.post(self.url, {
            'url': 'http://github.com/overshard/pinry/raw/master/'
                   'screenshot.png',
        })
        response = self.client.post(self.url, {
            'url': 'https://github.com/overshard/pinry/raw/master/'
                   'screenshot.png',
        })
        self.assertEqual(response.status_code, 200)
