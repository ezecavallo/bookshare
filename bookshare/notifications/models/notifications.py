"""Notifications models."""

# Django
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.conf import settings

class Notification(models.Model):
    """Notification model."""

    verb = models.CharField(max_length=255)

    SU = 'success'
    IN = 'info'
    WAR = 'warning'
    ER = 'error'

    LEVELS = [
        ('success', 'asdasd'),
        ('info', 'asdasd'),
        ('warning', 'asdasd'),
        ('error', 'asdasd')
    ]
    level = models.CharField(choices=LEVELS, default=IN, max_length=32)

    # Actor
    actor_content_type = models.ForeignKey(
        ContentType,
        related_name='notification_actor',
        on_delete=models.CASCADE,
        blank=True
    )
    actor_object_id = models.PositiveIntegerField()
    actor = GenericForeignKey('actor_content_type', 'actor_object_id')

    # Object on action
    object_content_type = models.ForeignKey(
        ContentType,
        related_name='notification_object',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    object_object_id = models.PositiveIntegerField(blank=True, null=True)
    object = GenericForeignKey('object_content_type', 'object_object_id')

    # Target
    target_content_type = models.ForeignKey(ContentType,
        related_name='notification_target',
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    target_object_id = models.PositiveIntegerField(blank=True, null=True)
    target = GenericForeignKey('target_content_type', 'target_object_id')

    # Recipient
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='notifications', on_delete=models.CASCADE)

    # Notification
    unread = models.BooleanField(default=True, db_index=True)
    deleted = models.BooleanField(default=False, db_index=True)
    datetime = models.DateTimeField(auto_now_add=True, db_index=True)


    class Meta:
        ordering = ['-datetime']
        index_together = ['recipient', 'unread']

    def timesince(self):
        from django.utils.timesince import timesince as django_timesince
        return django_timesince(self.datetime)

    def __str__(self):
        if self.target and self.object:
            return f'{self.actor} {self.verb} {self.object} {self.target} {self.timesince()} ago'
        if self.target:
            return f'{self.actor} {self.verb} {self.target} {self.timesince()} ago'
        if self.object:
            return f'{self.actor} {self.verb} {self.object} {self.timesince()} ago'
        return f'{self.actor} {self.verb} {self.timesince()} ago'

    def send_notification(self, data):
        # Django Channels
        from channels.layers import get_channel_layer
        from asgiref.sync import async_to_sync

        current_user = self.recipient.pk
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            str(current_user),
            {
                "type": "notification_sender",
                "payload": data,
            },
        )
