from datetime import timedelta
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken

class TokenRenewMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Verificar si el usuario está autenticado y si hay un token de acceso
        if request.user.is_authenticated:
            access_token = request.COOKIES.get('access_token')
            if access_token:
                try:
                    # Decodificar el token de acceso para obtener la fecha de expiración
                    token = RefreshToken(access_token)
                    token_expiration = token.access_token['exp']

                    # Verificar si el token de acceso está a punto de expirar
                    if token_expiration > timezone.now() + timedelta(seconds=150):
                        refresh = RefreshToken(access_token)
                        access_token = str(refresh.access_token)

                        # Actualizar el token de acceso en la cookie
                        response.set_cookie('access_token', access_token, httponly=True)
                except Exception as e:
                    pass
        return response
