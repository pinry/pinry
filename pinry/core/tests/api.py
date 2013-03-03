import mock

from django.conf import settings

from django_images.models import Thumbnail
from taggit.models import Tag
from tastypie.test import ResourceTestCase

from ..models import Pin, Image
from ...users.models import User


__all__ = ['ImageResourceTest', 'PinResourceTest']


def filter_generator_for(size):
    def wrapped_func(obj):
        return Thumbnail.objects.get_or_create_at_size(obj.pk, size)
    return wrapped_func


def mock_urlopen(url):
    return open('screenshot.png')


def mock_storage_path(self, name):
    if name == 'screenshot.png':
        return settings.SITE_ROOT + 'screenshot.png'
    return name


@mock.patch('django.core.files.storage.FileSystemStorage.path', mock_storage_path)
class ImageResourceTest(ResourceTestCase):
    fixtures = ['test_resources.json']

    def test_post_create_unsupported(self):
        """Make sure that new images can't be created using API"""
        response = self.api_client.post('/api/v1/image/', format='json', data={})
        self.assertHttpUnauthorized(response)

    def test_list_detail(self):
        image = Image.objects.get(pk=1)
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


@mock.patch('django.core.files.storage.FileSystemStorage.path', mock_storage_path)
class PinResourceTest(ResourceTestCase):
    fixtures = ['test_resources.json']

    def setUp(self):
        super(PinResourceTest, self).setUp()

        self.pin_1 = Pin.objects.get(pk=1)
        self.image_url = ''

        self.user = User.objects.get(pk=1)
        self.api_client.client.login(username=self.user.username, password='password')

    @mock.patch('urllib2.urlopen', mock_urlopen)
    def test_post_create_url(self):
        post_data = {
            'submitter': '/api/v1/user/1/',
            'url': 'http://testserver/mocked/screenshot.png',
            'description': 'That\'s an Apple!'
        }
        response = self.api_client.post('/api/v1/pin/', data=post_data)
        self.assertHttpCreated(response)
        self.assertEqual(Pin.objects.count(), 3)
        self.assertEqual(Image.objects.count(), 3)

    @mock.patch('urllib2.urlopen', mock_urlopen)
    def test_post_create_url_empty_tags(self):
        url = 'http://testserver/mocked/screenshot.png'
        post_data = {
            'submitter': '/api/v1/user/1/',
            'url': url,
            'description': 'That\'s an Apple!',
            'tags': []
        }
        response = self.api_client.post('/api/v1/pin/', data=post_data)
        self.assertHttpCreated(response)
        self.assertEqual(Pin.objects.count(), 3)
        self.assertEqual(Image.objects.count(), 3)
        pin = Pin.objects.get(url=url)
        self.assertEqual(pin.tags.count(), 0)

    @mock.patch('urllib2.urlopen', mock_urlopen)
    def test_post_create_url_with_empty_origin(self):
        url = 'http://testserver/mocked/screenshot.png'
        post_data = {
            'submitter': '/api/v1/user/1/',
            'url': url,
            'description': 'That\'s an Apple!',
            'origin': None
        }
        response = self.api_client.post('/api/v1/pin/', data=post_data)
        self.assertHttpCreated(response)
        self.assertEqual(Pin.objects.count(), 3)
        self.assertEqual(Image.objects.count(), 3)
        self.assertEqual(Pin.objects.get(url=url).origin, None)

    @mock.patch('urllib2.urlopen', mock_urlopen)
    def test_post_create_url_with_origin(self):
        origin = 'http://testserver/mocked/'
        url = origin + 'screenshot.png'
        post_data = {
            'submitter': '/api/v1/user/1/',
            'url': url,
            'description': 'That\'s an Apple!',
            'origin': origin
        }
        response = self.api_client.post('/api/v1/pin/', data=post_data)
        self.assertHttpCreated(response)
        self.assertEqual(Pin.objects.count(), 3)
        self.assertEqual(Image.objects.count(), 3)
        self.assertEqual(Pin.objects.get(url=url).origin, origin)

    def test_post_create_obj(self):
        user = User.objects.get(pk=1)
        image = Image.objects.get(pk=1)
        post_data = {
            'submitter': '/api/v1/user/{}/'.format(user.pk),
            'image': '/api/v1/image/{}/'.format(image.pk),
            'description': 'That\'s something else (probably a CC logo)!',
            'tags': ['random', 'tags'],
        }
        response = self.api_client.post('/api/v1/pin/', data=post_data)
        self.assertEqual(self.deserialize(response)['id'], 3)
        self.assertHttpCreated(response)
        # A number of Image objects should stay the same as we are using an existing image
        self.assertEqual(Image.objects.count(), 2)
        self.assertEqual(Pin.objects.count(), 3)
        self.assertEquals(Tag.objects.count(), 4)

    def test_put_detail_unauthenticated(self):
        self.api_client.client.logout()
        uri = '/api/v1/pin/{}/'.format(self.pin_1.pk)
        response = self.api_client.put(uri, format='json', data={})
        self.assertHttpUnauthorized(response)

    def test_put_detail_unauthorized(self):
        uri = '/api/v1/pin/{}/'.format(self.pin_1.pk)
        User.objects.create_user('test', 'test@example.com', 'test')
        self.api_client.client.login(username='test', password='test')
        response = self.api_client.put(uri, format='json', data={})
        self.assertHttpUnauthorized(response)

    def test_put_detail(self):
        uri = '/api/v1/pin/{}/'.format(self.pin_1.pk)
        original = self.deserialize(self.api_client.get(uri, format='json'))
        new = {'description': 'Updated description'}

        response = self.api_client.put(uri, format='json', data=new)
        self.assertHttpAccepted(response)
        self.assertEqual(Pin.objects.count(), 2)
        self.assertEqual(Pin.objects.get(pk=self.pin_1.pk).description, new['description'])

    def test_delete_detail_unauthenticated(self):
        uri = '/api/v1/pin/{}/'.format(self.pin_1.pk)
        self.api_client.client.logout()
        self.assertHttpUnauthorized(self.api_client.delete(uri))

    def test_delete_detail_unauthorized(self):
        uri = '/api/v1/pin/{}/'.format(self.pin_1.pk)
        User.objects.create_user('test', 'test@example.com', 'test')
        self.api_client.client.login(username='test', password='test')
        self.assertHttpUnauthorized(self.api_client.delete(uri))

    def test_delete_detail(self):
        uri = '/api/v1/pin/{}/'.format(self.pin_1.pk)
        self.assertHttpAccepted(self.api_client.delete(uri))
        self.assertEqual(Pin.objects.count(), 1)

    def test_get_list_json_ordered(self):
        pin = Pin.objects.latest('id')
        response = self.api_client.get('/api/v1/pin/', format='json', data={'order_by': '-id'})
        self.assertValidJSONResponse(response)
        self.assertEqual(self.deserialize(response)['objects'][0]['id'], pin.id)

    def test_get_list_json_filtered(self):
        tag = self.pin_1.tags.all()[0]
        response = self.api_client.get('/api/v1/pin/', format='json', data={'tag': tag})
        self.assertValidJSONResponse(response)
        self.assertEqual(self.deserialize(response)['objects'][0]['id'], self.pin_1.id)

    def test_get_list_json(self):
        user = User.objects.get(pk=1)
        image = Image.objects.get(pk=1)
        standard = filter_generator_for('standard')(image)
        thumbnail = filter_generator_for('thumbnail')(image)
        square = filter_generator_for('square')(image)
        response = self.api_client.get('/api/v1/pin/', format='json')
        self.assertValidJSONResponse(response)
        self.assertDictEqual(self.deserialize(response)['objects'][0], {
            u'id': self.pin_1.id,
            u'submitter': {
                u'username': user.username,
                u'gravatar': user.gravatar
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
            u'url': self.pin_1.url,
            u'origin': self.pin_1.origin,
            u'description': self.pin_1.description,
            u'tags': [u'creative-commons'],
        })
