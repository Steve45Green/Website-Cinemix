# -*- coding: utf-8 -*-
from __future__ import annotations
from django.db import models

class Pessoa(models.Model):
    """
    Represents a person involved in the film industry (e.g., actor, director).
    """
    nome = models.CharField(
        "Name",
        max_length=250,
        db_index=True,
        help_text="The person's full name."
    )
    slug = models.SlugField(
        "Slug",
        max_length=260,
        unique=True,
        help_text="URL-friendly identifier."
    )
    bio = models.TextField(
        "Biography",
        blank=True,
        help_text="A short biography of the person."
    )
    foto = models.URLField(
        "Photo URL",
        blank=True,
        help_text="URL for the person's photo."
    )
    created_at = models.DateTimeField("Date Created", auto_now_add=True)
    updated_at = models.DateTimeField("Last Updated", auto_now=True)

    class Meta:
        verbose_name = "Person"
        verbose_name_plural = "People"
        ordering = ["nome"]

    def __str__(self) -> str:
        return self.nome

class Realizador(Pessoa):
    """
    A proxy model to manage directors separately in the admin interface.
    """
    class Meta:
        proxy = True
        verbose_name = "Director"
        verbose_name_plural = "Directors"

class Ator(Pessoa):
    """
    A proxy model to manage actors separately in the admin interface.
    """
    class Meta:
        proxy = True
        verbose_name = "Actor"
        verbose_name_plural = "Actors"
