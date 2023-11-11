from django.urls import path, include
from rest_framework.routers import DefaultRouter
from inmobiliaria.views import *

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
    path('', include(router.urls)),
]