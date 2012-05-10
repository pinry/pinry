from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse

from .forms import PinForm


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
            'url': 'https://github.com/overshard/pinry/raw/master/screenshot.png',
        })
        self.assertEqual(response.status_code, 302)
    
    def test_new_pin_fail(self):
        # Invalid protocol
        response = self.client.post(self.url, {
            'url': 'ftp://github.com/overshard/pinry/raw/master/screenshot.png',
        })
        self.assertEqual(response.status_code, 200)
        #self.assertFormError(response, PinForm(), 'url',
        #    'Currently only support HTTP and HTTPS protocols, please be sure you include this in the URL.')

        # Invalid file type.
        response = self.client.post(self.url, {
            'url': 'https://raw.github.com/overshard/pinry/master/README.md',
        })
        self.assertEqual(response.status_code, 200)

        # Already Pinned
        response = self.client.post(self.url, {
            'url': 'https://github.com/overshard/pinry/raw/master/screenshot.png',
        })
        response = self.client.post(self.url, {
            'url': 'https://github.com/overshard/pinry/raw/master/screenshot.png',
        })
        self.assertEqual(response.status_code, 200)
