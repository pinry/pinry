from django.utils import unittest
from django.test.client import Client
from django.core.urlresolvers import reverse


# pylint: disable-msg=E1103


class HomeTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('core:home')

    def test_url(self):
        self.assertEqual(self.url, '/')

    def test_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)


class RegisterTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('core:register')

    def test_url(self):
        self.assertEqual(self.url, '/register/')

    def test_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_successful_registration(self):
        # If 302 was success, if 200 same page registration failed.
        response = self.client.post(self.url, {
            'username': 'test_registration_success',
            'password1': 'test_password',
            'password2': 'test_password',
        })
        self.assertEqual(response.status_code, 302)

    def test_failed_registration(self):
        # If 302 was success, if 200 same page registration failed.
        response = self.client.post(self.url, {
            'username': 'test_registration_failed',
            'password1': 'test_password',
            'password2': 'test_wrong_password',
        })
        self.assertEqual(response.status_code, 200)


class LoginTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('core:login')

    def test_url(self):
        self.assertEqual(self.url, '/login/')

    def test_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)


class LogoutTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('core:logout')
        self.client.post(self.url, {
            'username': 'test_user_logout',
            'password1': 'test_password',
            'password2': 'test_password',
        })

    def test_url(self):
        self.assertEqual(self.url, '/logout/')

    def test_logout_with_logged_in_user(self):
        self.client.post(self.url, {
            'username': 'test_user_logout',
            'password': 'test_password'
        })
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
