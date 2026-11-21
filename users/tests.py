import base64
import json

from django.core.cache import cache
from django.test import Client, TestCase
from django.test.utils import override_settings

from unittest import mock
from django.urls import reverse
from rest_framework.reverse import reverse as drf_reverse
from rest_framework.test import APITestCase

from .auth.backends import CombinedAuthBackend
from .auth.throttling import LoginRateThrottle
from .models import User, create_token_if_necessary


def mock_requests_get(url, headers=None):
    response = mock.Mock(content=open('docs/src/imgs/logo-dark.png', 'rb').read())
    return response


class CombinedAuthBackendTest(TestCase):
    def setUp(self):
        self.backend = CombinedAuthBackend()
        self.username = 'jdoe'
        self.email = 'jdoe@example.com'
        self.password = 'password'
        User.objects.create_user(username=self.username, email=self.email, password=self.password)

    def authenticate(self, username, password):
        return self.backend.authenticate(None, username=username, password=password)

    def test_authenticate_email(self):
        self.assertEqual(self.authenticate(self.email, self.password).username, self.username)

    def test_authenticate_email_ignores_case(self):
        self.assertEqual(self.authenticate('JDoe@Example.com', self.password).username, self.username)

    def test_username_is_left_to_model_backend(self):
        self.assertIsNone(self.authenticate(self.username, self.password))

    def test_authenticate_wrong_password(self):
        self.assertIsNone(self.authenticate(self.email, 'wrong-password'))

    def test_authenticate_unknown_user(self):
        self.assertIsNone(self.authenticate('nobody@example.com', 'wrong-password'))

    def test_inactive_user_cannot_log_in(self):
        User.objects.filter(username=self.username).update(is_active=False)
        self.assertIsNone(self.authenticate(self.email, self.password))

    def test_duplicate_email_logs_in_the_one_matching_account(self):
        User.objects.create_user(username='jdoe2', email=self.email, password='other-password')
        self.assertEqual(self.authenticate(self.email, 'other-password').username, 'jdoe2')
        self.assertEqual(self.authenticate(self.email, self.password).username, self.username)

    def test_duplicate_email_with_two_matches_does_not_log_in(self):
        User.objects.create_user(username='jdoe2', email=self.email, password=self.password)
        self.assertIsNone(self.authenticate(self.email, self.password))


class LoginViewTest(TestCase):
    url = '/api/v2/profile/login/'

    def setUp(self):
        cache.clear()
        User.objects.create_user(username='jdoe', email='jdoe@example.com', password='password')

    def tearDown(self):
        cache.clear()

    def login(self, username, password, **extra):
        return self.client.post(
            self.url,
            data=json.dumps({'username': username, 'password': password}),
            content_type='application/json',
            **extra
        )

    def test_login_with_username(self):
        response = self.login('jdoe', 'password')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['username'], 'jdoe')

    def test_login_with_email(self):
        response = self.login('jdoe@example.com', 'password')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['username'], 'jdoe')

    def test_login_with_username_containing_at_sign(self):
        User.objects.create_user(username='a@b.example', email='other@example.com', password='password')
        response = self.login('a@b.example', 'password')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['username'], 'a@b.example')

    def test_login_wrong_password(self):
        response = self.login('jdoe', 'wrong')
        self.assertEqual(response.status_code, 400)

    def test_login_get_not_allowed(self):
        self.assertEqual(self.client.get(self.url).status_code, 405)

    def test_failed_logins_are_throttled(self):
        with mock.patch.object(LoginRateThrottle, 'THROTTLE_RATES', {'login': '3/hour'}):
            for _ in range(3):
                self.assertEqual(self.login('jdoe', 'wrong').status_code, 400)
            response = self.login('jdoe', 'password')
            self.assertEqual(response.status_code, 429)
            self.assertIn('Retry-After', response)
            self.assertIn('password', response.json())
            # Other addresses are not affected.
            response = self.login('jdoe', 'password', REMOTE_ADDR='10.0.0.2')
            self.assertEqual(response.status_code, 200)

    def test_successful_logins_are_not_counted(self):
        with mock.patch.object(LoginRateThrottle, 'THROTTLE_RATES', {'login': '3/hour'}):
            for _ in range(5):
                self.assertEqual(self.login('jdoe', 'password').status_code, 200)

    def test_admin_login_is_throttled_too(self):
        User.objects.filter(username='jdoe').update(is_staff=True)
        with mock.patch.object(LoginRateThrottle, 'THROTTLE_RATES', {'login': '3/hour'}):
            for _ in range(3):
                self.login('jdoe', 'wrong')
            response = self.client.post(
                '/admin/login/', {'username': 'jdoe', 'password': 'password'},
            )
            self.assertEqual(response.status_code, 200)
            self.assertNotIn('_auth_user_id', self.client.session)


