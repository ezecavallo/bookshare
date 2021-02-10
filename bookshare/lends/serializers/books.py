"""Books serializers."""

# REST Framework
from rest_framework import serializers

# Models
from bookshare.lends.models import Book

class BookModelSerializer(serializers.ModelSerializer):
    """Book serializer."""

    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Book
        fields = [
            'title',
            'author',
            'cover',
            'isbn',
            'owner'
        ]
