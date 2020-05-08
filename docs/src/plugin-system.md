# New plugin system for Pinry

New plugin system is under development and a naive version has been released.

A `PinryPlugin` is a python class or object which is callable.
The plugin loader will call the `Plugin` target only once and use the plugin
instance after specified events triggered just like the way django-middleware works.

You could create a plugin as python-package with content below:

```
from core.models import Image
from django_images.models import Thumbnail


class Plugin:
    
    def __init__(self):
        # do something you want, just be called only once
        pass

    def process_image_pre_creation(self, django_settings, image_instance: Image):
        pass

    def process_thumbnail_pre_creation(self, django_settings, thumbnail_instance: Thumbnail):
        pass

```


You could make some changes on Image object and Thumbnail object 
before they actually be saved (for example, add water-mark to them).

You could access example plugin via `pinry_plugins/batteries/plugin_example.py`.

After all, enable the plugin in local_settings.py:

```
ENABLED_PLUGINS = [
    'pinry_plugins.batteries.plugin_example.Plugin',
]
```

Now the plugin will work like a charm!

# List of Available Plugins

left blank to fill, coming soon...


# Install Plugin in Docker
If you have a plugin named `hello.py` and it have a `Plugin` class inside.

You could just copy it to directory `pinry_plugins/batteries`.

Now add config to local_settings.py

```
ENABLED_PLUGINS = [
    'pinry_plugins.batteries.hello.Plugin',
]
```

Then, rebuild your docker image, the plugin will work 
if no further python dependencies required.
