import os
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('shop/', include('shop.urls', namespace='shop')),
    path('', include('conference.urls', namespace='conference')),
    path('portal/', include('portal.urls', namespace='portal')),
]

# Serve media files in development or when not using cloud storage
if settings.DEBUG or not os.environ.get("CLOUDINARY_URL"):
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
