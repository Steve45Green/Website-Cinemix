# -*- coding: utf-8 -*-
"""
Definição de classes de permissão personalizadas para a API.

As permissões no Django REST Framework são usadas para conceder ou negar
o acesso de diferentes tipos de utilizadores a determinadas views ou objetos.
"""
from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsOwnerOrReadOnly(BasePermission):
    """
    Permissão personalizada para permitir que apenas o proprietário de um objeto
    o possa editar ou apagar, enquanto permite a leitura a qualquer utilizador.

    Esta permissão é ideal para conteúdos gerados por utilizadores, como avaliações
    (reviews) ou comentários, onde o autor deve ter controlo total sobre a sua
    criação, mas a visualização é pública.

    A permissão assume que o objeto da base de dados tem um atributo que
    referencia o seu criador, como `autor` ou `utilizador`.
    """

    def has_object_permission(self, request, view, obj):
        """
        Verifica a permissão para um único objeto.

        Args:
            request: O objeto do pedido HTTP.
            view: A view que está a ser acedida.
            obj: O objeto da base de dados que está a ser verificado.

        Returns:
            bool: True se a permissão for concedida, False caso contrário.
        """
        # `SAFE_METHODS` é uma tupla que contém os métodos de pedido HTTP
        # considerados "seguros", ou seja, que não alteram o estado do
        # recurso: ('GET', 'HEAD', 'OPTIONS').
        # Se o método for seguro, permite o acesso a qualquer utilizador.
        if request.method in SAFE_METHODS:
            return True

        # Se o método não for seguro (ex: POST, PUT, PATCH, DELETE),
        # a permissão só é concedida se o utilizador que faz o pedido
        # for o proprietário do objeto.

        # Tenta obter o proprietário do objeto a partir do atributo `autor` ou `utilizador`.
        # `getattr` é usado para evitar erros caso o atributo não exista.
        owner = getattr(obj, "autor", None) or getattr(obj, "utilizador", None)

        # Compara o proprietário do objeto com o utilizador autenticado na sessão/pedido.
        return owner == request.user
