from __future__ import annotations
from django.conf import settings
from django.db import models


class Watchlist(models.Model):
    utilizador = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="watchlist_items")
    filme = models.ForeignKey("core.Filme", on_delete=models.CASCADE, related_name="watchlisted_por")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  # opcional

    class Meta:
        ordering = ["-created_at", "id"]
        verbose_name = "Watchlist"
        verbose_name_plural = "Watchlists"
        constraints = [
            models.UniqueConstraint(fields=["utilizador", "filme"], name="unique_watchlist_por_user_filme"),
        ]

    def __str__(self) -> str:
        return f"{self.utilizador} → {self.filme}"


class Favorito(models.Model):
    utilizador = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="favoritos")
    filme = models.ForeignKey("core.Filme", on_delete=models.CASCADE, related_name="favoritado_por")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  # opcional

    class Meta:
        ordering = ["-created_at", "id"]
        verbose_name = "Favorito"
        verbose_name_plural = "Favoritos"
        constraints = [
            models.UniqueConstraint(fields=["utilizador", "filme"], name="unique_favorito_por_user_filme"),
        ]

    def __str__(self) -> str:
        return f"★ {self.utilizador} → {self.filme}"