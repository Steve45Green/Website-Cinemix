from __future__ import annotations

from typing import TYPE_CHECKING, cast
from django.db.models import Q
from rest_framework import viewsets, mixins, permissions, filters
# from rest_framework.decorators import action
# from rest_framework.response import Response
from rest_framework.request import Request
from .models.taxonomia import Genero, Etiqueta, Pais, Lingua, Categoria
from .models.pessoa import Pessoa, Realizador, Ator
from .models.filme import Filme
from .models.elenco import Elenco
from .models.video import Video
from .models.review import Review
from .models.listas import Watchlist, Favorito


from .serializers import (
    GeneroSerializer, EtiquetaSerializer, PaisSerializer, LinguaSerializer, PessoaSerializer,
    FilmeListSerializer, FilmeDetailSerializer, ElencoSerializer, VideoSerializer,
    ReviewSerializer, WatchlistSerializer, FavoritoSerializer
)
from .permissions import IsOwnerOrReadOnly

# -----------------------------
# ReadOnly básicos
# -----------------------------
class GeneroViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Genero.objects.all()
    serializer_class = GeneroSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["nome"]
    ordering_fields = ["nome"]

class EtiquetaViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Etiqueta.objects.all()
    serializer_class = EtiquetaSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["nome"]
    ordering_fields = ["nome"]

class PaisViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Pais.objects.all()
    serializer_class = PaisSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["nome", "iso2"]
    ordering_fields = ["nome", "iso2"]

class LinguaViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Lingua.objects.all()
    serializer_class = LinguaSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["nome", "codigo"]
    ordering_fields = ["nome", "codigo"]

class PessoaViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Pessoa.objects.all()
    serializer_class = PessoaSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["nome", "slug", "bio"]
    ordering_fields = ["nome", "created_at"]

# -----------------------------
# Filmes
# -----------------------------
class FilmeViewSet(viewsets.ModelViewSet):
    queryset = (
        Filme.objects.all()
        .select_related()  # seleciona FKs; ok sem args
        .prefetch_related("generos", "etiquetas", "paises", "linguas", "videos", "creditos__pessoa")
    )
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["titulo", "descricao", "slug"]
    ordering_fields = ["popularidade", "media_rating", "ano_lancamento", "titulo"]
    ordering = ["-popularidade", "-media_rating"]

    def get_serializer_class(self):
        if self.action in ["list"]:
            return FilmeListSerializer
        return FilmeDetailSerializer

    def get_queryset(self):
        qs = super().get_queryset()

        request = cast(Request, self.request)
        genero = request.query_params.get("genero")
        ano = request.query_params.get("ano")
        q = request.query_params.get("q")

        if genero:
            qs = qs.filter(Q(generos__slug=genero) | Q(generos__nome__iexact=genero))
        if ano:
            qs = qs.filter(ano_lancamento=ano)
        if q:
            qs = qs.filter(Q(titulo__icontains=q) | Q(descricao__icontains=q))

        return qs.distinct()

# -----------------------------
# Elenco e Vídeos
# -----------------------------
class ElencoViewSet(viewsets.ModelViewSet):
    queryset = Elenco.objects.select_related("filme", "pessoa").all()
    serializer_class = ElencoSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["ordem_credito"]


class VideoViewSet(viewsets.ModelViewSet):
    queryset = Video.objects.select_related("filme").all()
    serializer_class = VideoSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["created_at"]

# -----------------------------
# Reviews (1 por utilizador por filme)
# -----------------------------
class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.select_related("filme", "autor").all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["created_at", "rating"]
    ordering = ["-created_at"]

    def perform_create(self, serializer):
        # Enforce unique (filme, autor): se existir, atualiza; senão, cria
        request = cast(Request, self.request)
        filme = serializer.validated_data["filme"]
        autor = request.user
        obj, created = Review.objects.update_or_create(
            filme=filme,
            autor=autor,
            defaults={
                "titulo": serializer.validated_data.get("titulo", ""),
                "texto": serializer.validated_data.get("texto", ""),
                "rating": serializer.validated_data["rating"],
            },
        )
        serializer.instance = obj  # devolve a instância criada/atualizada

    def get_queryset(self):
        qs = super().get_queryset()
        request = cast(Request, self.request)
        filme_id = request.query_params.get("filme")
        user_only = request.query_params.get("mine")
        if filme_id:
            qs = qs.filter(filme_id=filme_id)
        if user_only and user_only.lower() in {"1", "true", "yes"} and request.user.is_authenticated:
            qs = qs.filter(autor=request.user)
        return qs

# -----------------------------
# Watchlist & Favoritos (scoped ao utilizador)
# -----------------------------
if TYPE_CHECKING:
    from rest_framework.request import Request as DRFRequest

class _UserOwnedMixin:
    # Ajuda o linter a saber que existe self.request
    request: "DRFRequest"

    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.user.is_authenticated:
            return qs.filter(utilizador=self.request.user)
        return qs.none()

    def perform_create(self, serializer):
        serializer.save(utilizador=self.request.user)

class WatchlistViewSet(
    _UserOwnedMixin,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Watchlist.objects.select_related("utilizador", "filme").all()
    serializer_class = WatchlistSerializer
    permission_classes = [permissions.IsAuthenticated]


class FavoritoViewSet(
    _UserOwnedMixin,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Favorito.objects.select_related("utilizador", "filme").all()
    serializer_class = FavoritoSerializer
    permission_classes = [permissions.IsAuthenticated]
