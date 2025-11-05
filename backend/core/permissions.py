from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerOrReadOnly(BasePermission):
    """
    Só (autor) pode alterar/apagar; leitura é pública.
    Requer que o objeto tenha atributo `.autor` ou `.utilizador`.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        owner = getattr(obj, "autor", None) or getattr(obj, "utilizador", None)
        return owner == request.user

