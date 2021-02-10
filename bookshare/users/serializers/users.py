"""Users serializers."""

# REST Framework
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

# Models
from bookshare.users.models import User, Profile

# Django
from django.contrib.auth import password_validation
from django.db import transaction
from django.core.validators import RegexValidator
from django.conf import settings

# Celery
from bookshare.taskapp.tasks import send_confirmation_email

# Serializers
from .profiles import ProfileModelSerializer

# PyJWT
import jwt


class UserModelSerializer(serializers.ModelSerializer):
    """User model serializer."""

    profile = ProfileModelSerializer(read_only=True)

    class Meta:
        """meta class."""

        model = User
        fields = [
            'username', 'email', 'first_name',
            'last_name', 'phone_number', 'profile'
        ]

class CreateUserSerializer(serializers.Serializer):
    """User signup serializer."""

    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    username = serializers.CharField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    phone_regex = RegexValidator(
        regex=r'\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: +999999999. Up to 15 digits allowed."
    )
    phone_number = serializers.CharField(validators=[phone_regex])

    password = serializers.CharField(
        min_length=8,
        max_length=256,
        style={'input_type': 'password'},
    )
    password_confirmation = serializers.CharField(
        min_length=8,
        max_length=256,
        style={'input_type': 'password'},
    )

    first_name = serializers.CharField(min_length=1, max_length=64)
    last_name = serializers.CharField(min_length=1, max_length=64)

    def validate(self, data):
        """
        Check if the password are the same.
        """
        password = data['password']
        password_confirmation = data['password_confirmation']

        if password != password_confirmation:
            raise serializers.ValidationError('Password does not match.')
        password_validation.validate_password(password)

        return data

    def create(self, data):
        """User and profile creation."""

        data.pop('password_confirmation')
        user = User.objects.create_user(**data, is_verified=False)
        Profile.objects.create(user=user)
        transaction.on_commit(lambda: send_confirmation_email.delay(user_pk=user.pk))
        return user


class VerifyAccountSerializer(serializers.Serializer):
    """Handle the verification of the email."""

    token = serializers.CharField()

    def validate_token(self, data):
        """Verify if token is valid."""

        try:
            payload = jwt.decode(data, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise serializers.ValidationError('Verification link has expired')
        except jwt.PyJWTError:
            raise serializers.ValidationError('Invalid token')

        if payload['type'] != 'email_confirmation':
            raise serializers.ValidationError('Invalid token')

        self.context['payload'] = payload
        return data

    def save(self):
        """Change user to verified account."""

        payload = self.context['payload']
        user = User.objects.get(username=payload['user'])
        user.is_verified = True
        user.save()
