from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.http import JsonResponse
from django.urls import include, path

from data_doctor.views import dashboard


def health_check(request):
    return JsonResponse({"status": "ok", "service": "ai-data-doctor"})


def api_root(request):
    return JsonResponse({
        "name": "AI Data Doctor API",
        "status": "online",
        "version": "1.0",
        "health": "/health/",
        "api": "/api/",
        "admin": "/admin/",
    })


urlpatterns = [
    path("admin/", admin.site.urls),
    path("health/", health_check, name="health"),
    path("api-status/", api_root, name="api-status"),
    path("", dashboard, name="dashboard"),
    path("api/", include("data_doctor.urls")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
