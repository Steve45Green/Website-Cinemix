from __future__ import annotations
from django.db import models


class Genero(models.Model):
    nome = models.CharField(max_length=100, unique=True, db_index=True)
    slug = models.SlugField(max_length=120, unique=True)

    class Meta:
        ordering = ["nome"]
        verbose_name = "Género"
        verbose_name_plural = "Géneros"

    def __str__(self) -> str:
        return self.nome


class Etiqueta(models.Model):
    nome = models.CharField(max_length=100, unique=True, db_index=True)
    slug = models.SlugField(max_length=120, unique=True)

    class Meta:
        ordering = ["nome"]
        verbose_name = "Etiqueta"
        verbose_name_plural = "Etiquetas"

    def __str__(self) -> str:
        return self.nome

class Pais(models.Model):
    nome = models.CharField(max_length=100, db_index=True)
    iso2 = models.CharField("Código ISO2", max_length=2, unique=True, db_index=True)

    class Meta:
        ordering = ["nome"]
        verbose_name = "País"
        verbose_name_plural = "Países"

    def __str__(self) -> str:
        return f"{self.nome} ({self.iso2})"

class Lingua(models.Model):
    nome = models.CharField(max_length=100, db_index=True)
    codigo = models.CharField("Código", max_length=10, unique=True, db_index=True)

    class Meta:
        ordering = ["nome"]
        verbose_name = "Língua"
        verbose_name_plural = "Línguas"

    def __str__(self) -> str:
        return f"{self.nome} ({self.codigo})"

class Categoria(models.Model):
    """Categoria de topo (ex.: Filme, Série, Documentário, etc.)."""
    nome = models.CharField(max_length=100, unique=True, db_index=True)
    slug = models.SlugField(max_length=120, unique=True)

    class Meta:
        ordering = ["nome"]
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"

    def __str__(self) -> str:
        return self.nome