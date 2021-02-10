"""JWT Token serializers."""

# REST Framework JWT
from rest_framework_jwt.serializers import JSONWebTokenSerializer
from rest_framework_jwt.settings import api_settings
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

# Django
from django.contrib.auth import authenticate

# REST Framwork
from rest_framework import serializers

class CustomJSONWebTokenSerializer(JSONWebTokenSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(
        min_length=8,
        max_length=256,
        style={'input_type': 'password'},
    )

    def validate(self, attrs):
        super(JSONWebTokenSerializer, self).validate(attrs)

        user = authenticate(email=attrs['email'], password=attrs['password'])
        if not user:
            raise serializers.ValidationError('Invalid credentials.')
        if user.is_verified != True:
            raise serializers.ValidationError('Account is not verified yet.')

        payload = jwt_payload_handler(user)

        return {
            'token': jwt_encode_handler(payload),
            'user': user
        }
