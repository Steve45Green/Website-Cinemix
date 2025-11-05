from __future__ import annotations

from django.db import models


class Video(models.Model):
    TIPO_CHOICES = [
        ("trailer", "Trailer"),
        ("teaser", "Teaser"),
        ("clip", "Clip"),
        ("featurette", "Featurette"),
        ("outro", "Outro"),
    ]

    filme = models.ForeignKey("core.Filme", on_delete=models.CASCADE, related_name="videos")
    titulo = models.CharField(max_length=250, db_index=True)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default="trailer")
    url = models.URLField(max_length=500)
    site = models.CharField(max_length=50, blank=True)  # ex.: YouTube, Vimeo
    key = models.CharField(max_length=200, blank=True)  # ex.: id no YouTube
    idioma = models.CharField(max_length=20, blank=True)  # ex.: "pt-PT", "en-US"

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  # ← pedido

    class Meta:
        ordering = ["-created_at", "id"]
        indexes = [
            models.Index(fields=["-created_at"]),
            models.Index(fields=["tipo"]),
        ]

    def __str__(self) -> str:
        return f"{self.titulo} ({self.get_tipo_display()})"
