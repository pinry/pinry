import hashlib

from django.contrib.auth.models import User as BaseUser
from django.db.models.signals import post_save
from django.dispatch import receiver


def create_token_if_necessary(user: BaseUser):
    from rest_framework.authtoken.models import Token
    token = Token.objects.filter(user=user).first()
    if token is not None:
        return token
    else:
        return Token.objects.create(user=user)


class User(BaseUser):

    @property
    def gravatar(self):
        return hashlib.md5(self.email.encode('utf-8')).hexdigest()

    class Meta:
        proxy = True


@receiver(post_save, sender=User)
def create_profile(sender, instance: User, **kwargs):
    create_token_if_necessary(instance)
