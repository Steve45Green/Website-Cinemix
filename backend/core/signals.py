# core/signals.py
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.apps import apps
from django.db.models import Avg, Count

Filme = apps.get_model("core", "Filme")
Review = apps.get_model("core", "Review")


def _atualizar_agregados_filme(filme_id: int):
    """Recalcula rating médio e número de reviews para um Filme."""
    try:
        filme = Filme.objects.get(id=filme_id)
    except Filme.DoesNotExist:
        return

    agg = Review.objects.filter(filme_id=filme_id).aggregate(
        media=Avg("rating"),
        total=Count("id"),
    )

    filme.rating_medio = agg["media"] or None
    filme.reviews_count = agg["total"] or 0
    # Evita sinais recursivos; atualiza só os campos necessários.
    filme.save(update_fields=["rating_medio", "reviews_count", "updated_at"])

@receiver(post_save, sender=Review)
def review_post_save(sender, instance, created, **kwargs):
    _atualizar_agregados_filme(instance.filme_id)

@receiver(post_delete, sender=Review)
def review_post_delete(sender, instance, **kwargs):
    _atualizar_agregados_filme(instance.filme_id)