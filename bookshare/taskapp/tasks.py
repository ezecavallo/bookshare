"""Celery tasks."""

# Django
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings

# Celery
from celery.decorators import task

# Models
from bookshare.users.models import User

# Utilities
import jwt
from datetime import timedelta
from django.utils import timezone

def gen_verification_token(user):

    exp_date = timezone.now() + timedelta(days=3)
    payload = {
        'user': user.username,
        'exp': int(exp_date.timestamp()),
        'type': 'email_confirmation'
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
    return token.decode()

@task(name='send_confirmation_email', max_retries=3)
def send_confirmation_email(user_pk):

    user = User.objects.get(pk=user_pk)
    verification_token = gen_verification_token(user)

    subject = f'Welcome @{user}! First we need your verify account to start.'
    from_email = 'Ezequiel Cavallo <ezecavallo@gmail.com>'
    content = render_to_string(
        'emails/users/verification.html',
        {'token': verification_token, 'user': user}
    )

    message = EmailMultiAlternatives(subject, content, from_email, [user.email])
    message.attach_alternative(content, "text/html")
    message.send()
