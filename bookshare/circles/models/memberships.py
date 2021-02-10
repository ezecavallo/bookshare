"""Memberships models."""

# Django
from django.db import models

# Utils
from bookshare.utils import BookShareModel


class Membership(BookShareModel):
    """
    Membership model.
    This table holds the realationship between users and circles.
    """

    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    circle = models.ForeignKey('circles.Circle', on_delete=models.CASCADE)

    remaning_invitations = models.PositiveSmallIntegerField(default=0)
    invited_by = models.ForeignKey(
        'users.User',
        null=True,
        on_delete=models.SET_NULL,
        related_name='invited_by'
    )
    is_admin = models.BooleanField(
        'circle admin',
        default=False,
    )

    # Stats
    lends_offered = models.PositiveIntegerField(default=0)
    lends_taked = models.PositiveIntegerField(default=0)

    is_active = models.BooleanField(
        'active status',
        default=True,
        help_text='Only active users are allowed.'
    )

    def __str__(self):
        """Return the relationship."""
        return f'{self.user.username} in {self.circle.name}'
