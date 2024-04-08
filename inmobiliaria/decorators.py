from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from rest_framework_simplejwt.authentication import JWTAuthentication
from functools import wraps

def jwt_login_required(view_func):
    @wraps(view_func)
    def wrapped_view(request, *args, **kwargs):
        # Verificar si el usuario está autenticado mediante JWT
        jwt_authentication = JWTAuthentication()
        user, _ = jwt_authentication.authenticate(request)
        if user is None:
            # Si el usuario no está autenticado, redireccionarlo a la página de inicio de sesión
            return HttpResponse("Unauthorized", status=401)
        # Si el usuario está autenticado, continuar con la vista
        return view_func(request, *args, **kwargs)
    return wrapped_view
