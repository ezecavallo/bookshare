"""Utils models."""

# Django
from django.db import models


class BookShareModel(models.Model):
    """BookShare base model.

    BookShareModel acts as an abstract base class from where every other model
    in the project will inherit. This class provides the following atributes:
        + created (DateTime): Store the datetime when the object was created.
        + modified (DateTime): Store the last time the object was modified.
    """

    created = models.DateTimeField(
        'created_at',
        auto_now_add=True,
        help_text='Datetime on when the object was created.'
    )

    modified = models.DateTimeField(
        'modified_at',
        auto_now=True,
        help_text='Datetime on when the object was modified.'
    )

    class Meta():
        """Meta class"""

        abstract = True

        get_latest_by = 'created'
        ordering = ['-created', '-modified']
