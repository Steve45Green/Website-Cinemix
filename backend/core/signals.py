# -*- coding: utf-8 -*-
"""
Sinais (Signals) para a aplicação 'core'.

Os sinais são um mecanismo do Django que permite que certas ações (remetentes)
notifiquem outras partes da aplicação (receptores) quando um evento ocorre.

Neste ficheiro, definimos receptores que são acionados sempre que uma `Review`
é guardada (`post_save`) ou apagada (`post_delete`). A função destes receptores
é recalcular e atualizar os campos agregados `media_rating` e `reviews_count`
no modelo `Filme` correspondente, mantendo assim os dados consistentes e
otimizados para leitura.
"""
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.apps import apps
from django.db.models import Avg, Count

# --- Carregamento dinâmico dos modelos ---
# `apps.get_model` é usado para obter as classes dos modelos de forma segura,
# evitando importações circulares, especialmente durante a inicialização do Django.
Filme = apps.get_model("core", "Filme")
Review = apps.get_model("core", "Review")


def _atualizar_agregados_filme(filme_id: int):
    """
    Função auxiliar para recalcular e atualizar os dados agregados de um Filme.

    Esta função é chamada sempre que uma review é criada, atualizada ou apagada.
    Ela executa uma única query à base de dados para obter a nova média de
    classificações (rating) e o número total de reviews para um dado filme.

    Args:
        filme_id: O ID do filme que precisa de ser atualizado.
    """
    try:
        filme = Filme.objects.get(id=filme_id)
    except Filme.DoesNotExist:
        # Se o filme não for encontrado (caso raro), não há nada a fazer.
        return

    # Executa uma query de agregação na tabela de Reviews.
    # `aggregate` calcula a média (`Avg`) do campo 'rating' e a contagem (`Count`)
    # de registos, tudo numa única operação na base de dados.
    agregados = Review.objects.filter(filme_id=filme_id).aggregate(
        media=Avg("rating"),
        total=Count("id"),
    )

    # Atualiza os campos do objeto Filme em memória.
    # Se não houver reviews, `media` será None, pelo que usamos `or 0.0`.
    filme.media_rating = agregados["media"] or 0.0
    filme.reviews_count = agregados["total"] or 0

    # Guarda as alterações na base de dados.
    # `update_fields` é uma otimização importante: especifica quais colunas
    # devem ser atualizadas, evitando reescrever o registo inteiro e acionar
    # desnecessariamente outros sinais ou lógica de `auto_now`.
    filme.save(update_fields=["media_rating", "reviews_count", "updated_at"])


@receiver(post_save, sender=Review)
def review_post_save(sender, instance, created, **kwargs):
    """
    Receptor acionado após uma `Review` ser guardada (criada ou atualizada).

    O decorador `@receiver` conecta esta função ao sinal `post_save` emitido
    pelo modelo `Review`.

    Args:
        sender: A classe do modelo que emitiu o sinal (Review).
        instance: A instância específica do modelo que foi guardada.
        created: Um booleano que é True se um novo registo foi criado.
        **kwargs: Argumentos adicionais do sinal.
    """
    # Chama a função auxiliar para atualizar os dados do filme associado.
    _atualizar_agregados_filme(instance.filme_id)


@receiver(post_delete, sender=Review)
def review_post_delete(sender, instance, **kwargs):
    """
    Receptor acionado após uma `Review` ser apagada.

    O decorador `@receiver` conecta esta função ao sinal `post_delete` emitido
    pelo modelo `Review`.

    Args:
        sender: A classe do modelo que emitiu o sinal (Review).
        instance: A instância específica do modelo que foi apagada.
        **kwargs: Argumentos adicionais do sinal.
    """
    # Chama a função auxiliar para atualizar os dados do filme associado.
    _atualizar_agregados_filme(instance.filme_id)
