# -*- coding: utf-8 -*-
from __future__ import annotations
from django.db import models

class Video(models.Model):
    """
    Represents a video related to a movie (e.g., trailer, teaser).
    """
    class TipoVideo(models.TextChoices):
        TRAILER = "trailer", "Trailer"
        TEASER = "teaser", "Teaser"
        BEHIND_THE_SCENES = "behind_the_scenes", "Behind the Scenes"
        CLIP = "clip", "Clip"
        FEATURETTE = "featurette", "Featurette"

    class SiteVideo(models.TextChoices):
        YOUTUBE = "youtube", "YouTube"
        VIMEO = "vimeo", "Vimeo"

    filme = models.ForeignKey(
        "core.Filme",
        verbose_name="Movie",
        on_delete=models.CASCADE,
        related_name="videos",
        help_text="The movie this video belongs to."
    )
    titulo = models.CharField(
        "Title",
        max_length=200,
        help_text="The title of the video (e.g., 'Official Trailer')."
    )
    tipo = models.CharField(
        "Video Type",
        max_length=50,
        choices=TipoVideo.choices,
        default=TipoVideo.TRAILER,
        help_text="The category of the video (e.g., Trailer, Teaser)."
    )
    site = models.CharField(
        "Platform",
        max_length=50,
        choices=SiteVideo.choices,
        default=SiteVideo.YOUTUBE,
        help_text="The platform where the video is hosted (e.g., YouTube, Vimeo)."
    )
    key = models.CharField(
        "Video Key",
        max_length=100,
        help_text="The unique identifier of the video on the platform (e.g., a YouTube video ID)."
    )
    url = models.URLField(
        "Video URL",
        blank=True,
        help_text="The full URL to access the video."
    )
    idioma = models.CharField(
        "Language",
        max_length=10,
        blank=True,
        help_text="The language code of the video (e.g., 'pt-PT', 'en-US')."
    )
    created_at = models.DateTimeField("Date Created", auto_now_add=True)
    updated_at = models.DateTimeField("Last Updated", auto_now=True)

    class Meta:
        verbose_name = "Video"
        verbose_name_plural = "Videos"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["-created_at"], name="idx_video_created_at"),
            models.Index(fields=["tipo"], name="idx_video_tipo"),
        ]

    def __str__(self) -> str:
        return f"{self.get_tipo_display()} for {self.filme.titulo}"
