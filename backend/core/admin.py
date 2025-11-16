# core/admin.py
from django.contrib import admin

# ───────────── Imports por módulo (robustos a issues no __init__) ─────────────
from .models.taxonomia import Pais, Lingua, Genero, Etiqueta, Categoria
from .models.pessoa import Pessoa, Realizador, Ator
from .models.filme import Filme
from .models.elenco import Elenco
from .models.video import Video
from .models.review import Review
from .models.listas import Watchlist, Favorito

# ===========================
#           INLINES
# ===========================

class ElencoInline(admin.TabularInline):
    """
    Inline dos créditos (elenco) dentro de Filme.
    Requer Elenco.filme (FK) e Elenco.pessoa (FK).
    """
    model = Elenco
    extra = 1
    autocomplete_fields = ("pessoa",)
    fields = ("pessoa", "papel", "ordem_credito")
    ordering = ("ordem_credito",)
    # Se o FK para Filme NÃO se chamar "filme", define:
    # fk_name = "o_nome_do_teu_fk"


class VideoInline(admin.TabularInline):
    """
    Inline dos vídeos (trailers, teasers) dentro de Filme.
    Requer Video.filme (FK).
    """
    model = Video
    extra = 1
    # Se no teu modelo o campo se chamar 'lingua', troca 'idioma' por 'lingua'
    fields = ("titulo", "tipo", "site", "key", "url", "idioma")
    ordering = ("-created_at",)
    # fk_name = "o_nome_do_teu_fk"  # se o FK para Filme tiver outro nome


# ===========================
#         TAXONOMIAS
# ===========================

@admin.register(Pais)
class PaisAdmin(admin.ModelAdmin):
    list_display = ("id", "nome", "iso2")
    search_fields = ("nome", "iso2")
    ordering = ("nome",)
    list_per_page = 50


@admin.register(Lingua)
class LinguaAdmin(admin.ModelAdmin):
    list_display = ("id", "nome", "codigo")
    search_fields = ("nome", "codigo")
    ordering = ("nome",)
    list_per_page = 50


@admin.register(Genero)
class GeneroAdmin(admin.ModelAdmin):
    list_display = ("id", "nome", "slug")
    search_fields = ("nome", "slug")
    prepopulated_fields = {"slug": ("nome",)}
    ordering = ("nome",)
    list_per_page = 50


@admin.register(Etiqueta)
class EtiquetaAdmin(admin.ModelAdmin):
    list_display = ("id", "nome", "slug")
    search_fields = ("nome", "slug")
    prepopulated_fields = {"slug": ("nome",)}
    ordering = ("nome",)
    list_per_page = 50


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    """
    Mantém apenas se tiveres Categoria em taxonomia.py.
    """
    list_display = ("id", "nome", "slug")
    search_fields = ("nome", "slug")
    prepopulated_fields = {"slug": ("nome",)}
    ordering = ("nome",)
    list_per_page = 50


# ===========================
#           PESSOAS
# ===========================

@admin.register(Pessoa)
class PessoaAdmin(admin.ModelAdmin):
    list_display = ("id", "nome", "created_at")
    search_fields = ("nome", "id", "slug")
    ordering = ("nome",)
    date_hierarchy = "created_at"
    list_per_page = 50


@admin.register(Realizador)
class RealizadorAdmin(admin.ModelAdmin):
    """
    Funciona quer Realizador seja PROXY (Meta.proxy = True) quer modelo CONCRETO.
    """
    list_display = ("id", "nome", "created_at")
    search_fields = ("nome", "slug")
    ordering = ("nome",)
    date_hierarchy = "created_at"
    list_per_page = 50


@admin.register(Ator)
class AtorAdmin(admin.ModelAdmin):
    """
    Funciona quer Ator seja PROXY quer modelo CONCRETO.
    """
    list_display = ("id", "nome", "created_at")
    search_fields = ("nome", "slug")
    ordering = ("nome",)
    date_hierarchy = "created_at"
    list_per_page = 50


# ===========================
#     FILME & RELACIONADOS
# ===========================

@admin.register(Filme)
class FilmeAdmin(admin.ModelAdmin):
    """
    Admin principal para Filme, com inlines de Elenco e Video.
    """
    inlines = [ElencoInline, VideoInline]

    list_display = ("id", "titulo", "ano_lancamento", "popularidade", "media_rating", "created_at")
    list_filter = ("ano_lancamento", "generos", "etiquetas", "paises", "linguas", "created_at")
    search_fields = (
        "titulo", "descricao", "slug",
        # Se Elenco.filme tiver related_name="creditos":
        "creditos__pessoa__nome",
        # Caso NÃO tenhas related_name em Elenco.filme, usa:
        # "elenco__pessoa__nome",
        "generos__nome", "etiquetas__nome",
    )
    prepopulated_fields = {"slug": ("titulo",)}
    filter_horizontal = ("generos", "etiquetas", "paises", "linguas")
    date_hierarchy = "created_at"
    ordering = ("-popularidade", "-media_rating", "titulo")
    list_per_page = 50
    # list_select_related = ("algum_fk",)  # se tiveres FKs frequentes


@admin.register(Elenco)
class ElencoAdmin(admin.ModelAdmin):
    list_display = ("id", "filme", "pessoa", "papel", "ordem_credito")
    list_filter = ("filme", "pessoa")
    search_fields = ("filme__titulo", "pessoa__nome", "papel")
    ordering = ("filme", "ordem_credito")
    autocomplete_fields = ("filme", "pessoa")
    list_per_page = 50


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ("id", "filme", "titulo", "tipo", "site", "created_at")
    # Se o campo for 'lingua', troca 'idioma' por 'lingua' nos filtros
    list_filter = ("tipo", "site", "idioma", "filme")
    search_fields = ("titulo", "filme__titulo", "site", "key")
    ordering = ("-created_at",)
    autocomplete_fields = ("filme",)
    date_hierarchy = "created_at"
    list_per_page = 50


# ===========================
#     REVIEWS / LISTAS
# ===========================

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("id", "filme", "autor", "rating", "created_at")
    list_filter = ("rating", "filme", "created_at")
    search_fields = ("filme__titulo", "autor__username", "titulo", "texto")
    ordering = ("-created_at",)
    date_hierarchy = "created_at"
    autocomplete_fields = ("filme", "autor")
    list_per_page = 50


@admin.register(Watchlist)
class WatchlistAdmin(admin.ModelAdmin):
    list_display = ("id", "utilizador", "filme", "created_at")
    list_filter = ("utilizador", "filme", "created_at")
    search_fields = ("utilizador__username", "filme__titulo")
    ordering = ("-created_at",)
    autocomplete_fields = ("utilizador", "filme")
    date_hierarchy = "created_at"
    list_per_page = 50


@admin.register(Favorito)
class FavoritoAdmin(admin.ModelAdmin):
    list_display = ("id", "utilizador", "filme", "created_at")
    list_filter = ("utilizador", "filme", "created_at")
    search_fields = ("utilizador__username", "filme__titulo")
    ordering = ("-created_at",)
    autocomplete_fields = ("utilizador", "filme")
    date_hierarchy = "created_at"
    list_per_page = 50
