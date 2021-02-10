"""Circles models."""

# Django
from django.db import models

# Utils
from bookshare.utils import BookShareModel

class Circle(BookShareModel):
    """
    Circle models.
    This model work as a private groups where books lends are
    offer and take between the users. To join into the circle
    must receive an invitation from a member.
    """

    name = models.CharField('circle name', max_length=148)
    slug_name = models.SlugField('circle slug name', unique=True, max_length=148)

    about = models.TextField('circle description', max_length=500)
    picture = models.ImageField(
        'circle picture',
        upload_to='circles/pictures',
        blank=True,
        null=True
    )

    is_verified = models.BooleanField(
        'verified',
        default=False,
        help_text='An oficial organization or community.'
    )
    is_public = models.BooleanField(
        default=True,
        help_text='Public circles are filter in so anyone can know about it.'
    )

    members_limit = models.PositiveIntegerField(
        'members limits',
        default=0,
        help_text='If members limits is 0, the circle has not limit.'
    )
    members = models.ManyToManyField(
        'users.User',
        through='circles.Membership',
        through_fields=('circle', 'user')
    )


    # Stats
    lends_offered = models.PositiveIntegerField(default=0)
    lends_taked = models.PositiveIntegerField(default=0)

    def __str__(self):
        """Return circle name."""
        return self.name

    class Meta:
        ordering = ['-lends_taked', '-lends_offered']
