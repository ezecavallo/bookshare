"""Memberships permissions."""

# REST Framework
from rest_framework import permissions

# Models
from bookshare.circles.models import Membership

class IsActiveMember(permissions.BasePermission):

    def has_permission(self, request, view):

        query = Membership.objects.filter(
            user=request.user,
            circle=view.circle,
            is_active=True
        )
        return query.exists()

class IsSelfMember(permissions.BasePermission):

    def has_permission(self, request, view):
        obj = view.kwargs['pk']
        return request.user.username == obj
