#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pinry.settings.development")
    sys.path.insert(0, './lib/python2.7/site-packages')

    print(sys.path)

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
