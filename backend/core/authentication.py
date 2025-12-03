# backend/core/authentication.py
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken

class JWTCookieAuthentication(JWTAuthentication):
    """
    Uma classe de autenticação que tenta validar um token JWT.
    Se o token for inválido ou expirado, em vez de lançar um erro,
    ela simplesmente retorna `None`, tratando o utilizador como anónimo.
    Isto permite que as páginas públicas continuem a funcionar mesmo
    se um utilizador tiver um token expirado no seu navegador.
    """
    def authenticate(self, request):
        try:
            return super().authenticate(request)
        except InvalidToken:
            return None
