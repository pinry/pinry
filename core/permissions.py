from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.IsAuthenticatedOrReadOnly):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """
    def __init__(self, owner_field_name="owner"):
        self.__owner_field_name = owner_field_name

    def __call__(self):
        return self

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        return getattr(obj, self.__owner_field_name) == request.user


class OwnerOnlyIfPrivate(permissions.BasePermission):
    def __init__(self, owner_field_name="owner"):
        self.__owner_field_name = owner_field_name

    def __call__(self):
        return self

    def has_object_permission(self, request, view, obj):
        if getattr(obj, "private"):
            return request.user == getattr(obj, self.__owner_field_name)
        return True


class OwnerOnly(permissions.IsAuthenticatedOrReadOnly):

    def has_permission(self, request, view):
        return request.user.is_authenticated()

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class SuperUserOnly(permissions.BasePermission):
    """
    The request is authenticated as a user, or is a read-only request.
    """

    def has_permission(self, request, view):
        return request.user.is_superuser

    def has_object_permission(self, request, view, obj):
        return request.user.is_superuser
