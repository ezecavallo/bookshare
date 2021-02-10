"""Circles permissions."""

# REST Framework
from rest_framework import permissions


class IsCircleAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):

        query = Membership.objects.filter(
            circle=obj,
            user=request.user,
            is_admin=True,
            is_active=True
        )
        return query.exists()
