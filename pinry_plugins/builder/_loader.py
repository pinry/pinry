import logging

from django.dispatch import receiver
from django.utils.module_loading import import_string
from django.conf import settings
from django.db import models

from core.models import Image
from django_images.models import Thumbnail

_plugins = getattr(settings, "ENABLED_PLUGINS", [])
_plugin_instances = []


def _load_plugins():
    for plugin_path in _plugins:
        plugin_cls = import_string(plugin_path)
        _plugin_instances.append(plugin_cls())


@receiver(models.signals.pre_save, sender=Image)
def process_image_pre_creation(sender, instance: Image, **kwargs):
    # FIXME(winkidney): May have issue on determining if it
    #  is created or not
    if instance.pk is not None:
        return
    for plugin in _plugin_instances:
        process_fn = getattr(plugin, "process_image_pre_creation")
        try:
            process_fn(
                django_settings=settings,
                image_instance=instance,
            )
        except Exception:
            logging.exception(
                "Error occurs while trying to access plugin's pin_pre_save "
                "for plugin %s" % plugin
            )


@receiver(models.signals.pre_save, sender=Thumbnail)
def process_thumbnail_pre_creation(sender, instance: Thumbnail, **kwargs):
    # FIXME(winkidney): May have issue on determining if it
    #  is created or not
    if instance.pk is not None:
        return

    for plugin in _plugin_instances:
        process_fn = getattr(plugin, "process_thumbnail_pre_creation")
        try:
            process_fn(
                django_settings=settings,
                thumbnail_instance=instance,
            )
        except Exception:
            logging.exception(
                "Error occurs while trying to access plugin's process_thumbnail_pre_creation "
                "for plugin %s" % plugin
            )


def init():
    _load_plugins()
