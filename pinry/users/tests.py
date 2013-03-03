from django.test import TestCase

import mock

from .auth.backends import CombinedAuthBackend
from ..core.models import Image, Pin
from .models import User


def mock_urlopen(url):
    return open('screenshot.png')


class CombinedAuthBackendTest(TestCase):
    def setUp(self):
        self.backend = CombinedAuthBackend()
        self.username = 'jdoe'
        self.email = 'jdoe@example.com'
        self.password = 'password'
        User.objects.create_user(username=self.username, email=self.email, password=self.password)

    def test_authenticate_username(self):
        self.assertTrue(self.backend.authenticate(username=self.username, password=self.password))

    def test_authenticate_email(self):
        self.assertTrue(self.backend.authenticate(username=self.email, password=self.password))

    def test_authenticate_wrong_password(self):
        self.assertIsNone(self.backend.authenticate(username=self.username, password='wrong-password'))

    def test_authenticate_unknown_user(self):
        self.assertIsNone(self.backend.authenticate(username='wrong-username', password='wrong-password'))

    @mock.patch('urllib2.urlopen', mock_urlopen)
    def test_has_perm_on_pin(self):
        image = Image.objects.create_for_url('http://testserver/mocked/screenshot.png')
        user = User.objects.get(pk=1)
        pin = Pin.objects.create(submitter=user, image=image)
        self.assertTrue(self.backend.has_perm(user, 'add_pin', pin))

    @mock.patch('urllib2.urlopen', mock_urlopen)
    def test_has_perm_on_pin_unauthorized(self):
        image = Image.objects.create_for_url('http://testserver/mocked/screenshot.png')
        user = User.objects.get(pk=1)
        other_user = User.objects.create_user('test', 'test@example.com', 'test')
        pin = Pin.objects.create(submitter=user, image=image)
        self.assertFalse(self.backend.has_perm(other_user, 'add_pin', pin))