class BasicAuthTest(APITestCase):
    url = '/api/v2/profile/users/'

    def setUp(self):
        cache.clear()
        User.objects.create_user(username='jdoe', email='jdoe@example.com', password='password')

    def tearDown(self):
        cache.clear()

    def get(self, password):
        token = base64.b64encode(('jdoe:%s' % password).encode()).decode()
        return self.client.get(self.url, HTTP_AUTHORIZATION='Basic ' + token)

    def test_basic_auth_off_by_default(self):
        response = self.get('password')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, [])

    def test_unauthenticated_write_gets_401(self):
        response = self.client.post('/api/v2/boards/', data={'name': 'x'})
        self.assertEqual(response.status_code, 401)

    @override_settings(ALLOW_BASIC_AUTH=True)
    def test_basic_auth_when_enabled(self):
        response = self.get('password')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['username'], 'jdoe')

    @override_settings(ALLOW_BASIC_AUTH=True)
    def test_basic_auth_is_throttled(self):
        with mock.patch.object(LoginRateThrottle, 'THROTTLE_RATES', {'login': '3/hour'}):
            for _ in range(3):
                self.assertEqual(self.get('wrong').status_code, 401)
            self.assertEqual(self.get('password').status_code, 429)


class CreateUserTest(TestCase):
    password = 'correct horse battery'

    def post(self, **overrides):
        data = {
            'username': 'jdoe',
            'email': 'jdoe@example.com',
            'password': self.password,
            'password_repeat': self.password,
        }
        data.update(overrides)
        return self.client.post(reverse('users:user-list'), data=data)

    def test_create_post(self):
        response = self.post()
        self.assertEqual(response.status_code, 201)
        self.assertTrue(User.objects.get(username='jdoe').check_password(self.password))

    def test_common_password_rejected(self):
        response = self.post(password='password', password_repeat='password')
        self.assertEqual(response.status_code, 400)
        self.assertIn('password', response.json())
        self.assertFalse(User.objects.exists())

    def test_password_similar_to_username_rejected(self):
        response = self.post(username='horsebattery', password='horsebattery1', password_repeat='horsebattery1')
        self.assertEqual(response.status_code, 400)
        self.assertIn('password', response.json())

    def test_long_password_accepted(self):
        password = 'x7!' * 42 + 'ab'
        self.assertEqual(len(password), 128)
        response = self.post(password=password, password_repeat=password)
        self.assertEqual(response.status_code, 201)

    def test_password_over_128_rejected(self):
        password = 'x7!' * 43
        response = self.post(password=password, password_repeat=password)
        self.assertEqual(response.status_code, 400)

    @override_settings(ALLOW_NEW_REGISTRATIONS=False)
    def test_create_post_not_allowed(self):
        response = self.post()
        self.assertEqual(response.status_code, 401)


