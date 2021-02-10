"""Lends urls."""

# REST Framework
from rest_framework.routers import DefaultRouter

# Django
from django.urls import path, include

# Views
from bookshare.lends.views import lends
from bookshare.lends.views import books

router = DefaultRouter()
router.register(
    r'circles/(?P<slug_name>[a-zA-Z0-9_-]+)/lends',
    lends.LendViewSet,
    basename='lends'
)
router.register(
    r'books',
    books.BookViewSet,
    basename='books'
)

urlpatterns = [
    path('', include(router.urls))
]
