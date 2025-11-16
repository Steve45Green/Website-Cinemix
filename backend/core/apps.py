# backend/core/apps.py
from django.apps import AppConfig
import logging

logger = logging.getLogger(__name__)

class CoreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "backend.core"   # ← atualizado
    verbose_name = "Core"

    def ready(self):
        try:
            from . import signals  # noqa: F401
            logger.debug("Sinais do core carregados com sucesso.")
        except Exception as e:
            logger.exception("Falha a importar core.signals: %s", e)
