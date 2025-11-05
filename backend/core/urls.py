# backend/core/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter

# Importa os ViewSets definidos em backend/core/views.py
from .views import (
    GeneroViewSet, EtiquetaViewSet, PaisViewSet, LinguaViewSet, CategoriaViewSet,
    PessoaViewSet,  # se tiveres ViewSets específicos para Realizador/Ator, adiciona-os
    FilmeViewSet, ElencoViewSet, VideoViewSet,
    ReviewViewSet, WatchlistViewSet, FavoritoViewSet,
)

app_name = "core"

router = DefaultRouter()
router.register(r"generos", GeneroViewSet, basename="genero")
router.register(r"etiquetas", EtiquetaViewSet, basename="etiqueta")
router.register(r"paises", PaisViewSet, basename="pais")
router.register(r"linguas", LinguaViewSet, basename="lingua")
router.register(r"categorias", CategoriaViewSet, basename="categoria")  # se tiveres CategoriaViewSet

router.register(r"pessoas", PessoaViewSet, basename="pessoa")
# Se existirem estes ViewSets no teu views.py, podes expô-los também:
#from .views import RealizadorViewSet, AtorViewSet
# router.register(r"realizadores", RealizadorViewSet, basename="realizador")
# router.register(r"atores", AtorViewSet, basename="ator")

router.register(r"filmes", FilmeViewSet, basename="filme")
router.register(r"elenco", ElencoViewSet, basename="elenco")
router.register(r"videos", VideoViewSet, basename="video")

router.register(r"reviews", ReviewViewSet, basename="review")
router.register(r"watchlist", WatchlistViewSet, basename="watchlist")
router.register(r"favoritos", FavoritoViewSet, basename="favorito")


urlpatterns = [
    path("", include(router.urls)),
]
# Também poderias usar simplesmente: urlpatterns = router.urls