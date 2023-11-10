from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import *
from .serializers import *
from django.core.exceptions import FullResultSet

    
class PaisViewSet(viewsets.ModelViewSet):
    queryset = Pais.objects.all()
    serializer_class = PaisSerializer

class CiudadViewSet(viewsets.ModelViewSet):
    queryset = Ciudad.objects.all()
    serializer_class = CiudadSerializer

class SectorViewSet(viewsets.ModelViewSet):
    queryset = Sector.objects.all()
    serializer_class = SectorSerializer
    
class TipoDeCaracteristicaViewSet(viewsets.ModelViewSet):
    queryset = TipoDeCaracteristica.objects.all()
    serializer_class = TipoDeCaracteristicaSerializer
    
class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    
class CaracteristicaViewSet(viewsets.ModelViewSet):
    queryset = Caracteristica.objects.all()
    serializer_class = CaracteristicaSerializer
    
class TipoDeInmuebleViewSet(viewsets.ModelViewSet):
    queryset = TipoDeInmueble.objects.all()
    serializer_class = TipoDeInmuebleSerializer

class InmuebleViewSet(viewsets.ModelViewSet):
    queryset = Inmueble.objects.all()
    serializer_class = InmuebleSerializer
    
class InmueblePorUsuarioViewSet(viewsets.ModelViewSet):
    queryset = InmueblePorUsuario.objects.all()
    serializer_class = InmueblePorUsuarioSerializer

