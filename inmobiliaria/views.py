from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import *
from .serializers import *
from django.core.exceptions import FullResultSet


class CustomModelViewSet(viewsets.ModelViewSet):
    def list(self, request, *args, **kwargs):
        try:
            return super().list(request, *args, **kwargs)
        except FullResultSet:
            # Aquí puedes manejar la excepción FullResultSet según tus necesidades
            return Response(
                {"detail": "La consulta devolvió más resultados de los esperados."},
                status=status.HTTP_400_BAD_REQUEST
            )

class PaisViewSet(CustomModelViewSet):
    queryset = Pais.objects.all()
    serializer_class = PaisSerializer

class CiudadViewSet(CustomModelViewSet):
    queryset = Ciudad.objects.all()
    serializer_class = CiudadSerializer

class SectorViewSet(CustomModelViewSet):
    queryset = Sector.objects.all()
    serializer_class = SectorSerializer
    
class TipoDeCaracteristicaViewSet(CustomModelViewSet):
    queryset = TipoDeCaracteristica.objects.all()
    serializer_class = TipoDeCaracteristicaSerializer
    
class UsuarioViewSet(CustomModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    
class CaracteristicaViewSet(CustomModelViewSet):
    queryset = Caracteristica.objects.all()
    serializer_class = CaracteristicaSerializer
    
class TipoDeInmuebleViewSet(CustomModelViewSet):
    queryset = TipoDeInmueble.objects.all()
    serializer_class = TipoDeInmuebleSerializer

class InmuebleViewSet(CustomModelViewSet):
    queryset = Inmueble.objects.all()
    serializer_class = InmuebleSerializer
    
class InmueblePorUsuarioViewSet(CustomModelViewSet):
    queryset = InmueblePorUsuario.objects.all()
    serializer_class = InmueblePorUsuarioSerializer

