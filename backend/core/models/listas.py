# -*- coding: utf-8 -*-
from __future__ import annotations
from django.conf import settings
from django.db import models

class Watchlist(models.Model):
    """
    Represents a movie that a user wants to watch later.
    """
    utilizador = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="User",
        on_delete=models.CASCADE,
        related_name="watchlist_items"
    )
    filme = models.ForeignKey(
        "core.Filme",
        verbose_name="Movie",
        on_delete=models.CASCADE,
        related_name="watchlist_users"
    )
    created_at = models.DateTimeField("Date Added", auto_now_add=True)

    class Meta:
        verbose_name = "Watchlist Item"
        verbose_name_plural = "Watchlist Items"
        ordering = ["-created_at"]
        unique_together = [["utilizador", "filme"]]
        constraints = [
            models.UniqueConstraint(
                fields=["utilizador", "filme"],
                name="unique_watchlist_por_user_filme"
            )
        ]

    def __str__(self) -> str:
        return f"{self.filme} in {self.utilizador}'s watchlist"


class Favorito(models.Model):
    """
    Represents a user's favorite movie.
    """
    utilizador = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="User",
        on_delete=models.CASCADE,
        related_name="favoritos"
    )
    filme = models.ForeignKey(
        "core.Filme",
        verbose_name="Movie",
        on_delete=models.CASCADE,
        related_name="favorited_by"
    )
    created_at = models.DateTimeField("Date Added", auto_now_add=True)

    class Meta:
        verbose_name = "Favorite"
        verbose_name_plural = "Favorites"
        ordering = ["-created_at"]
        unique_together = [["utilizador", "filme"]]

    def __str__(self) -> str:
        return f"{self.filme} is a favorite of {self.utilizador}"
