"""Books views."""

# REST Framework
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

# Serializers
from bookshare.lends.serializers import BookModelSerializer

# Models
from bookshare.lends.models import Book

# Permissions
from bookshare.lends.permissions import IsOwnerBook

class BookViewSet(viewsets.ModelViewSet):
    """
    Book model view set.
    Books works independently of circles and are attached to eh users.
    Owner can use the book in a book through lends.
    """

    serializer_class = BookModelSerializer

    def get_queryset(self):
        queryset = Book.objects.filter(owner=self.request.user)

        return queryset

    def get_permissions(self):
        """"Get permissions by actions."""

        permissions = [IsAuthenticated]
        if self.action not in ['create', 'list']:
            permissions.append(IsOwnerBook)

        return [p() for p in permissions]
