"""Lends permissions."""

# REST Framework
from rest_framework import permissions


class IsOwnerBook(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        """User mut be owner."""

        return request.user == obj.owner


class IsTakedUser(permissions.BasePermission):

    pass
