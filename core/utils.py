import hashlib
import os


def upload_path(instance, filename, **kwargs):
    hasher = hashlib.md5()
    for chunk in instance.image.chunks():
        hasher.update(chunk)
    hash = hasher.hexdigest()
    base, ext = os.path.splitext(filename)
    return '%(first)s/%(second)s/%(hash)s/%(base)s%(ext)s' % {
        'first': hash[0],
        'second': hash[1],
        'hash': hash,
        'base': base,
        'ext': ext,
    }
