import mock

from django_images.models import Thumbnail
from taggit.models import Tag
from tastypie.exceptions import Unauthorized
from tastypie.test import ResourceTestCase

from .helpers import ImageFactory, PinFactory, UserFactory
from ..models import Pin, Image
from ...users.models import User


__all__ = ['ImageResourceTest', 'PinResourceTest']


def filter_generator_for(size):
    def wrapped_func(obj):
        return Thumbnail.objects.get_or_create_at_size(obj.pk, size)
    return wrapped_func


def mock_requests_get(url):
    response = mock.Mock(content=open('logo.png', 'rb').read())
    return response


class ImageResourceTest(ResourceTestCase):
    def test_post_create_unsupported(self):
        """Make sure that new images can't be created using API"""
        response = self.api_client.post('/api/v1/image/', format='json', data={})
        self.assertHttpUnauthorized(response)

    def test_list_detail(self):
        image = ImageFactory()
        thumbnail = filter_generator_for('thumbnail')(image)
        standard = filter_generator_for('standard')(image)
        square = filter_generator_for('square')(image)
        response = self.api_client.get('/api/v1/image/', format='json')
        self.assertDictEqual(self.deserialize(response)['objects'][0], {
            u'image': unicode(image.image.url),
            u'height': image.height,
            u'width': image.width,
            u'standard': {
                u'image': unicode(standard.image.url),
                u'width': standard.width,
                u'height': standard.height,
            },
            u'thumbnail': {
                u'image': unicode(thumbnail.image.url),
                u'width': thumbnail.width,
                u'height': thumbnail.height,
            },
            u'square': {
                u'image': unicode(square.image.url),
                u'width': square.width,
                u'height': square.height,
            },
        })


