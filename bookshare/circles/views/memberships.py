"""Memberships views."""

# REST Framework
from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

# Django
from django.shortcuts import get_object_or_404

# Models
from bookshare.circles.models import Circle, Invitation, Membership

# Permissions
from bookshare.circles.permissions import IsActiveMember, IsSelfMember, IsCircleAdmin
from rest_framework.permissions import IsAuthenticated

# Serializers
from bookshare.circles.serializers import MembershipModelSerializer, AddMemberSerializer


class MembershipViewSet(viewsets.ModelViewSet):
    """Membership model view set."""

    serializer_class = MembershipModelSerializer

    def dispatch(self, request, *args, **kwargs):
        """Verify if the slug_name exist."""

        slug_name = kwargs['slug_name']
        self.circle = get_object_or_404(Circle, slug_name=slug_name)
        return super(MembershipViewSet, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        queryset = Membership.objects.filter(circle=self.circle, is_active=True)
        return queryset


    def get_permissions(self):
        permissions = [IsAuthenticated]
        if self.action != 'create':
            permissions.append(IsActiveMember)
        if self.action == 'invitations':
            permissions.append(IsSelfMember)
        if self.action == 'destroy':
            permissions.append(IsSelfMember|IsCircleAdmin)
        return [permission() for permission in permissions]

    def get_object(self):
        """Get membership."""
        return get_object_or_404(
            Membership,
            circle=self.circle,
            user__username=self.kwarg['pk'],
            is_active=True
        )

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()


    @action(methods=['POST'], detail=True)
    def invitations(self, request, *args, **kwargs):
        member = self.get_object()

        invitations_code = Invitations.objects.filter(
            issued_by=request.user,
            circle=self.circle,
            used=False
        ).values_list('code')

        invitations_left = member.remaning_invitations - len(invitations_code)

        invitations = [x[0] for x in invitations_code]
        for invitation in range(invitations_left):
            invitations.append(
                Invitation.objects.create(
                    issued_by=request.user,
                    circle=self.circle
                ).code
            )
        data = {
            'used_invitations': MembershipModelSerializer(invited_members, many=True).data,
            'invitations': invitations
        }
        return Response(data)

    def create(self,request, *args, **kwargs):
        """Handle the creation of a membership."""

        serializer = AddMemberSerializer(
            data=request.data,
            context = {
                'circle': self.circle
            }
        )

        serializer.is_valid(raise_exception=True)
        member = serializer.save()

        data = MembershipModelSerializer(member).data

        return Response(data, status=status.HTTP_201_CREATED)
