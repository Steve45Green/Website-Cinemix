# -*- coding: utf-8 -*-
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

# Importar as views de autenticação diretamente
from backend.core.views import UserRegistrationView, UserMeView

urlpatterns = [
    path("admin/", admin.site.urls),

    # --- Rotas de Autenticação ---
    path("api/auth/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/auth/register/", UserRegistrationView.as_view(), name="register"),
    path("api/auth/me/", UserMeView.as_view(), name="me"),

    # --- Rotas da Aplicação Principal ('core') ---
    path("api/", include("backend.core.urls")),

    # --- Rotas de Documentação da API ---
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/schema/swagger/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
