# -*- coding: utf-8 -*-
from __future__ import annotations
from django.db import models

class Elenco(models.Model):
    """
    Represents the relationship between a Movie and a Person (cast/crew).
    This is a through model for the many-to-many relationship.
    """
    filme = models.ForeignKey(
        "core.Filme",
        verbose_name="Movie",
        on_delete=models.CASCADE,
        related_name="creditos",
        help_text="The movie to which this credit belongs."
    )
    pessoa = models.ForeignKey(
        "core.Pessoa",
        verbose_name="Person",
        on_delete=models.CASCADE,
        related_name="creditos",
        help_text="The person who is part of the cast or crew."
    )
    papel = models.CharField(
        "Role",
        max_length=150,
        blank=True,
        help_text="The role played by the person (e.g., 'Actor', 'Director', 'Screenwriter')."
    )
    ordem_credito = models.PositiveIntegerField(
        "Credit Order",
        default=0,
        db_index=True,
        help_text="The order of appearance in the credits, for sorting (0 is most important)."
    )

    class Meta:
        verbose_name = "Credit"
        verbose_name_plural = "Credits"
        ordering = ["ordem_credito"]
        unique_together = [["filme", "pessoa", "papel"]]
        indexes = [
            models.Index(fields=["ordem_credito"], name="idx_elenco_ordem"),
        ]

    def __str__(self) -> str:
        return f"{self.pessoa} as {self.papel} in {self.filme}"
