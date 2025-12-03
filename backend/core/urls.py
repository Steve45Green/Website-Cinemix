# backend/core/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    GeneroViewSet,
    FilmeViewSet,
    ReviewViewSet,
    WatchlistViewSet,
    FavoritoViewSet,
)

router = DefaultRouter()
router.register(r'generos', GeneroViewSet, basename='genero')
router.register(r'filmes', FilmeViewSet, basename='filme')
router.register(r'reviews', ReviewViewSet, basename='review')
router.register(r'watchlist', WatchlistViewSet, basename='watchlist')
router.register(r'favoritos', FavoritoViewSet, basename='favorito')

urlpatterns = [
    path('', include(router.urls)),
]
