"""Read settings from environment variables. See .env.example."""
import json
import os

from django.core.exceptions import ImproperlyConfigured


def env_str(name, default=None):
    value = os.environ.get(name, '').strip()
    return value if value else default


def env_flag(name, default=False):
    value = env_str(name)
    if value is None:
        return default
    return value.lower() in ('1', 'true', 'yes', 'on')


def env_int(name, default):
    value = env_str(name)
    if value is None:
        return default
    try:
        return int(value)
    except ValueError:
        raise ImproperlyConfigured('%s must be a whole number' % name)


def env_list(name, default=None):
    """Comma separated values, e.g. "pins.example.com,192.168.1.10"."""
    value = env_str(name)
    if value is None:
        return [] if default is None else default
    return [item.strip() for item in value.split(',') if item.strip()]


def env_json(name, default):
    value = env_str(name)
    if value is None:
        return default
    try:
        return json.loads(value)
    except ValueError:
        raise ImproperlyConfigured('%s must be valid JSON' % name)
