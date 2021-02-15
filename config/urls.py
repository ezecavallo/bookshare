"""Main URLs module."""

# Django
from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static
from django.contrib import admin

urlpatterns = [
    # Django Admin
    path(settings.ADMIN_URL, admin.site.urls),

    # bookshare urls
    path('', include(('bookshare.users.urls', 'users'), namespace='user')),
    path('', include(('bookshare.circles.urls', 'circles'), namespace='circle')),
    path('', include(('bookshare.lends.urls', 'lends'), namespace='lend')),
    path('', include(('bookshare.notifications.urls', 'notifications'), namespace='notification')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
