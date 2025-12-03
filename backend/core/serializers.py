# -*- coding: utf-8 -*-
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from .models.taxonomia import Genero
from .models.pessoa import Pessoa
from .models.filme import Filme
from .models.review import Review
from .models.listas import Watchlist, Favorito

User = get_user_model()

class GeneroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genero
        fields = ["id", "nome", "slug"]

class PessoaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pessoa
        fields = ["id", "nome", "slug", "bio", "foto"]

class FilmeListSerializer(serializers.ModelSerializer):
    generos = GeneroSerializer(many=True, read_only=True)
    class Meta:
        model = Filme
        fields = [
            "id", "titulo", "slug", "ano_lancamento",
            "media_rating", "poster", "backdrop", "generos"
        ]

class FilmeDetailSerializer(FilmeListSerializer):
    class Meta(FilmeListSerializer.Meta):
        fields = FilmeListSerializer.Meta.fields + [
            "descricao", "imdb_id", "created_at", "updated_at"
        ]

class FilmeWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Filme
        fields = '__all__'

class UserMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username"]

class ReviewSerializer(serializers.ModelSerializer):
    autor = UserMiniSerializer(read_only=True)
    
    class Meta:
        model = Review
        # CORREÇÃO: Adicionado o campo 'spoiler'
        fields = ["id", "autor", "titulo", "texto", "rating", "spoiler", "created_at", "updated_at"]
        read_only_fields = ["autor", "created_at", "updated_at"]

class WatchlistSerializer(serializers.ModelSerializer):
    utilizador = UserMiniSerializer(read_only=True)
    filme_id = serializers.PrimaryKeyRelatedField(source="filme", queryset=Filme.objects.all(), write_only=True)
    filme_titulo = serializers.CharField(source="filme.titulo", read_only=True)
    class Meta:
        model = Watchlist
        fields = ["id", "utilizador", "filme_id", "filme_titulo", "created_at"]
        read_only_fields = ["utilizador", "created_at"]

class FavoritoSerializer(WatchlistSerializer):
    class Meta(WatchlistSerializer.Meta):
        model = Favorito

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'password2')
        extra_kwargs = {
            'email': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Passwords não coincidem."})
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "is_staff"]
