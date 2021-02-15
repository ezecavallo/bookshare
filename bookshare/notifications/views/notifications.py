"""Notifications views."""

#  REST Framework
from rest_framework import generics

# Permissions
from rest_framework.permissions import IsAuthenticated

# Models
from bookshare.notifications.models import Notification

# Serializers
from bookshare.notifications.serializers import NotificationSerializer

# Django
from django.http import request
from django.shortcuts import render
from django.http import HttpResponse

# Django Channels
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

class NotificationView(generics.ListAPIView):
    """Notification api view."""

    def get_queryset(self):

        queryset = Notification.objects.filter(
            recipient=self.request.user
        )
        return queryset

    serializer_class = NotificationSerializer
    permission_classes  = [IsAuthenticated]

def home(request):
    return render(request, 'home.html')

def notification_test(request):
    from bookshare.notifications.signals import notify
    notify.send(request.user, recipient=request.user, verb='you reached level 10', level='IN')
    return HttpResponse('Send it!')
