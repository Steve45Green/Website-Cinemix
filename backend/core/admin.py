# -*- coding: utf-8 -*-
from django.contrib import admin
from .models.taxonomia import Pais, Lingua, Genero, Etiqueta, Categoria
from .models.pessoa import Pessoa, Realizador, Ator
from .models.filme import Filme
from .models.elenco import Elenco
from .models.video import Video
from .models.review import Review
from .models.listas import Watchlist, Favorito

class ElencoInline(admin.TabularInline):
    model = Elenco
    extra = 1
    autocomplete_fields = ("pessoa",)

class VideoInline(admin.TabularInline):
    model = Video
    extra = 1

@admin.register(Pais)
class PaisAdmin(admin.ModelAdmin):
    list_display = ("id", "nome", "iso2")
    search_fields = ("nome", "iso2")

@admin.register(Lingua)
class LinguaAdmin(admin.ModelAdmin):
    list_display = ("id", "nome", "codigo")
    search_fields = ("nome", "codigo")

@admin.register(Genero)
class GeneroAdmin(admin.ModelAdmin):
    list_display = ("id", "nome", "slug")
    search_fields = ("nome", "slug")
    prepopulated_fields = {"slug": ("nome",)}

@admin.register(Etiqueta)
class EtiquetaAdmin(admin.ModelAdmin):
    list_display = ("id", "nome", "slug")
    search_fields = ("nome", "slug")
    prepopulated_fields = {"slug": ("nome",)}

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("id", "nome", "slug")
    search_fields = ("nome", "slug")
    prepopulated_fields = {"slug": ("nome",)}

@admin.register(Pessoa)
class PessoaAdmin(admin.ModelAdmin):
    list_display = ("id", "nome")
    search_fields = ("nome",)

@admin.register(Realizador)
class RealizadorAdmin(admin.ModelAdmin):
    list_display = ("id", "nome")
    search_fields = ("nome",)

@admin.register(Ator)
class AtorAdmin(admin.ModelAdmin):
    list_display = ("id", "nome")
    search_fields = ("nome",)

@admin.register(Filme)
class FilmeAdmin(admin.ModelAdmin):
    inlines = [ElencoInline, VideoInline]
    # CORREÇÃO: Removidos os campos que já não existem no modelo Filme
    list_display = ("id", "titulo", "ano_lancamento", "media_rating", "imdb_id")
    list_filter = ("ano_lancamento", "generos")
    search_fields = ("titulo", "descricao", "imdb_id")
    prepopulated_fields = {"slug": ("titulo",)}
    filter_horizontal = ("generos",)

@admin.register(Elenco)
class ElencoAdmin(admin.ModelAdmin):
    list_display = ("filme", "pessoa", "papel")
    search_fields = ("filme__titulo", "pessoa__nome")

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ("filme", "titulo", "tipo")
    search_fields = ("filme__titulo", "titulo")

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("filme", "autor", "rating")
    search_fields = ("filme__titulo", "autor__username")

@admin.register(Watchlist)
class WatchlistAdmin(admin.ModelAdmin):
    list_display = ("utilizador", "filme")
    search_fields = ("utilizador__username", "filme__titulo")

@admin.register(Favorito)
class FavoritoAdmin(admin.ModelAdmin):
    list_display = ("utilizador", "filme")
    search_fields = ("utilizador__username", "filme__titulo")
