from django.urls import path, include
from django.contrib import admin
from rest_framework.routers import DefaultRouter
from inmobiliaria.views import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = DefaultRouter()
router.register(r'paises', PaisViewSet)
router.register(r'ciudades', CiudadViewSet)
router.register(r'sectores', SectorViewSet)
router.register(r'tiposDeCaracteristicas', TipoDeCaracteristicaViewSet)
router.register(r'usuarios', UsuarioViewSet)
router.register(r'caracteristicas', CaracteristicaViewSet)
router.register(r'tiposDeInmuebles', TipoDeInmuebleViewSet)
router.register(r'inmuebles', InmuebleViewSet)
router.register(r'inmueblesPorUsuario', InmueblePorUsuarioViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]