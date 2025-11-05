from __future__ import annotations
from django.conf import settings
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Review(models.Model):
    filme = models.ForeignKey("core.Filme", on_delete=models.CASCADE, related_name="reviews")
    autor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reviews")

    titulo = models.CharField(max_length=200, blank=True)
    texto = models.TextField(blank=True)
    rating = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)])

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at", "id"]
        constraints = [
            models.UniqueConstraint(fields=["filme", "autor"], name="unique_review_por_filme_autor"),
        ]

    def __str__(self) -> str:
        return f"Review {self.rating}/10 por {self.autor} — {self.filme}"