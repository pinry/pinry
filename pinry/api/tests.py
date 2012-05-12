from django.test import TestCase
from django.test.client import Client


# pylint: disable-msg=R0904
# pylint: disable-msg=E1103


class RecentPinsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = '/api/pin/?format=json'

    def test_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
