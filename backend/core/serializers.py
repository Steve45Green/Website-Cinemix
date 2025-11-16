from __future__ import annotations
from typing import List
from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models.taxonomia import Genero, Etiqueta, Pais, Lingua, Categoria
from .models.pessoa import Pessoa, Realizador, Ator
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
class PessoaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pessoa
        fields = ["id", "nome", "slug", "bio", "data_nascimento", "foto_url"]
# -----------------------------
# Elenco / Vídeo
# -----------------------------
class ElencoSerializer(serializers.ModelSerializer):
    pessoa = PessoaSerializer(read_only=True)
    pessoa_id = serializers.PrimaryKeyRelatedField(
        queryset=Pessoa.objects.all(), write_only=True, source="pessoa"
    )
    class Meta:
        model = Elenco
        fields = [
            "id", "filme", "pessoa", "pessoa_id", "papel", "personagem", "ordem_credito",
            "created_at", "updated_at"
        ]
        read_only_fields = ["filme", "created_at", "updated_at"]

class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = [
            "id", "filme", "tipo", "titulo", "url",
            "site", # <--- CORREÇÃO (antes era "fonte")
            "idioma",
            "created_at", "updated_at"
        ]
        read_only_fields = ["created_at", "updated_at"]
# -----------------------------
# Filmes (lista/detalhe)
# -----------------------------
class FilmeListSerializer(serializers.ModelSerializer):
    generos = GeneroSerializer(many=True, read_only=True)
    media_rating = serializers.FloatField(read_only=True)

    class Meta:
        model = Filme
        fields = [
            "id", "titulo", "slug", "ano_lancamento", "poster_url",
            "media_rating", "popularidade", "generos", "updated_at"
        ]

class FilmeDetailSerializer(serializers.ModelSerializer):
    # Nested read-only
    generos = GeneroSerializer(many=True, read_only=True)
    etiquetas = EtiquetaSerializer(many=True, read_only=True)
    paises = PaisSerializer(many=True, read_only=True)
    linguas = LinguaSerializer(many=True, read_only=True)
    videos = VideoSerializer(many=True, read_only=True)
    creditos = ElencoSerializer(many=True, read_only=True)

    # IDs write-only para M2M (frontend envia listas de IDs)
    generos_ids: List[int] = serializers.ListField(
        child=serializers.IntegerField(), write_only=True, required=False
    )
    etiquetas_ids: List[int] = serializers.ListField(
        child=serializers.IntegerField(), write_only=True, required=False
    )
    paises_ids: List[int] = serializers.ListField(
        child=serializers.IntegerField(), write_only=True, required=False
    )
    linguas_ids: List[int] = serializers.ListField(
        child=serializers.IntegerField(), write_only=True, required=False
    )

    class Meta:
        model = Filme
        fields = [
            "id", "titulo", "slug", "descricao", "ano_lancamento", "duracao_min",
            "classificacao", "poster_url", "trailer_url",
            "popularidade", "media_rating", "total_reviews",

            # nested read-only
            "generos", "etiquetas", "paises", "linguas", "videos", "creditos",

            # ids write-only
            "generos_ids", "etiquetas_ids", "paises_ids", "linguas_ids",

            "created_at", "updated_at"
        ]
        read_only_fields = ["slug", "media_rating", "total_reviews", "created_at", "updated_at"]

    def _set_m2m(self, filme: Filme, data: dict):
        if "generos_ids" in data:
            filme.generos.set(Genero.objects.filter(id__in=data["generos_ids"]))
        if "etiquetas_ids" in data:
            filme.etiquetas.set(Etiqueta.objects.filter(id__in=data["etiquetas_ids"]))
        if "paises_ids" in data:
            filme.paises.set(Pais.objects.filter(id__in=data["paises_ids"]))
        if "linguas_ids" in data:
            filme.linguas.set(Lingua.objects.filter(id__in=data["linguas_ids"]))

    def create(self, validated_data):
        ids = {
            k: validated_data.pop(k)
            for k in list(validated_data.keys())
            if k.endswith("_ids")
        }
        filme = super().create(validated_data)
        self._set_m2m(filme, ids)
        return filme

    def update(self, instance, validated_data):
        ids = {
            k: validated_data.pop(k)
            for k in list(validated_data.keys())
            if k.endswith("_ids")
        }
        filme = super().update(instance, validated_data)
        self._set_m2m(filme, ids)
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

    class Meta:
        model = Review
        fields = [
            "id", "filme", "autor", "titulo", "texto", "rating",
            "created_at", "updated_at"
        ]
        read_only_fields = ["autor", "created_at", "updated_at"]

class WatchlistSerializer(serializers.ModelSerializer):
    utilizador = UserMiniSerializer(read_only=True)

    class Meta:
        model = Watchlist
        fields = ["id", "utilizador", "filme", "marcado_em"]
        read_only_fields = ["utilizador", "marcado_em"]


class FavoritoSerializer(serializers.ModelSerializer):
    utilizador = UserMiniSerializer(read_only=True)

    class Meta:
        model = Favorito
        fields = ["id", "utilizador", "filme", "marcado_em"]
        read_only_fields = ["utilizador", "marcado_em"]
