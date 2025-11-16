from __future__ import annotations
from typing import List
from django.contrib.auth import get_user_model
from rest_framework import serializers
# Imports dos modelos
from .models.taxonomia import Genero, Etiqueta, Pais, Lingua, Categoria
from .models.pessoa import Pessoa
from .models.filme import Filme
from .models.elenco import Elenco
from .models.video import Video
from .models.review import Review
from .models.listas import Watchlist, Favorito

User = get_user_model()


# -----------------------------
# Taxonomias (read-only)
# -----------------------------
class GeneroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genero
        fields = ["id", "nome", "slug"]


class EtiquetaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Etiqueta
        fields = ["id", "nome", "slug"]


class PaisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pais
        fields = ["id", "nome", "iso2"]


class LinguaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lingua
        fields = ["id", "nome", "codigo"]


class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ["id", "nome", "slug"]


class PessoaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pessoa
        fields = ["id", "nome", "slug", "bio", "foto"]  # Removido 'data_nascimento' se não existir


# -----------------------------
# Elenco / Vídeos (nested)
# -----------------------------
class ElencoSerializer(serializers.ModelSerializer):
    pessoa = PessoaSerializer(read_only=True)

    class Meta:
        model = Elenco
        fields = ["pessoa", "papel", "ordem_credito"]


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ["titulo", "tipo", "site", "key", "url", "idioma"]


# -----------------------------
# Filmes (API List e Detail)
# -----------------------------
class FilmeListSerializer(serializers.ModelSerializer):
    generos = GeneroSerializer(many=True, read_only=True)
    categoria = serializers.CharField(source="categoria.nome", read_only=True)

    class Meta:
        model = Filme
        fields = [
            "id", "titulo", "slug", "ano_lancamento",
            "popularidade", "media_rating",
            "poster", "backdrop",
            "generos", "categoria"
        ]


class FilmeDetailSerializer(FilmeListSerializer):
    etiquetas = EtiquetaSerializer(many=True, read_only=True)
    paises = PaisSerializer(many=True, read_only=True)
    linguas = LinguaSerializer(many=True, read_only=True)
    realizador = PessoaSerializer(read_only=True)

    trailer_key = serializers.SerializerMethodField()
    creditos = ElencoSerializer(many=True, read_only=True)
    videos = VideoSerializer(many=True, read_only=True)

    def get_trailer_key(self, obj: Filme) -> str | None:
        trailer = obj.videos.filter(tipo="trailer").order_by("-created_at").first()
        return trailer.key if trailer else None

    class Meta(FilmeListSerializer.Meta):
        fields = FilmeListSerializer.Meta.fields + [
            "descricao", "etiquetas", "paises", "linguas", "realizador",
            "trailer_key", "creditos", "videos",
            "created_at", "updated_at"
        ]


# -----------------------------
# Filmes (API Write/Update)
# -----------------------------
class FilmeWriteSerializer(serializers.ModelSerializer):
    generos_ids = serializers.ListField(write_only=True, required=False, child=serializers.IntegerField())
    etiquetas_ids = serializers.ListField(write_only=True, required=False, child=serializers.IntegerField())
    paises_ids = serializers.ListField(write_only=True, required=False, child=serializers.IntegerField())
    linguas_ids = serializers.ListField(write_only=True, required=False, child=serializers.IntegerField())
    categoria_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    realizador_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)

    class Meta:
        model = Filme
        fields = [
            "id", "titulo", "slug", "descricao", "ano_lancamento",
            "popularidade", "media_rating",
            "poster", "backdrop",
            "generos_ids", "etiquetas_ids", "paises_ids", "linguas_ids",
            "categoria_id", "realizador_id",
        ]
        read_only_fields = ["popularidade", "media_rating"]

    def _set_relations(self, filme: Filme, ids: dict):
        if "generos_ids" in ids:
            filme.generos.set(ids["generos_ids"])
        if "etiquetas_ids" in ids:
            filme.etiquetas.set(ids["etiquetas_ids"])
        if "paises_ids" in ids:
            filme.paises.set(ids["paises_ids"])
        if "linguas_ids" in ids:
            filme.linguas.set(ids["linguas_ids"])

    def create(self, validated_data):
        relational_ids = {
            k: validated_data.pop(k)
            for k in list(validated_data.keys())
            if k.endswith("_ids") or k.endswith("_id")
        }
        filme = Filme.objects.create(**validated_data)
        self._set_relations(filme, relational_ids)
        return filme

    def update(self, instance, validated_data):
        relational_ids = {
            k: validated_data.pop(k)
            for k in list(validated_data.keys())
            if k.endswith("_ids") or k.endswith("_id")
        }
        filme = super().update(instance, validated_data)
        self._set_relations(filme, relational_ids)
        return filme


# -----------------------------
# Interações de utilizador
# -----------------------------
class UserMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username"]


class ReviewSerializer(serializers.ModelSerializer):
    autor = UserMiniSerializer(read_only=True)
    filme_id = serializers.PrimaryKeyRelatedField(source="filme", queryset=Filme.objects.all(), write_only=True)
    filme_titulo = serializers.CharField(source="filme.titulo", read_only=True)

    class Meta:
        model = Review
        fields = [
            "id", "filme", "filme_id", "filme_titulo", "autor", "titulo", "texto", "rating",
            "created_at", "updated_at"
        ]
        read_only_fields = ["autor", "created_at", "updated_at"]
        extra_kwargs = {"filme": {"read_only": True}}


class WatchlistSerializer(serializers.ModelSerializer):
    utilizador = UserMiniSerializer(read_only=True)
    filme_id = serializers.PrimaryKeyRelatedField(source="filme", queryset=Filme.objects.all(), write_only=True)
    filme_titulo = serializers.CharField(source="filme.titulo", read_only=True)

    class Meta:
        model = Watchlist
        fields = ["id", "utilizador", "filme", "filme_id", "filme_titulo", "created_at"]
        read_only_fields = ["utilizador", "created_at"]
        extra_kwargs = {"filme": {"read_only": True}}


class FavoritoSerializer(WatchlistSerializer):
    class Meta:
        model = Favorito
        fields = WatchlistSerializer.Meta.fields
        read_only_fields = ["utilizador", "created_at"]
        extra_kwargs = {"filme": {"read_only": True}}


# =================================
#    AUTENTICAÇÃO (NOVOS)
# =================================
class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer para registo de novos utilizadores."""
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "email", "password"]
        extra_kwargs = {
            "email": {"required": True},
        }

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
        )
        return user


class UserSerializer(serializers.ModelSerializer):
    """Serializer seguro para retornar dados do utilizador autenticado."""

    class Meta:
        model = User
        fields = ["id", "username", "email", "is_staff"]
