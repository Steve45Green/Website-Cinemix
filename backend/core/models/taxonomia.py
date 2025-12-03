# -*- coding: utf-8 -*-
from __future__ import annotations
from django.db import models

class Genero(models.Model):
    nome = models.CharField(
        "Nome",
        max_length=100,
        unique=True,
        db_index=True,
        help_text="O nome do género."
    )
    slug = models.SlugField(
        "Slug",
        max_length=120,
        unique=True,
        help_text="URL amigável para o género."
    )

    class Meta:
        verbose_name = "Género"
        verbose_name_plural = "Géneros"
        ordering = ["nome"]

    def __str__(self) -> str:
        return self.nome

class Etiqueta(models.Model):
    nome = models.CharField(
        "Nome",
        max_length=100,
        unique=True,
        db_index=True,
        help_text="O nome da etiqueta."
    )
    slug = models.SlugField(
        "Slug",
        max_length=120,
        unique=True,
        help_text="URL amigável para a etiqueta."
    )

    class Meta:
        verbose_name = "Etiqueta"
        verbose_name_plural = "Etiquetas"
        ordering = ["nome"]

    def __str__(self) -> str:
        return self.nome

class Pais(models.Model):
    nome = models.CharField(
        "Nome",
        max_length=100,
        db_index=True,
        help_text="O nome do país."
    )
    iso2 = models.CharField(
        "Código ISO 3166-1 alpha-2",
        max_length=2,
        unique=True,
        db_index=True,
        help_text="O código de duas letras do país (ex: 'PT' para Portugal)."
    )

    class Meta:
        verbose_name = "País"
        verbose_name_plural = "Países"
        ordering = ["nome"]

    def __str__(self) -> str:
        return f"{self.nome} ({self.iso2})"

class Lingua(models.Model):
    nome = models.CharField(
        "Nome",
        max_length=100,
        db_index=True,
        help_text="O nome da língua (ex: 'Português', 'Inglês')."
    )
    codigo = models.CharField(
        "Código ISO 639-1",
        max_length=10,
        unique=True,
        db_index=True,
        help_text="O código da língua (ex: 'pt', 'en')."
    )

    class Meta:
        verbose_name = "Língua"
        verbose_name_plural = "Línguas"
        ordering = ["nome"]

    def __str__(self) -> str:
        return f"{self.nome} ({self.codigo})"

class Categoria(models.Model):
    nome = models.CharField(
        "Nome",
        max_length=100,
        unique=True,
        db_index=True,
        help_text="O nome da categoria."
    )
    slug = models.SlugField(
        "Slug",
        max_length=120,
        unique=True,
        help_text="URL amigável para a categoria."
    )

    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"
        ordering = ["nome"]

    def __str__(self) -> str:
        return self.nome
