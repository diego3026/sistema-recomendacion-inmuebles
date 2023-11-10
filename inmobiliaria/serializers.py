from rest_framework import serializers
from .models import *

class PaisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pais
        fields = '__all__'

class CiudadSerializer(serializers.ModelSerializer):
    pais = PaisSerializer()

    class Meta:
        model = Ciudad
        fields = '__all__'
        
    def create(self, validated_data):
        pais_data = validated_data.pop('pais')
        pais_instance, _ = Pais.objects.get_or_create(**pais_data)
        ciudad_instance = Ciudad.objects.create(pais=pais_instance, **validated_data)
        return ciudad_instance

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
    tipoDeCaracteristica = TipoDeCaracteristicaSerializer()
    
    class Meta:
        model = Caracteristica
        fields = '__all__'
        
    def create(self, validated_data):
        tipo_data = validated_data.pop('tipoDeCaracteristica')
        tipo_instance, _ = TipoDeCaracteristica.objects.get_or_create(**tipo_data)
        caracteristica_instance = Caracteristica.objects.create(tipoDeCaracteristica=tipo_instance, **validated_data)
        return caracteristica_instance

class TipoDeInmuebleSerializer(serializers.ModelSerializer):    
    class Meta:
        model = TipoDeInmueble
        fields = '__all__'
    
class InmuebleSerializer(serializers.ModelSerializer):
    sector = SectorSerializer()
    ciudad = CiudadSerializer()
    caracteristicas = CaracteristicaSerializer(many = True)
    
    class Meta:
        model = Inmueble
        fields = '__all__'
    
    def create(self, validated_data):
        sector_data = validated_data.pop('sector')
        ciudad_data = validated_data.pop('ciudad')
        caracteristicas_data = validated_data.pop('caracteristicas')
        
        inmueble_instance = Inmueble.objects.create(**validated_data)

        for caracteristica_data in caracteristicas_data:
            caracteristica_instance, _ = Caracteristica.objects.get_or_create(**caracteristica_data)
            inmueble_instance.caracteristicas.add(caracteristica_instance)
    
        ciudad_instance, _ = Ciudad.objects.get_or_create(**ciudad_data)
        sector_instance, _ = Sector.objects.get_or_create(**sector_data)
        inmueble_instance.sector = sector_instance
        inmueble_instance.ciudad = ciudad_instance
        inmueble_instance.save()
        return inmueble_instance

class InmueblePorUsuarioSerializer(serializers.ModelSerializer):
    usuario = UsuarioSerializer()
    inmueble = InmuebleSerializer()
    
    class Meta:
        model = InmueblePorUsuario
        fields = '__all__'
        
    def create(self, validated_data):
        usuario_data = validated_data.pop('usuario')
        usuario_instance, _ = Sector.objects.get_or_create(**usuario_data)
        inmueble_data = validated_data.pop('inmueble')
        inmueble_instance, _ = Ciudad.objects.get_or_create(**inmueble_data)
        
        inmueblePorUsuario_instance = InmueblePorUsuario.objects.create(usuario=usuario_instance,inmueble=inmueble_instance, **validated_data)
        return inmueblePorUsuario_instance
 