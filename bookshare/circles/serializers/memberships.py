"""Memberships serializers."""

# REST Framwork
from rest_framework import serializers

# Serializers
from bookshare.users.serializers import UserModelSerializer

# Models
from bookshare.circles.models import Membership, Invitation

# Utils
from django.utils import timezone

class MembershipModelSerializer(serializers.ModelSerializer):
    """Membership model serializer."""

    user = UserModelSerializer(read_only=True)
    joined_at = serializers.DateTimeField(source='created', read_only=True)
    invited_by = serializers.StringRelatedField()

    class Meta:
        model = Membership
        fields = [
            'user',
            'remaning_invitations',
            'invited_by',
            'is_admin',
            'lends_offered',
            'lends_taked',
            'joined_at'
        ]


class AddMemberSerializer(serializers.Serializer):
    """"""
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    code = serializers.CharField()
    remaning_invitations = serializers.IntegerField()

    def validate_user(self, data):
        """Verify is user is already in the circle."""

        self.circle = self.context.get('circle')

        query = Membership.objects.filter(
            circle=self.circle,
            user=data
        )
        if query.exists():
            raise serializer.ValidationError('User is already a member.')

        return data

    def validate_code(self, data):
        """Verify is the code is valid."""

        try:
            query = Invitation.objects.get(
                code=data,
                circle=self.circle,
                used=False
            )
        except Invitation.DoesNotExist:
            raise serializer.ValidationError('Invalid code.')

        self.invitation = query

        return data

    def validate(self, data):
        """Validate if a new member can be added."""

        if self.circle.members_limit != 0:
            counter = self.circle.members.count()
            diff = self.circle.members_limit - counter
            if diff <= 0:
                raise serializers.ValidationError('Circles has reached his members limit')

        return data


    def create(self, validated_data):


        member = Membership.objects.create(
            circle=self.circle,
            invited_by=self.invitation.issued_by,
            user=validated_data['user'],
            is_admin=False,
            is_active=True,
            remaning_invitations=validated_data['remaning_invitations']
        )

        # Updates

        # Invitation
        self.invitation.used_by = validated_data['user']
        self.invitation.used = True
        self.invitation.used_at = timezone.now()
        self.invitation.save()

       # Issuer
        issuer = Membership.objects.get(
            user=self.invitation.issued_by,
            circle=self.circle
        )
        issuer.remaning_invitations -= 1
        issuer.save()

        return member
