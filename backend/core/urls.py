# backend/core/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    GeneroViewSet, EtiquetaViewSet, PaisViewSet, LinguaViewSet,
    PessoaViewSet,
    FilmeViewSet, ElencoViewSet, VideoViewSet,
    ReviewViewSet, WatchlistViewSet, FavoritoViewSet,
)

app_name = "core"

# O router regista todos os ViewSets da tua app
router = DefaultRouter()
router.register(r"generos", GeneroViewSet, basename="genero")
router.register(r"etiquetas", EtiquetaViewSet, basename="etiqueta")
router.register(r"paises", PaisViewSet, basename="pais")
router.register(r"linguas", LinguaViewSet, basename="lingua")
# Nota: CategoriaViewSet não foi incluída porque não a criaste em views.py

router.register(r"pessoas", PessoaViewSet, basename="pessoa")
router.register(r"filmes", FilmeViewSet, basename="filme")
router.register(r"elenco", ElencoViewSet, basename="elenco")
router.register(r"videos", VideoViewSet, basename="video")

router.register(r"reviews", ReviewViewSet, basename="review")
router.register(r"watchlist", WatchlistViewSet, basename="watchlist")
router.register(r"favoritos", FavoritoViewSet, basename="favorito")


urlpatterns = [
    # Todas as rotas registadas no router (ex: /api/filmes/, /api/generos/)
    path("", include(router.urls)),
]
