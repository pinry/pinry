from django.conf import settings
from django.contrib.auth import login
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from users.models import User


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'gravatar',
            'password',
            'password_repeat',
            settings.DRF_URL_FIELD_NAME,
        )
        extra_kwargs = {
            settings.DRF_URL_FIELD_NAME: {
                "view_name": "users:user-detail",
            },
        }

    password = serializers.CharField(
        write_only=True,
        required=True,
        allow_blank=False,
        min_length=6,
        max_length=32,
    )
    password_repeat = serializers.CharField(
        write_only=True,
        required=True,
        allow_blank=False,
        min_length=6,
        max_length=32,
    )

    def create(self, validated_data):
        if validated_data['password'] != validated_data['password_repeat']:
            raise ValidationError(
                detail={
                    "password_repeat": "Tow password doesn't match",
                }
            )
        validated_data.pop('password_repeat')
        password = validated_data.pop('password')
        user = super(UserSerializer, self).create(
            validated_data,
        )
        user.set_password(password)
        user.save()
        login(
            self.context['request'],
            user=user,
            backend=settings.AUTHENTICATION_BACKENDS[0],
        )
        return user
