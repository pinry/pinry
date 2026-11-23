import json

from django.urls import reverse
import mock
from rest_framework import status
from rest_framework.test import APITestCase

from taggit.models import Tag

from .helpers import TEST_IMAGE_PATH, create_image, create_user, create_pin
from core.models import Pin, Image, Board


def _teardown_models():
    Pin.objects.all().delete()
    Image.objects.all().delete()
    Tag.objects.all().delete()
    Board.objects.all().delete()


def mock_requests_get(url, **kwargs):
    response = mock.Mock(content=open('docs/src/imgs/logo-dark.png', 'rb').read())
    return response


def mock_requests_get_with_non_image_content(url, **kwargs):
    response = mock.Mock(content=b"abcd")
    return response


class ImageTests(APITestCase):
    def test_post_create_unsupported(self):
        url = reverse("image-list")
        data = {}
        response = self.client.post(
            url,
            data=data,
            format='json',
        )
        self.assertEqual(response.status_code, 401, response.data)


class BoardPrivacyTests(APITestCase):

    def setUp(self):
        super(BoardPrivacyTests, self).setUp()
        self.owner = create_user("default")
        self.non_owner = create_user("non_owner")

        self.private_board = Board.objects.create(
            name="test_board",
            submitter=self.owner,
            private=True,
        )
        self.board_url = reverse("board-detail", kwargs={"pk": self.private_board.pk})
        self.boards_url = reverse("board-list")

    def tearDown(self):
        _teardown_models()

    def _create_pin_with_non_owner(self, private):
        image = create_image()
        pin = create_pin(self.non_owner, image=image, tags=[])
        pin.private = private
        pin.save()
        return pin

    def test_should_non_owner_and_anonymous_user_has_no_permission_to_list_private_board(self):
        resp = self.client.get(self.boards_url)
        self.assertEqual(len(resp.json()), 0, resp.json())

        self.client.login(username=self.non_owner.username, password='password')
        resp = self.client.get(self.boards_url)
        self.assertEqual(len(resp.json()), 0, resp.content)

    def test_should_owner_has_permission_to_list_private_board(self):
        self.client.login(username=self.non_owner.username, password='password')
        resp = self.client.get(self.boards_url)
        self.assertEqual(len(resp.json()), 0, resp.content)

    def test_should_non_owner_and_anonymous_user_has_no_permission_to_view_private_board(self):
        resp = self.client.get(self.board_url)
        self.assertEqual(resp.status_code, 404)

        self.client.login(username=self.non_owner.username, password='password')
        resp = self.client.get(self.board_url)
        self.assertEqual(resp.status_code, 404)

    def test_should_owner_has_permission_to_view_private_board(self):
        self.client.login(username=self.owner.username, password='password')
        resp = self.client.get(self.board_url)
        self.assertEqual(resp.status_code, 200)

    def test_should_owner_has_no_permission_to_add_private_pin_of_other_user_to_board(self):
        self.client.login(username=self.owner.username, password='password')

        private_pin_of_other_user = self._create_pin_with_non_owner(True)

        resp = self.client.patch(self.board_url, data={"pins_to_add": [private_pin_of_other_user.id, ]})
        self.assertEqual(resp.status_code, 200)

        resp = self.client.get(self.board_url)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()['total_pins'], 0, resp.json())

    def test_should_owner_has_permission_to_add_non_private_pin_of_other_user_to_board(self):
        self.client.login(username=self.owner.username, password='password')

        private_pin_of_other_user = self._create_pin_with_non_owner(False)

        resp = self.client.patch(self.board_url, data={"pins_to_add": [private_pin_of_other_user.id, ]})
        self.assertEqual(resp.status_code, 200)

        resp = self.client.get(self.board_url)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()['total_pins'], 1, resp.json())


class PinPrivacyTests(APITestCase):

    def setUp(self):
        super(PinPrivacyTests, self).setUp()
        self.owner = create_user("default")
        self.non_owner = create_user("non_owner")

        with mock.patch('requests.get', mock_requests_get):
            image = create_image()
        self.private_pin = Pin.objects.create(
            submitter=self.owner,
            image=image,
            private=True,
        )
        self.private_pin_url = reverse("pin-detail", kwargs={"pk": self.private_pin.pk})

        self.board = Board.objects.create(name="test_board", submitter=self.owner)
        self.board.pins.add(self.private_pin)
        self.board.save()
        self.board_url = reverse("board-detail", kwargs={"pk": self.board.pk})

    def tearDown(self):
        _teardown_models()

    def test_should_non_owner_and_anonymous_user_has_no_permission_to_list_private_pin(self):
        resp = self.client.get(reverse("pin-list"))
        self.assertEqual(len(resp.json()['results']), 0, resp.content)

        self.client.login(username=self.non_owner.username, password='password')
        resp = self.client.get(reverse("pin-list"))
        self.assertEqual(len(resp.json()['results']), 0, resp.content)

    def test_should_owner_user_has_permission_to_list_private_pin(self):
        self.client.login(username=self.owner.username, password='password')
        resp = self.client.get(reverse("pin-list"))
        self.assertEqual(len(resp.json()['results']), 1, resp.content)

    def test_should_owner_has_permission_to_view_private_pin(self):
        self.client.login(username=self.owner.username, password='password')
        resp = self.client.get(self.private_pin_url)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()['id'], self.private_pin.id)

    def test_should_anonymous_user_has_no_permission_to_view_private_pin(self):
        resp = self.client.get(self.private_pin_url)
        self.assertEqual(resp.status_code, 404)

    def test_should_non_owner_has_no_permission_to_view_private_pin(self):
        self.client.login(username=self.non_owner.username, password='password')
        resp = self.client.get(self.private_pin_url)
        self.assertEqual(resp.status_code, 404)


