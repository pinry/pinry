#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    if not any(arg.startswith("--settings") for arg in sys.argv):
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pinry.settings.development")
    from django.core.management import execute_from_command_line
    if 'test' in sys.argv:
        from django.conf import settings
        settings.IS_TEST = True

    execute_from_command_line(sys.argv)
