# -*- coding: utf-8 -*-
from django.apps import AppConfig
import logging

# Configuração inicial do logger para este módulo.
logger = logging.getLogger(__name__)

class CoreConfig(AppConfig):
    """
    Configuração da aplicação 'core'.

    Esta classe é utilizada pelo Django para configurar a aplicação.
    Define o tipo de campo de chave primária automática e o nome da aplicação.
    O método `ready` é especialmente importante, pois é aqui que os sinais (signals)
    são importados e registados, garantindo que são ativados quando a aplicação arranca.
    """
    # Define o tipo de campo padrão para chaves primárias automáticas.
    # BigAutoField é um inteiro de 64 bits, ideal para escalabilidade.
    default_auto_field = "django.db.models.BigAutoField"

    # O nome completo da aplicação, incluindo o namespace do projeto.
    # Essencial para que o Django localize corretamente a aplicação.
    name = "backend.core"

    # Nome legível para a aplicação, usado na interface de administração do Django.
    verbose_name = "Core"

    def ready(self):
        """
        Executa código de inicialização quando a aplicação está pronta.

        Este método é o local recomendado para importar e conectar sinais,
        evitando problemas de importação circular e garantindo que os `handlers`
        estão prontos para receber eventos.
        """
        try:
            # Importa o módulo de sinais da aplicação 'core'.
            # A diretiva `# noqa: F401` indica ao linter para ignorar o aviso
            # de "módulo importado mas não utilizado", pois a importação é
            # necessária para que os sinais sejam registados.
            from . import signals  # noqa: F401
            logger.debug("Sinais da aplicação 'core' carregados com sucesso.")
        except Exception as e:
            # Regista uma exceção detalhada se a importação dos sinais falhar.
            # Isto é crucial para depurar problemas durante o arranque do servidor.
            logger.exception("Falha ao importar 'core.signals': %s", e)
