# -*- coding: utf-8 -*-
from __future__ import annotations
from django.db import models
from django.utils.text import slugify

class Filme(models.Model):
    """
    Representa um filme no catálogo.
    """
    titulo = models.CharField(
        "Título",
        max_length=250,
        db_index=True,
        help_text="O título principal do filme."
    )
    slug = models.SlugField(
        "Slug",
        max_length=260,
        unique=True,
        help_text="URL amigável gerado a partir do título."
    )
    descricao = models.TextField(
        "Descrição",
        blank=True,
        help_text="Sinopse ou resumo do enredo do filme."
    )
    ano_lancamento = models.PositiveIntegerField(
        "Ano de Lançamento",
        null=True,
        blank=True,
        db_index=True,
        help_text="Ano em que o filme foi lançado."
    )
    # Novo campo para o ID do IMDb
    imdb_id = models.CharField(
        "ID do IMDb",
        max_length=20,
        unique=True,
        db_index=True,
        null=True,
        blank=True,
        help_text="O identificador único do filme no IMDb (ex: tt0111161)."
    )
    media_rating = models.FloatField(
        "Média de Avaliações",
        default=0,
        db_index=True,
        help_text="A média de todas as avaliações dos utilizadores."
    )
    poster = models.URLField(
        "Poster",
        blank=True,
        help_text="URL para a imagem do poster do filme."
    )
    backdrop = models.URLField(
        "Imagem de Fundo",
        blank=True,
        help_text="URL para a imagem de fundo (backdrop)."
    )
    # ... (relações com outras tabelas) ...
    generos = models.ManyToManyField("core.Genero", blank=True, related_name="filmes")
    
    created_at = models.DateTimeField("Data de Criação", auto_now_add=True)
    updated_at = models.DateTimeField("Última Atualização", auto_now=True)

    class Meta:
        verbose_name = "Filme"
        verbose_name_plural = "Filmes"
        ordering = ["-media_rating", "titulo"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.titulo}-{self.ano_lancamento}")
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.titulo} ({self.ano_lancamento})"
