"""Notifications routings."""

from django.urls import re_path

from bookshare.notifications.consumers import NotificationConsumer

websocket_urlpatterns = [
    re_path(r'notifications/', NotificationConsumer.as_asgi()),
    # re_path(r'ws/notifications/(?P<username>\w+)/$', NotificationConsumer.as_asgi()),
]