class PinResourceTest(ResourceTestCase):
    def setUp(self):
        super(PinResourceTest, self).setUp()
        self.user = UserFactory(password='password')
        self.api_client.client.login(username=self.user.username, password='password')

    @mock.patch('requests.get', mock_requests_get)
    def test_post_create_url(self):
        url = 'http://testserver/mocked/logo.png'
        post_data = {
            'submitter': '/api/v1/user/1/',
            'url': url,
            'description': 'That\'s an Apple!'
        }
        response = self.api_client.post('/api/v1/pin/', data=post_data)
        self.assertHttpCreated(response)
        self.assertEqual(Pin.objects.count(), 1)
        self.assertEqual(Image.objects.count(), 1)

        # submitter is optional, current user will be used by default
        post_data = {
            'url': url,
            'description': 'That\'s an Apple!',
            'origin': None
        }
        response = self.api_client.post('/api/v1/pin/', data=post_data)
        self.assertHttpCreated(response)

    @mock.patch('requests.get', mock_requests_get)
    def test_post_create_url_with_empty_tags(self):
        url = 'http://testserver/mocked/logo.png'
        post_data = {
            'submitter': '/api/v1/user/1/',
            'url': url,
            'description': 'That\'s an Apple!',
            'tags': []
        }
        response = self.api_client.post('/api/v1/pin/', data=post_data)
        self.assertHttpCreated(response)
        self.assertEqual(Pin.objects.count(), 1)
        self.assertEqual(Image.objects.count(), 1)
        pin = Pin.objects.get(url=url)
        self.assertEqual(pin.tags.count(), 0)

    @mock.patch('requests.get', mock_requests_get)
    def test_post_create_url_unauthorized(self):
        url = 'http://testserver/mocked/logo.png'
        post_data = {
            'submitter': '/api/v1/user/2/',
            'url': url,
            'description': 'That\'s an Apple!',
            'tags': []
        }
        with self.assertRaises(Unauthorized):
            response = self.api_client.post('/api/v1/pin/', data=post_data)
        self.assertEqual(Pin.objects.count(), 0)
        self.assertEqual(Image.objects.count(), 0)

    @mock.patch('requests.get', mock_requests_get)
    def test_post_create_url_with_empty_origin(self):
        url = 'http://testserver/mocked/logo.png'
        post_data = {
            'submitter': '/api/v1/user/1/',
            'url': url,
            'description': 'That\'s an Apple!',
            'origin': None
        }
        response = self.api_client.post('/api/v1/pin/', data=post_data)
        self.assertHttpCreated(response)
        self.assertEqual(Pin.objects.count(), 1)
        self.assertEqual(Image.objects.count(), 1)
        self.assertEqual(Pin.objects.get(url=url).origin, None)

    @mock.patch('requests.get', mock_requests_get)
    def test_post_create_url_with_origin(self):
        origin = 'http://testserver/mocked/'
        url = origin + 'logo.png'
        post_data = {
            'submitter': '/api/v1/user/1/',
            'url': url,
            'description': 'That\'s an Apple!',
            'origin': origin
        }
        response = self.api_client.post('/api/v1/pin/', data=post_data)
        self.assertHttpCreated(response)
        self.assertEqual(Pin.objects.count(), 1)
        self.assertEqual(Image.objects.count(), 1)
        self.assertEqual(Pin.objects.get(url=url).origin, origin)

    def test_post_create_obj(self):
        image = ImageFactory()
        post_data = {
            'submitter': '/api/v1/user/{}/'.format(self.user.pk),
            'image': '/api/v1/image/{}/'.format(image.pk),
            'description': 'That\'s something else (probably a CC logo)!',
            'tags': ['random', 'tags'],
        }
        response = self.api_client.post('/api/v1/pin/', data=post_data)
        self.assertEqual(self.deserialize(response)['id'], 1)
        self.assertHttpCreated(response)
        # A number of Image objects should stay the same as we are using an existing image
        self.assertEqual(Image.objects.count(), 1)
        self.assertEqual(Pin.objects.count(), 1)
        self.assertEquals(Tag.objects.count(), 2)

    def test_put_detail_unauthenticated(self):
        self.api_client.client.logout()
        uri = '/api/v1/pin/{}/'.format(PinFactory().pk)
        response = self.api_client.put(uri, format='json', data={})
        self.assertHttpUnauthorized(response)

    def test_put_detail_unauthorized(self):
        uri = '/api/v1/pin/{}/'.format(PinFactory(submitter=self.user).pk)
        user = UserFactory(password='password')
        self.api_client.client.login(username=user.username, password='password')
        response = self.api_client.put(uri, format='json', data={})
        self.assertHttpUnauthorized(response)

    def test_put_detail(self):
        pin = PinFactory(submitter=self.user)
        uri = '/api/v1/pin/{}/'.format(pin.pk)
        new = {'description': 'Updated description'}

        response = self.api_client.put(uri, format='json', data=new)
        self.assertHttpAccepted(response)
        self.assertEqual(Pin.objects.count(), 1)
        self.assertEqual(Pin.objects.get(pk=pin.pk).description, new['description'])

    def test_delete_detail_unauthenticated(self):
        uri = '/api/v1/pin/{}/'.format(PinFactory(submitter=self.user).pk)
        self.api_client.client.logout()
        self.assertHttpUnauthorized(self.api_client.delete(uri))

    def test_delete_detail_unauthorized(self):
        uri = '/api/v1/pin/{}/'.format(PinFactory(submitter=self.user).pk)
        User.objects.create_user('test', 'test@example.com', 'test')
        self.api_client.client.login(username='test', password='test')
        self.assertHttpUnauthorized(self.api_client.delete(uri))

    def test_delete_detail(self):
        uri = '/api/v1/pin/{}/'.format(PinFactory(submitter=self.user).pk)
        self.assertHttpAccepted(self.api_client.delete(uri))
        self.assertEqual(Pin.objects.count(), 0)

    def test_get_list_json_ordered(self):
        _, pin = PinFactory(), PinFactory()
        response = self.api_client.get('/api/v1/pin/', format='json', data={'order_by': '-id'})
        self.assertValidJSONResponse(response)
        self.assertEqual(self.deserialize(response)['objects'][0]['id'], pin.id)

    def test_get_list_json_filtered_by_tags(self):
        pin = PinFactory()
        response = self.api_client.get('/api/v1/pin/', format='json', data={'tag': pin.tags.get(pk=1)})
        self.assertValidJSONResponse(response)
        self.assertEqual(self.deserialize(response)['objects'][0]['id'], pin.pk)

    def test_get_list_json_filtered_by_submitter(self):
        pin = PinFactory(submitter=self.user)
        response = self.api_client.get('/api/v1/pin/', format='json', data={'submitter__username': self.user.username})
        self.assertValidJSONResponse(response)
        self.assertEqual(self.deserialize(response)['objects'][0]['id'], pin.pk)

    def test_get_list_json(self):
        image = ImageFactory()
        pin = PinFactory(**{
            'submitter': self.user,
            'image': image,
            'url': 'http://testserver/mocked/logo.png',
            'description': u'Mocked Description',
            'origin': None
        })
        standard = filter_generator_for('standard')(image)
        thumbnail = filter_generator_for('thumbnail')(image)
        square = filter_generator_for('square')(image)
        response = self.api_client.get('/api/v1/pin/', format='json')
        self.assertValidJSONResponse(response)
        self.assertDictEqual(self.deserialize(response)['objects'][0], {
            u'id': pin.id,
            u'submitter': {
                u'username': unicode(self.user.username),
                u'gravatar': unicode(self.user.gravatar)
            },
            u'image': {
                u'image': unicode(image.image.url),
                u'width': image.width,
                u'height': image.height,
                u'standard': {
                    u'image': unicode(standard.image.url),
                    u'width': standard.width,
                    u'height': standard.height,
                },
                u'thumbnail': {
                    u'image': unicode(thumbnail.image.url),
                    u'width': thumbnail.width,
                    u'height': thumbnail.height,
                },
                u'square': {
                    u'image': unicode(square.image.url),
                    u'width': square.width,
                    u'height': square.height,
                    },
            },
            u'url': pin.url,
            u'origin': pin.origin,
            u'description': pin.description,
            u'tags': [tag.name for tag in pin.tags.all()]
        })