class LogoutViewTest(TestCase):
    url = '/api/v2/profile/logout/'

    def setUp(self):
        User.objects.create_user(username='jdoe', email='jdoe@example.com', password='password')
        self.client.login(username='jdoe', password='password')

    def test_logout_view(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 204)
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_logout_get_not_allowed(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 405)
        self.assertIn('_auth_user_id', self.client.session)

    def test_logout_needs_csrf(self):
        client = Client(enforce_csrf_checks=True)
        client.login(username='jdoe', password='password')
        response = client.post(self.url)
        self.assertEqual(response.status_code, 403)
        self.assertIn('_auth_user_id', client.session)

    def test_drf_get_logout_is_gone(self):
        self.assertEqual(self.client.get('/api-auth/logout/').status_code, 404)
        self.assertIn('_auth_user_id', self.client.session)


@override_settings(PUBLIC=False)
class PrivateInstanceTest(TestCase):
    def test_anonymous_blocked_from_pins(self):
        self.assertEqual(self.client.get('/api/v2/pins/').status_code, 403)

    def test_anonymous_can_reach_profile_api(self):
        self.assertEqual(self.client.get('/api/v2/profile/users/').status_code, 200)

    def test_anonymous_can_reach_admin_login(self):
        self.assertEqual(self.client.get('/admin/login/').status_code, 200)

    def test_anonymous_blocked_from_rest_of_admin(self):
        self.assertEqual(self.client.get('/admin/').status_code, 403)

    def test_logged_in_user_can_see_pins(self):
        User.objects.create_user(username='jdoe', email='jdoe@example.com', password='password')
        self.client.login(username='jdoe', password='password')
        self.assertEqual(self.client.get('/api/v2/pins/').status_code, 200)

    def test_token_client_can_see_pins(self):
        user = User.objects.create_user(username='jdoe', email='jdoe@example.com', password='password')
        token = create_token_if_necessary(user).key
        response = self.client.get('/api/v2/pins/', HTTP_AUTHORIZATION='Token ' + token)
        self.assertEqual(response.status_code, 200)

    def test_bad_token_is_blocked(self):
        response = self.client.get('/api/v2/pins/', HTTP_AUTHORIZATION='Token nope')
        self.assertEqual(response.status_code, 403)

    def basic(self, password):
        if not User.objects.filter(username='jdoe').exists():
            User.objects.create_user(username='jdoe', email='jdoe@example.com', password='password')
        token = base64.b64encode(('jdoe:%s' % password).encode()).decode()
        return self.client.get('/api/v2/pins/', HTTP_AUTHORIZATION='Basic ' + token)

    def test_basic_auth_blocked_when_disabled(self):
        self.assertEqual(self.basic('password').status_code, 403)

    @override_settings(ALLOW_BASIC_AUTH=True)
    def test_basic_auth_client_can_see_pins_when_enabled(self):
        cache.clear()
        self.assertEqual(self.basic('password').status_code, 200)
        self.assertEqual(self.basic('wrong').status_code, 403)
        cache.clear()


class ProfileViewTest(TestCase):
    def setUp(self):
        self.first_user = User.objects.create_user(username='jdoe', email='jdoe@example.com', password='password')
        self.second_user = User.objects.create_user(username='judy', email='judy@example.com', password='password')
        self.client.login(username='jdoe', email='jdoe@example.com', password='password')

    def test_should_have_access_to_token(self):
        from rest_framework.authtoken.models import Token
        url = drf_reverse('users:user-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['token'], Token.objects.get(user=self.first_user).key)
        self.assertEqual(response.data[0]['email'], self.first_user.email)

    def test_public_profile_should_not_expose_token_or_email(self):
        url = drf_reverse('users:public-user-list')
        for user in (self.first_user, self.second_user):
            response = self.client.get(f"{url}?username={user.username}")
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.data[0]['username'], user.username)
            self.assertNotIn('token', response.data[0])
            self.assertNotIn('email', response.data[0])

    def test_public_profile_should_not_expose_email_to_anonymous(self):
        self.client.logout()
        url = drf_reverse('users:public-user-list')
        response = self.client.get(f"{url}?username={self.second_user.username}")
        self.assertEqual(response.status_code, 200)
        self.assertNotIn('email', response.data[0])
