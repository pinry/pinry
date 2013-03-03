import hashlib

from django.contrib.auth.models import User as BaseUser


class User(BaseUser):
    @property
    def gravatar(self):
        return hashlib.md5(self.email).hexdigest()

    class Meta:
        proxy = True