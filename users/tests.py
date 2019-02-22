from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.utils import override_settings

import mock

from .auth.backends import CombinedAuthBackend
from .models import User


def mock_requests_get(url, headers=None):
    response = mock.Mock(content=open('logo.png', 'rb').read())
    return response


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


class CreateUserTest(TestCase):
    def test_create_post(self):
        data = {
            'username': 'jdoe',
            'email': 'jdoe@example.com',
            'password': 'password'
        }
        response = self.client.post(reverse('users:register'), data=data)
        self.assertRedirects(response, reverse('core:recent-pins'))
        self.assertIn('_auth_user_id', self.client.session)

    @override_settings(ALLOW_NEW_REGISTRATIONS=False)
    def test_create_post_not_allowed(self):
        response = self.client.get(reverse('users:register'))
        self.assertRedirects(response, reverse('core:recent-pins'))


class LogoutViewTest(TestCase):
    def setUp(self):
        User.objects.create_user(username='jdoe', password='password')
        self.client.login(username='jdoe', password='password')

    def test_logout_view(self):
        response = self.client.get(reverse('users:logout'))
        self.assertRedirects(response, reverse('core:recent-pins'))
