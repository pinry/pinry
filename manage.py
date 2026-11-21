#!/usr/bin/env python
import atexit
import os
import shutil
import sys
import tempfile

if __name__ == "__main__":
    if not any(arg.startswith("--settings") for arg in sys.argv):
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pinry.settings.development")
    from django.core.management import execute_from_command_line
    if 'test' in sys.argv:
        from django.conf import settings
        settings.IS_TEST = True
        # Give each run its own media folder. Inside a test's transaction,
        # deleting an image never removes its files (that happens on
        # commit), so they would otherwise pile up between runs.
        settings.MEDIA_ROOT = tempfile.mkdtemp(prefix='pinry-test-media-')
        atexit.register(shutil.rmtree, settings.MEDIA_ROOT, ignore_errors=True)

    execute_from_command_line(sys.argv)
