from rest_framework import serializers
from .models import *

class PaisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pais
        fields = '__all__'
    
class CiudadSerializer(serializers.ModelSerializer):
    idPais = PaisSerializer()
    
    class Meta:
        model = Ciudad
        fields = '__all__'

class SectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sector
        fields = '__all__'

class TipoDeCaracteristicaSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoDeCaracteristica
        fields = '__all__'

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = '__all__'
    
class CaracteristicaSerializer(serializers.ModelSerializer):
    idTipoCaracteristica = TipoDeCaracteristicaSerializer()
    
    class Meta:
        model = Caracteristica
        fields = '__all__'

class TipoDeInmuebleSerializer(serializers.ModelSerializer):    
    class Meta:
        model = TipoDeInmueble
        fields = '__all__'
    
class InmuebleSerializer(serializers.ModelSerializer):
    idSector = SectorSerializer()
    idCiudad = CiudadSerializer()
    Caracteristica = CaracteristicaSerializer(many = True)
    
    class Meta:
        model = Inmueble
        fields = '__all__'

class InmueblePorUsuarioSerializer(serializers.ModelSerializer):
    idUsuario = UsuarioSerializer()
    idInmueble = InmuebleSerializer()
    
    class Meta:
        model = InmueblePorUsuario
        fields = '__all__'

