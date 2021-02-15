"""Notification signals."""

# Django
from django.dispatch import Signal
from django.db.models.query import QuerySet
from django.contrib.contenttypes.models import ContentType

# Models
from bookshare.notifications.models import Notification

# Serializers
from bookshare.notifications.serializers import NotificationSerializer

# Utils
from datetime import datetime

notify = Signal()

def notify_handler(verb, **kwargs):
    recipient = kwargs['recipient']
    actor = kwargs['sender']
    object = kwargs.get('object', None)
    level = kwargs.get('level')

    notifications = []

    notification = Notification(
        recipient=recipient,
        object=object,
        actor_content_type=ContentType.objects.get_for_model(actor),
        actor_object_id=actor.pk,
        level=level,
        verb=verb
    )
    notification.save()
    serialized = NotificationSerializer(notification)
    notification.send_notification(serialized.data)
    notifications.append(notification)

    return notifications

notify.connect(notify_handler, dispatch_uid='bookshare.notifications.models.notification')