class PinTests(APITestCase):
    _JSON_TYPE = "application/json"

    def setUp(self):
        super(PinTests, self).setUp()
        self.user = create_user("default")
        self.client.login(username=self.user.username, password='password')

    def tearDown(self):
        _teardown_models()

    @mock.patch('requests.get', mock_requests_get_with_non_image_content)
    def test_should_not_create_pin_if_url_content_invalid(self):
        url = 'http://testserver.com/mocked/logo-01.png'
        create_url = reverse("pin-list")
        referer = 'http://testserver.com/'
        post_data = {
            'url': url,
            'private': False,
            'referer': referer,
            'description': 'That\'s an Apple!'
        }
        response = self.client.post(create_url, data=post_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @mock.patch('requests.get', mock_requests_get)
    def test_should_create_pin(self):
        url = 'http://testserver.com/mocked/logo-01.png'
        create_url = reverse("pin-list")
        referer = 'http://testserver.com/'
        post_data = {
            'url': url,
            'private': False,
            'referer': referer,
            'description': 'That\'s an Apple!'
        }
        response = self.client.post(create_url, data=post_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        pin = Pin.objects.get(url=url)
        self.assertIsNotNone(pin.image.image)

    @mock.patch('requests.get', mock_requests_get)
    def test_post_create_url_with_empty_tags(self):
        url = 'http://testserver.com/mocked/logo-02.png'
        create_url = reverse("pin-list")
        referer = 'http://testserver.com/'
        post_data = {
            'url': url,
            'referer': referer,
            'description': 'That\'s an Apple!',
            'tags': []
        }
        response = self.client.post(create_url, data=post_data, format="json")
        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED, response.json()
        )
        self.assertEqual(Image.objects.count(), 1)
        pin = Pin.objects.get(url=url)
        self.assertIsNotNone(pin.image.image)
        self.assertEqual(pin.tags.count(), 0)

    def test_should_post_create_pin_with_existed_image(self):
        image = create_image()
        create_pin(self.user, image=image, tags=[])
        create_url = reverse("pin-list")
        referer = 'http://testserver.com/'
        post_data = {
            'referer': referer,
            'image_by_id': image.pk,
            'description': 'That\'s something else (probably a CC logo)!',
            'tags': ['random', 'tags'],
        }
        response = self.client.post(create_url, data=post_data, format="json")
        resp_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, resp_data)
        self.assertEqual(
            resp_data['description'],
            'That\'s something else (probably a CC logo)!',
            resp_data
        )
        self.assertEquals(Pin.objects.count(), 2)

    def test_patch_detail_unauthenticated(self):
        image = create_image()
        pin = create_pin(self.user, image, [])
        self.client.logout()
        uri = reverse("pin-detail", kwargs={"pk": pin.pk})
        response = self.client.patch(uri, format='json', data={})
        self.assertEqual(response.status_code, 401, response.data)

    def test_patch_detail(self):
        image = create_image()
        pin = create_pin(self.user, image, [])
        uri = reverse("pin-detail", kwargs={"pk": pin.pk})
        new = {'description': 'Updated description'}

        response = self.client.patch(
            uri, new, format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.json())
        self.assertEqual(Pin.objects.count(), 1)
        self.assertEqual(Pin.objects.get(pk=pin.pk).description, new['description'])

    def test_delete_detail_unauthenticated(self):
        image = create_image()
        pin = create_pin(self.user, image, [])
        uri = reverse("pin-detail", kwargs={"pk": pin.pk})
        self.client.logout()
        resp = self.client.delete(uri)
        self.assertEqual(resp.status_code, 401, resp.data)

    def test_delete_detail(self):
        image = create_image()
        pin = create_pin(self.user, image, [])
        uri = reverse("pin-detail", kwargs={"pk": pin.pk})
        self.client.delete(uri)
        self.assertEqual(Pin.objects.count(), 0)


