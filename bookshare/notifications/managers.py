"""Notifications managers."""

# Django
from django.db import models


class NotificationQuerySet(models.QuerySet):
    """Custom QuerySet methods for Notification model."""

    def all_
