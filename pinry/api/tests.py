from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse


class RecentPinsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('api:pins-recent', args=[0])

    def test_url(self):
        self.assertEqual(self.url, '/api/pins/recent/0/')

    def test_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
