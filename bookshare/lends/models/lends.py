"""Lends models."""

# Django
from django.db import models

# Utils
from bookshare.utils.models import BookShareModel


class Book(BookShareModel):
    """Book model."""

    title = models.CharField(
        'book title',
        max_length=148
    )
    author = models.CharField(
        'book author',
        max_length=148
    )
    cover = models.ImageField(
        'book cover',
        upload_to='books/cover',
        blank=True,
        null=True
    )
    isbn = models.PositiveBigIntegerField(default=0, blank=True)

    # User related
    owner = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='books'
    )

    def __str__(self):
        return f'{self.title} by {self.author}'

class Lend(BookShareModel):
    """
    Lend model.
    Only one lend per book can be active.
    """

    lended_by = models.ForeignKey(
        'users.User',
        null=True,
        on_delete=models.SET_NULL,
        related_name='lended_by'
    )
    circle = models.ForeignKey(
        'circles.Circle',
        null=True,
        on_delete=models.SET_NULL,
    )
    taked_by = models.ForeignKey(
        'users.User',
        null=True,
        on_delete=models.SET_NULL,
        related_name='taked_by'
    )

    book = models.ForeignKey(
        Book,
        null=True,
        on_delete=models.SET_NULL
    )

    comments = models.TextField(max_length=255, blank=True)
    taked = models.BooleanField(
        'book taked',
        default=False
    )
    returned = models.BooleanField(
        'book returned',
        default=False,
        help_text='If returned is True, the book was returned.'
    )
    returned_at = models.DateTimeField(blank=True, null=True)
