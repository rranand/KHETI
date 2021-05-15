from django.contrib import admin
from django.urls import path, include
from agriculture import urls
from django.conf.urls.static import static
from django.conf import settings
from app import urls as appUrls


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(urls)),
    path('dash', include(appUrls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
