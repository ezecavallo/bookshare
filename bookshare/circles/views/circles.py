"""Circles views."""

# REST Framework
from rest_framework import viewsets, mixins
from rest_framework.response import Response

# Models
from bookshare.circles.models import Membership, Circle

# Serializers
from bookshare.circles.serializers import CircleModelSerializer

# Permissions
from bookshare.circles.permissions import IsCircleAdmin
from rest_framework.permissions import IsAuthenticated

class CircleViewSet(mixins.CreateModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.ListModelMixin,
                    viewsets.GenericViewSet):
    """
    Circle viewset.
    """

    serializer_class = CircleModelSerializer
    lookup_field = 'slug_name'

    def get_permissions(self):
        """Permissions based in actions."""
        permissions = [IsAuthenticated]
        if self.action in ['update', 'partial_update']:
            permissions.append(IsCircleAdmin)

        return [p() for p in permissions]

    def get_queryset(self):
        """Specify and limit queryset in list action."""
        queryset = Circle.objects.all()

        if self.action == 'list':
            queryset = Circle.objects.filter(is_public=True)

        return queryset

    def perform_create(self, serializer):
        """Create the relationship user and circle when this last its created."""

        user = self.request.user
        circle = serializer.save()
        Membership.objects.create(
            user=user,
            circle=circle,
            is_admin=True,
            remaning_invitations=10,
        )
