"""Notifications serializers."""

# REST Framework
from rest_framework import serializers

# Models
from bookshare.notifications.models import Notification


class NotificationSerializer(serializers.ModelSerializer):

    actor = serializers.StringRelatedField()

    class Meta:
        model = Notification
        fields = [
            'actor',
            'verb',
            'object',
            'target',
            'unread',
            'level',
            'datetime'
        ]
