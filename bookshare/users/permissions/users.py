"""Users permissions."""

# REST Framework
from rest_framework import permissions


class IsAccountOwner(permissions.BasePermission):
    """
    User must be equal to the user requested.
    """

    def has_object_permissions(self, request, view, obj):
        """Check if user and obj are the same."""
        return request.user == obj
