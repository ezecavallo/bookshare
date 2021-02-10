"""Lend views."""

# REST Framework
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

# Django
from django.shortcuts import get_object_or_404

# Serializers
from bookshare.lends.serializers import (
    LendModelSerializer,
    EndLendSerializer,
    TakeLendSerializer,
    CreateLendSerializer,
)

# Permissions
from bookshare.lends.permissions import IsTakedUser, IsOwnerBook
from bookshare.circles.permissions import IsActiveMember
from rest_framework.permissions import IsAuthenticated

# Models
from bookshare.circles.models import Circle
from bookshare.lends.models import Lend


class LendViewSet(viewsets.ModelViewSet):

    lookup_field = 'pk'

    def dispatch(self, request, *args, **kwargs):

        slug_name = kwargs['slug_name']
        self.circle = get_object_or_404(Circle, slug_name=slug_name)
        return super(LendViewSet, self).dispatch(request, *args, **kwargs)

    def get_serializer_class(self):

        if self.action == 'create':
            return CreateLendSerializer
        if self.action == 'take':
            return TakeLendSerializer
        if self.action == 'finish':
            return EndLendSerializer

        return LendModelSerializer

    def get_permission(self):
        permissions = [IsActiveMember, IsAuthenticated]
        if self.action == 'finish':
            permissions.append(IsTakedUser)
        if self.action in ['update', 'partial_update']:
            permissions.append(IsOwnerBook)

        return [p() for p in permissions]

    def get_queryset(self):

        if self.action in ['finish', 'retrieve']:
            return self.circle.lend_set.filter(
                circle=self.circle,
                taked=True
            )
        if self.action == 'join':
            return self.circle.lend_set.filter(
                circle=self.circle,
                taked=False
            )
        if self.action == 'retrieve':
            return self.circle.lend_set.filter(
                circle=self.circle
            )

        return self.circle.lend_set.all()

    def get_object(self):
        """Get object lend by pk."""

        obj = get_object_or_404(Lend, pk=self.kwargs['pk'])
        return obj

    def get_serializer_context(self):
        """Return circle in the context."""

        return {
            'request': self.request,
            'circle': self.circle
        }


    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(
            data=request.data,
            context=self.get_serializer_context()
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(methods=['POST'], url_path='return', detail=False)
    def finish(self, request, *args, **kwargs):

        lend = self.get_object()
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(
            lend,
            data={
                'returned': True
            },
            context={
                'circle': self.circle,
                'lend':lend
            },
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        lend = serializer.save()
        data = LendModelSerializer(lend).data

        return Response(data, status=status.HTTP_200_OK)

    @action(methods=['POST'], detail=False)
    def take(self, request, *args, **kwargs):

        lend = self.get_object()
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(
            lend,
            data={
                'taked_by': request.user
            },
            context={
                'circle': self.circle,
                'lend':lend
            },
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        lend = serializer.save()
        data = LendModelSerializer(lend).data

        return Response(data, status=status.HTTP_200_OK)
