# New plugin system for Pinry

New plugin system is under development.

Now you could access it via project example plugin file `pinry_plugins/batteries/plugin_example.py`.

You could create a simple plugin which has a class which owns methods named:

+ process_image_pre_creation
+ process_thumbnail_pre_creation
 
And, add the plugin class to local_settings.py as:

```
ENABLED_PLUGINS = [
    'pinry_plugins.batteries.plugin_example.Plugin',
]
```

Now the plugin will work like a charm!
