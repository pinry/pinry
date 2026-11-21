from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from users.models import User, create_token_if_necessary


class PublicUserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            'gravatar',
            settings.DRF_URL_FIELD_NAME,
        )
        extra_kwargs = {
            settings.DRF_URL_FIELD_NAME: {
                "view_name": "users:public-user-detail",
            },
        }


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            'token',
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
        max_length=128,
    )
    password_repeat = serializers.CharField(
        write_only=True,
        required=True,
        allow_blank=False,
        max_length=128,
    )
    token = serializers.SerializerMethodField(read_only=True)

    def validate(self, attrs):
        attrs = super().validate(attrs)
        if 'password' in attrs:
            candidate = User(
                username=attrs.get('username', ''),
                email=attrs.get('email', ''),
            )
            try:
                validate_password(attrs['password'], user=candidate)
            except DjangoValidationError as e:
                raise ValidationError(
                    detail={"password": list(e.messages)}
                ) from e
        return attrs

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

    def get_token(self, obj: User) -> str | None:
        if self.context['request'].user == obj:
            return create_token_if_necessary(obj).key
        return None
