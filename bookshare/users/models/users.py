"""Users models."""

# Django
from django.db import models
from django.contrib.auth.models import AbstractUser

# Models
from bookshare.utils import BookShareModel


class User(BookShareModel, AbstractUser):
    """
    Custom user model.
    Extends from AbstractUser and change the username field
    to email with extra fields.
    """


    email = models.EmailField(
        'email',
        unique=True,
        help_text={'unique': 'A user with that email already exists.'}
    )

    phone_number = models.CharField(max_length=17, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    is_client = models.BooleanField(
        'client',
        default=True,
        help_text=(
            'Help to distinguish users and perform queries.'
            'Clients are the main type of user.'
        )
    )
    is_verified = models.BooleanField(
        'verified',
        default=False,
        help_text='User must confirmate the email.'
    )

    def __str__(self):
        """Return username."""
        return self.username

    def get_short_name(self):
        """Return username."""
        return self.username
