# -*- coding: utf-8 -*-
from __future__ import annotations
from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator

class Review(models.Model):
    """
    Representa uma review de um filme feita por um utilizador.
    """
    filme = models.ForeignKey(
        "core.Filme",
        on_delete=models.CASCADE,
        related_name="reviews",
        help_text="O filme ao qual esta review se refere."
    )
    autor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reviews",
        help_text="O autor da review."
    )
    titulo = models.CharField(
        "Título da Review",
        max_length=200,
        blank=True,
        help_text="Um título opcional para a review."
    )
    texto = models.TextField(
        "Texto da Review",
        help_text="O conteúdo da review."
    )
    rating = models.PositiveSmallIntegerField(
        "Avaliação",
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="A avaliação do utilizador para o filme, de 1 a 5."
    )
    # NOVO CAMPO: Para marcar se a review contém spoilers.
    spoiler = models.BooleanField(
        "Contém Spoilers",
        default=False,
        help_text="Marque se a review contém spoilers."
    )
    
    created_at = models.DateTimeField("Data de Criação", auto_now_add=True)
    updated_at = models.DateTimeField("Última Atualização", auto_now=True)

    class Meta:
        verbose_name = "Review"
        verbose_name_plural = "Reviews"
        ordering = ["-created_at"]
        # Garante que um utilizador só pode fazer uma review por filme
        unique_together = ('filme', 'autor')

    def __str__(self) -> str:
        return f"Review de {self.autor.username} para {self.filme.titulo}"
