from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),

    # HTML na raiz
    path("", include("core.urls")),      # 
    # API (mesmo urls por simplicidade)
    path("api/", include("core.urls")),  # <-- idem
]

# Servir MEDIA em desenvolvimento
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

