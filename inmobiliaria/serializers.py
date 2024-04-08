from rest_framework import serializers
from .models import *


class PaisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pais
        fields = '__all__'


class DepartamentoSerializer(serializers.ModelSerializer):
    pais = PaisSerializer()

    class Meta:
        model = Departamento
        fields = '__all__'

    def create(self, validated_data):
        pais_data = validated_data.pop('pais')
        pais_instance, _ = Pais.objects.get_or_create(**pais_data)
        departamento_instance = Departamento.objects.create(pais=pais_instance, **validated_data)
        return departamento_instance


class CiudadSerializer(serializers.ModelSerializer):
    departamento = DepartamentoSerializer()

    class Meta:
        model = Ciudad
        fields = '__all__'

    def create(self, validated_data):
        departamento_data = validated_data.pop('departamento')
        pais_data = departamento_data.pop('pais')
        pais_instance, _ = Pais.objects.get_or_create(**pais_data)
        departamento_instance, _ = Departamento.objects.get_or_create(pais=pais_instance, **departamento_data)
        ciudad_instance = Ciudad.objects.create(departamento=departamento_instance, **validated_data)
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
        fields = ['id','nombre','apellido','username','email','edad']

class UsuarioLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=200)
    password = serializers.CharField(max_length=255, style={'input_type': 'password'})

class UsuarioRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['email', 'password', 'nombre', 'apellido', 'username', 'edad']

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
    tipoDeInmueble = TipoDeInmuebleSerializer()
    caracteristicas = CaracteristicaSerializer(many=True)

    class Meta:
        model = Inmueble
        fields = '__all__'

    def create(self, validated_data):
        sector_data = validated_data.pop('sector')
        ciudad_data = validated_data.pop('ciudad', None)
        tipo_inmueble_data = validated_data.pop('tipoDeInmueble')
        caracteristicas_data = validated_data.pop('caracteristicas')

        sector_instance, created = Sector.objects.get_or_create(**sector_data)
        tipo_inmueble_instance, _ = TipoDeInmueble.objects.get_or_create(**tipo_inmueble_data)

        ciudad_instance = None

        if ciudad_data:
            departamento_data = ciudad_data.pop('departamento', None)
            pais_data = departamento_data.pop('pais', None)

            pais_instance, _ = Pais.objects.get_or_create(**pais_data) if pais_data else (None, None)
            departamento_instance, _ = Departamento.objects.get_or_create(pais=pais_instance,
                                                                          **departamento_data) if departamento_data else (
            None, None)
            ciudad_instance, _ = Ciudad.objects.get_or_create(departamento=departamento_instance, **ciudad_data)

        inmueble_instance = Inmueble.objects.create(
            sector=sector_instance,
            ciudad=ciudad_instance,
            tipoDeInmueble=tipo_inmueble_instance,
            **validated_data
        )

        if caracteristicas_data:
            for caracteristica_data in caracteristicas_data:
                tipoDeCaracteristica_data = caracteristica_data.pop('tipoDeCaracteristica')
                tipoDeCaracteristica_instance, _ = TipoDeCaracteristica.objects.get_or_create(
                    **tipoDeCaracteristica_data)
                caracteristica_instance, _ = Caracteristica.objects.get_or_create(
                    tipoDeCaracteristica=tipoDeCaracteristica_instance, **caracteristica_data)
                inmueble_instance.caracteristicas.add(caracteristica_instance)

        return inmueble_instance


class InmueblePorUsuarioSerializer(serializers.ModelSerializer):
    usuario = serializers.SlugRelatedField(slug_field='username', queryset=Usuario.objects.all())
    inmueble = serializers.SlugRelatedField(slug_field='url', queryset=Inmueble.objects.all())

    class Meta:
        model = InmueblePorUsuario
        fields = '__all__'

    def create(self, validated_data):
        usuario_data = validated_data.pop('usuario')
        inmueble_data = validated_data.pop('inmueble')

        inmueblePorUsuario_instance = InmueblePorUsuario.objects.create(usuario=usuario_data, inmueble=inmueble_data,
                                                                        **validated_data)
        return inmueblePorUsuario_instance
 