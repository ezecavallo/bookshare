"""Profiles serializers."""

# REST Framework
from rest_framework import serializers

# Models
from bookshare.users.models import Profile


class ProfileModelSerializer(serializers.ModelSerializer):
    """Model class serializer."""

    class Meta:
        """Meta class."""

        model = Profile
        fields = ['biography', 'picture', 'reputation']
        read_only_fields = ['reputation']
