"""Circles serializers."""

# REST Framework
from rest_framework import serializers

# Models
from bookshare.circles.models import Circle

class CircleModelSerializer(serializers.ModelSerializer):


    class Meta:

        model = Circle
        fields = [
            'name',
            'about',
            'slug_name',
            'picture',
            'is_verified',
            'is_public',
            'members_limit',
            'lends_offered',
            'lends_taked'
        ]
        read_only_fields = ['lends_offered', 'lends_taked', 'is_verified']
