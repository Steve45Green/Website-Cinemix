# backend/core/models/pessoa.py
from __future__ import annotations
from django.db import models

class Pessoa(models.Model):
    nome = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=220, unique=True)
    bio = models.TextField(blank=True)
    foto = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["nome"]
        verbose_name = "Pessoa"
        verbose_name_plural = "Pessoas"

    def __str__(self) -> str:
        return self.nome


class Realizador(Pessoa):
    # Exemplo de campo específico (opcional):
    # portfolio = models.URLField(blank=True)

    class Meta:
        ordering = ["nome"]                    # repete/ajusta conforme precisares
        verbose_name = "Realizador"
        verbose_name_plural = "Realizadores"


class Ator(Pessoa):
    # Ex.: agente = models.CharField(max_length=200, blank=True)

    class Meta:
        ordering = ["nome"]
        verbose_name = "Ator"
        verbose_name_plural = "Atores"