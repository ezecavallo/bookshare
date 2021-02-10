"""Invitations models."""

# Django
from django.db import models

# Utils
from bookshare.utils.models import BookShareModel

# Manager
from bookshare.circles.managers  import InvitationManager

class Invitation(BookShareModel):
    """Invitation model."""

    issued_by = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='issued_by'
    )
    circle = models.ForeignKey('circles.Circle', on_delete=models.CASCADE)

    code = models.CharField(max_length=128)

    used_by = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        related_name='used_by',
        null=True
    )
    used = models.BooleanField(default=False)

    used_at = models.DateTimeField(blank=True, null=True)

    objects = InvitationManager()

    def __str__(self):
        return f'#{self.circle.slugname} by {self.issued_by}: {self.code}'
