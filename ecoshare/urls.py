"""
EcoShare Tashkent — root URL conf.
"""

from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from django.views.decorators.csrf import csrf_exempt
from django.views.i18n import set_language

urlpatterns = [
    path("admin/", admin.site.urls),
    path("i18n/setlang/", csrf_exempt(set_language), name="set_language"),
    path("", include("items.urls")),
    path("accounts/", include("accounts.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.BASE_DIR / "static")