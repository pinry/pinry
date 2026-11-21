from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = 'users'

    def ready(self):
        # Registers the user_login_failed receiver for the login throttle.
        from users.auth import throttling  # noqa: F401
        # Describes OptionalBasicAuthentication in the OpenAPI schema.
        from users.auth import schema  # noqa: F401
