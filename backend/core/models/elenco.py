from __future__ import annotations

from django.db import models


class Elenco(models.Model):
    filme = models.ForeignKey("core.Filme", on_delete=models.CASCADE, related_name="creditos")
    pessoa = models.ForeignKey("core.Pessoa", on_delete=models.CASCADE, related_name="creditos")
    papel = models.CharField(max_length=200, blank=True)  # ex.: "Ator", "Realizador"
    ordem_credito = models.PositiveIntegerField(default=0, db_index=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  # ← pedido

    class Meta:
        ordering = ["ordem_credito", "id"]
        verbose_name = "Crédito"
        verbose_name_plural = "Créditos"
        indexes = [models.Index(fields=["ordem_credito"])]
        unique_together = [
            ("filme", "pessoa", "papel", "ordem_credito"),
        ]

    def __str__(self) -> str:
        base = f"{self.pessoa} @ {self.filme}"
        return f"{self.ordem_credito:03d} - {base}" if self.ordem_credito is not None else base