"""Users urls."""

# Django
from django.urls import path, include


# REST Framework
from rest_framework.routers import DefaultRouter

# REST Framwork JWT
from rest_framework_jwt.views import refresh_jwt_token, verify_jwt_token

# Views
from bookshare.users.views import users

router = DefaultRouter()
router.register(r'users', users.UserViewSet, basename='user')
urlpatterns = [
    path('', include(router.urls)),
    path('users/api-token-refresh/', refresh_jwt_token),
    path('users/api-token-verify/', verify_jwt_token),
]
