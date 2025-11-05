from __future__ import annotations

from django.db import models


class Filme(models.Model):
    titulo = models.CharField(max_length=250, db_index=True)
    slug = models.SlugField(max_length=260, unique=True)
    descricao = models.TextField(blank=True)
    ano_lancamento = models.PositiveIntegerField(null=True, blank=True, db_index=True)

    # métricas usadas nas views
    popularidade = models.FloatField(default=0, db_index=True)
    media_rating = models.FloatField(default=0, db_index=True)

    poster = models.URLField(blank=True)
    backdrop = models.URLField(blank=True)

    # taxonomias  (usar o app_label "core")
    generos = models.ManyToManyField("core.Genero", blank=True, related_name="filmes")
    etiquetas = models.ManyToManyField("core.Etiqueta", blank=True, related_name="filmes")
    paises = models.ManyToManyField("core.Pais", blank=True, related_name="filmes")
    linguas = models.ManyToManyField("core.Lingua", blank=True, related_name="filmes")
    # novos pedidos
    categoria = models.ForeignKey(
        "core.Categoria",
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name="filmes",
    )
    realizador = models.ForeignKey(
        "core.Pessoa",
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name="filmes_realizados",
    )
    # Nota: Mantemos também Elenco para papéis detalhados; 'atores' dá-te acesso direto a elenco principal, se quiseres.
    atores = models.ManyToManyField("core.Pessoa", blank=True, related_name="filmes_atuados")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  # ← pedido

    class Meta:
        ordering = ["-popularidade", "-media_rating", "titulo"]
        indexes = [
            models.Index(fields=["titulo"]),
            models.Index(fields=["popularidade"]),
            models.Index(fields=["media_rating"]),
            models.Index(fields=["ano_lancamento"]),
        ]

    def __str__(self) -> str:
        return self.titulo