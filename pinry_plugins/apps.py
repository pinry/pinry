from django.apps import AppConfig


class PinryPluginsConfig(AppConfig):
    name = 'pinry_plugins'

    def ready(self):
        from pinry_plugins import builder   # noqa
        builder.init()
