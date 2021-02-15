"""Notifications urls."""

# REST Framework
from rest_framework.routers import DefaultRouter

# Django
from django.urls import path, include

# Views

from bookshare.notifications.views import NotificationView, notification_test, home

# router = DefaultRouter()
# router.register(r'notifications', NotificationView.as_view(), basename='notifications')

urlpatterns = [
    path('notifications/', NotificationView.as_view(), name='notification-list'),
    path('notifications/home', home, name='notifications'),
    path('notifications/test', notification_test, name='notifications_test'),
]
