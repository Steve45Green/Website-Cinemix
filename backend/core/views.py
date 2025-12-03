# -*- coding: utf-8 -*-
from __future__ import annotations
from django.contrib.auth import get_user_model
from rest_framework import viewsets, permissions, generics, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models.taxonomia import Genero
from .models.filme import Filme
from .models.review import Review
from .models.listas import Watchlist, Favorito

from .serializers import (
    GeneroSerializer,
    FilmeListSerializer, FilmeDetailSerializer, FilmeWriteSerializer,
    ReviewSerializer, WatchlistSerializer, FavoritoSerializer,
    UserRegistrationSerializer, UserSerializer,
)

User = get_user_model()

class GeneroViewSet(viewsets.ModelViewSet):
    queryset = Genero.objects.all()
    serializer_class = GeneroSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class FilmeViewSet(viewsets.ModelViewSet):
    queryset = Filme.objects.all().prefetch_related('generos')
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = 'slug'

    def get_serializer_class(self):
        if self.action == 'list':
            return FilmeListSerializer
        if self.action in ['create', 'update', 'partial_update']:
            return FilmeWriteSerializer
        return FilmeDetailSerializer

    @action(detail=True, methods=['get'], permission_classes=[permissions.AllowAny])
    def status(self, request, slug=None):
        user = request.user
        if not user.is_authenticated:
            return Response({'in_watchlist': False, 'is_favorite': False})
        filme = self.get_object()
        data = {
            'in_watchlist': Watchlist.objects.filter(utilizador=user, filme=filme).exists(),
            'is_favorite': Favorito.objects.filter(utilizador=user, filme=filme).exists(),
        }
        return Response(data)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def toggle_watchlist(self, request, slug=None):
        filme = self.get_object()
        user = request.user
        watchlist_entry, created = Watchlist.objects.get_or_create(utilizador=user, filme=filme)
        if not created:
            watchlist_entry.delete()
            return Response({'in_watchlist': False}, status=status.HTTP_200_OK)
        return Response({'in_watchlist': True}, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def toggle_favorite(self, request, slug=None):
        filme = self.get_object()
        user = request.user
        favorite_entry, created = Favorito.objects.get_or_create(utilizador=user, filme=filme)
        if not created:
            favorite_entry.delete()
            return Response({'is_favorite': False}, status=status.HTTP_200_OK)
        return Response({'is_favorite': True}, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['get'], url_path='reviews')
    def list_reviews(self, request, slug=None):
        filme = self.get_object()
        reviews = filme.reviews.all()
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], url_path='reviews/create', permission_classes=[permissions.IsAuthenticated])
    def create_review(self, request, slug=None):
        # --- MODO DE DEPURAÇÃO ---
        print("--- CABEÇALHOS RECEBIDOS NO BACKEND ---")
        print(request.headers)
        print("------------------------------------")
        
        filme = self.get_object()
        user = request.user
        if Review.objects.filter(filme=filme, autor=user).exists():
            return Response({'detail': 'Você já fez uma review para este filme.'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(autor=user, filme=filme)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(autor=self.request.user)

class WatchlistViewSet(viewsets.ModelViewSet):
    serializer_class = WatchlistSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Watchlist.objects.filter(utilizador=self.request.user)

    def perform_create(self, serializer):
        serializer.save(utilizador=self.request.user)

class FavoritoViewSet(WatchlistViewSet):
    serializer_class = FavoritoSerializer
    
    def get_queryset(self):
        return Favorito.objects.filter(utilizador=self.request.user)

class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]

class UserMeView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user