class PinImageOwnershipTests(APITestCase):
    """A pin may only reuse an image that belongs to its submitter."""

    def setUp(self):
        super(PinImageOwnershipTests, self).setUp()
        self.owner = create_user("image_owner")
        self.other = create_user("other")

    def tearDown(self):
        _teardown_models()

    def _login(self, user):
        self.client.logout()
        self.client.login(username=user.username, password='password')

    def _upload_image(self, user):
        self._login(user)
        with open(TEST_IMAGE_PATH, 'rb') as fp:
            resp = self.client.post(
                reverse("image-list"), {"image": fp}, format="multipart",
            )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED, resp.content)
        return resp.json()['id']

    def _create_pin(self, user, image_id, private=False):
        self._login(user)
        return self.client.post(
            reverse("pin-list"),
            data={'image_by_id': image_id, 'private': private},
            format="json",
        )

    def _owner_pin(self, private=False):
        image_id = self._upload_image(self.owner)
        resp = self._create_pin(self.owner, image_id, private=private)
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED, resp.content)
        return Pin.objects.get(pk=resp.json()['id'])

    def test_upload_pin_delete_flow(self):
        image_id = self._upload_image(self.owner)
        self.assertEqual(Image.objects.get(pk=image_id).owner_id, self.owner.pk)
        resp = self._create_pin(self.owner, image_id)
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED, resp.content)
        pin_id = resp.json()['id']

        resp = self.client.delete(reverse("pin-detail", kwargs={"pk": pin_id}))
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Pin.objects.filter(pk=pin_id).exists())
        self.assertFalse(Image.objects.filter(pk=image_id).exists())

    def test_direct_delete_of_other_users_pin_is_refused(self):
        pin = self._owner_pin()
        self._login(self.other)
        resp = self.client.delete(reverse("pin-detail", kwargs={"pk": pin.pk}))
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Pin.objects.filter(pk=pin.pk).exists())

    def test_cannot_pin_image_of_other_users_public_pin(self):
        pin = self._owner_pin()
        # The image ID of a public pin is part of the public API.
        self.client.logout()
        resp = self.client.get(reverse("pin-detail", kwargs={"pk": pin.pk}))
        image_id = resp.json()['image']['id']
        self.assertEqual(image_id, pin.image_id)

        resp = self._create_pin(self.other, image_id)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST, resp.content)
        self.assertIn('image_by_id', resp.json())
        self.assertFalse(Pin.objects.filter(submitter=self.other).exists())

        # Owner's pin and image survive anything the other user can do.
        self.assertTrue(Pin.objects.filter(pk=pin.pk).exists())
        self.assertTrue(Image.objects.filter(pk=image_id).exists())

    def test_cannot_pin_image_of_other_users_private_pin(self):
        pin = self._owner_pin(private=True)
        resp = self._create_pin(self.other, pin.image_id)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST, resp.content)
        # Refused exactly like a nonexistent ID, so existence is not revealed.
        missing = self._create_pin(self.other, pin.image_id + 1000)
        self.assertEqual(missing.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            resp.json()['image_by_id'][0].replace(str(pin.image_id), 'N'),
            missing.json()['image_by_id'][0].replace(str(pin.image_id + 1000), 'N'),
        )

        self.client.logout()
        resp = self.client.get(reverse("pin-list"))
        self.assertEqual(resp.json()['results'], [], resp.content)

    def test_cannot_pin_other_users_unpinned_upload(self):
        image_id = self._upload_image(self.owner)
        resp = self._create_pin(self.other, image_id)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST, resp.content)
        # The uploader can still pin it afterwards.
        resp = self._create_pin(self.owner, image_id)
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED, resp.content)

    def test_cannot_pin_other_users_image_without_owner(self):
        # Images stored before ownership was recorded have no owner.
        image = create_image()
        create_pin(self.owner, image, [])
        resp = self._create_pin(self.other, image.pk)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST, resp.content)

        orphan = create_image()
        resp = self._create_pin(self.other, orphan.pk)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST, resp.content)

    def test_owner_may_repin_own_image(self):
        pin = self._owner_pin()
        resp = self._create_pin(self.owner, pin.image_id)
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED, resp.content)

    def test_deleting_pin_keeps_image_used_by_another_pin(self):
        first = self._owner_pin()
        resp = self._create_pin(self.owner, first.image_id)
        second_id = resp.json()['id']

        resp = self.client.delete(reverse("pin-detail", kwargs={"pk": second_id}))
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertTrue(Pin.objects.filter(pk=first.pk).exists())
        self.assertTrue(Image.objects.filter(pk=first.image_id).exists())

        resp = self.client.delete(reverse("pin-detail", kwargs={"pk": first.pk}))
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Image.objects.filter(pk=first.image_id).exists())

    def test_deleting_own_pin_keeps_other_users_pin_on_shared_image(self):
        # Data created before this fix may already share an image across users.
        victim_pin = self._owner_pin()
        attacker_pin = create_pin(self.other, victim_pin.image, [])

        self._login(self.other)
        resp = self.client.delete(
            reverse("pin-detail", kwargs={"pk": attacker_pin.pk}),
        )
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Pin.objects.filter(pk=attacker_pin.pk).exists())
        self.assertTrue(Pin.objects.filter(pk=victim_pin.pk).exists())
        self.assertTrue(Image.objects.filter(pk=victim_pin.image_id).exists())
