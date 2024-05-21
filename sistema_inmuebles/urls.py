from django.urls import path, include
from django.contrib import admin
from rest_framework import permissions
from rest_framework.routers import DefaultRouter
from inmobiliaria.views import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from drf_yasg.views import get_schema_view # type: ignore
from drf_yasg import openapi # type: ignore

schema_view = get_schema_view(
    openapi.Info(
        title="sistema de recomendacion de inmuebles API",
        default_version='v1',
        contact=openapi.Contact(email="diegoonate3026@gmail.com"),
        license=openapi.License(name="GIDSYC"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
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
router.register(r'intereses', InteresViewSet)
router.register(r'interesesPorUsuario', InteresPorUsuarioViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/', include(router.urls)),
    path('api/login/', LoginAPIView.as_view(), name='login'),
    path('api/interesesPorUsuario/<int:idUsuario>/deleteInteresesPorUsuario/<int:idInteres>/', InteresPorUsuarioViewSet.as_view({'delete': 'deleteInteresesPorUsuario'}), name='delete_intereses_por_usuario'),
    path('api/register/', RegisterAPIView.as_view(), name='register'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
