"""Circles urls."""

# REST Framework
from rest_framework.routers import DefaultRouter

# Django
from django.urls import path, include

# Views
from bookshare.circles.views import circles as circle_views
from bookshare.circles.views import memberships as membership_views

router = DefaultRouter()
router.register(
    r'circles',
    circle_views.CircleViewSet,
    basename='circles'
)
router.register(
    r'circles/(?P<slug_name>[a-zA-Z0-9_-]+)/members',
    membership_views.MembershipViewSet,
    basename='membership'
)

urlpatterns = [
    path('', include(router.urls))
]
