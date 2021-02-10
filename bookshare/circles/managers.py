"""Circles Managers."""

#  Django
from django.db import models

# Utils
from string import ascii_uppercase, digits
import random


class InvitationManager(models.Manager):

    def create(self, **kwargs):
        length = 15
        code = ''.join(random.choices(ascii_uppercase + digits, k=length))
        while self.filter(code=code).exists():
            code = ''.join(random.choices(ascii_uppercase + digits, k=length))
        kwargs['code'] = code
        return super(InvitationManager, self).create(**kwargs)
