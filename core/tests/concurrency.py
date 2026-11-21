import threading
import unittest

from django.db import connection, models
from django.test import TransactionTestCase

from .helpers import create_image, create_pin, create_user
from core.models import Pin, Image, delete_pin_images


@unittest.skipUnless(connection.vendor == 'postgresql',
                     'needs concurrent write transactions (SQLite runs '
                     'one at a time)')
class ConcurrentPinDeleteTests(TransactionTestCase):
    def test_deleting_last_two_pins_at_once_should_remove_image(self):
        # Issue #7: hold both delete transactions after their pin is gone
        # but before the image check, so the two checks overlap.
        image = create_image()
        user = create_user("default")
        pins = [create_pin(user, image, []) for _ in range(2)]
        barrier = threading.Barrier(2, timeout=10)
        errors = []

        def wait_for_other_delete(sender, instance, **kwargs):
            barrier.wait()

        def delete(pk):
            try:
                Pin.objects.get(pk=pk).delete()
            except Exception as e:
                errors.append(e)
            finally:
                connection.close()

        # Receivers run in the order they were connected.
        models.signals.post_delete.disconnect(delete_pin_images, sender=Pin)
        models.signals.post_delete.connect(wait_for_other_delete, sender=Pin)
        models.signals.post_delete.connect(delete_pin_images, sender=Pin)
        try:
            threads = [threading.Thread(target=delete, args=(pin.pk,))
                       for pin in pins]
            for thread in threads:
                thread.start()
            for thread in threads:
                thread.join()
        finally:
            models.signals.post_delete.disconnect(
                wait_for_other_delete, sender=Pin)

        self.assertEqual(errors, [])
        self.assertFalse(Pin.objects.exists())
        self.assertFalse(Image.objects.filter(pk=image.pk).exists())
