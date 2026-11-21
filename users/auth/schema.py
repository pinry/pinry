from drf_spectacular.extensions import OpenApiAuthenticationExtension


class OptionalBasicAuthenticationScheme(OpenApiAuthenticationExtension):
    target_class = "users.auth.throttling.OptionalBasicAuthentication"
    name = "basicAuth"

    def get_security_definition(self, auto_schema):
        return {"type": "http", "scheme": "basic"}
