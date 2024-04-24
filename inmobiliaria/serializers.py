from django.db import IntegrityError
from django.utils.text import slugify
from rest_framework import serializers
from rest_framework.response import Response

from .models import *


class NormalizedCharField(serializers.CharField):
    def to_internal_value(self, data):
        return slugify(data)


class PaisSerializer(serializers.ModelSerializer):
    nombre = NormalizedCharField(max_length=255)

    class Meta:
        model = Pais
        fields = '__all__'
        
    def create(self, validated_data):
        try:
            pais_data = validated_data
            pais_name = pais_data['nombre']
            pais_instance = Pais.objects.create(nombre=pais_name)
            return pais_instance
        except IntegrityError:
            raise serializers.ValidationError("Ya existe una pais con el mismo nombre.")


class DepartamentoSerializer(serializers.ModelSerializer):
    pais = PaisSerializer()
    nombre = NormalizedCharField(max_length=255)

    class Meta:
        model = Departamento
        fields = '__all__'

    def create(self, validated_data):
        try:
            pais_data = validated_data.pop('pais')
            pais_name = pais_data['nombre']
            pais_instance = Pais.objects.get_or_create(nombre=pais_name)
            departamento_instance = Departamento.objects.create(pais=pais_instance, **validated_data)
            return departamento_instance
        except IntegrityError:
            raise serializers.ValidationError("Ya existe un departamento con el mismo nombre.")

    def update(self, instance, validated_data):
        nuevo_nombre = validated_data.get('nombre', instance.nombre)

        if nuevo_nombre != instance.nombre and Departamento.objects.filter(nombre=nuevo_nombre).exists():
            Departamento.objects.filter(nombre=nuevo_nombre).exclude(id=instance.id).delete()
            instance.nombre = nuevo_nombre
        else:
            instance.nombre = nuevo_nombre

        pais_data = validated_data.pop('pais', None)
        if pais_data:
            pais_name = pais_data.get('nombre')
            if pais_name:
                pais_instance, _ = Pais.objects.get_or_create(nombre=pais_name)
                instance.pais = pais_instance

        instance.save()
        return instance


class CiudadSerializer(serializers.ModelSerializer):
    departamento = DepartamentoSerializer()
    nombre = NormalizedCharField(max_length=255)

    class Meta:
        model = Ciudad
        fields = '__all__'

    def create(self, validated_data):
        try:
            departamento_data = validated_data.pop('departamento')
            departamento_name = departamento_data['nombre']
            pais_data = departamento_data.pop('pais')
            pais_instance, _ = Pais.objects.get_or_create(**pais_data)
            departamento_instance, _ = Departamento.objects.get_or_create(pais=pais_instance, nombre=departamento_name)
            ciudad_instance = Ciudad.objects.create(departamento=departamento_instance, **validated_data)
            return ciudad_instance
        except IntegrityError:
            raise serializers.ValidationError("Ya existe una ciudad con el mismo nombre.")

    def update(self, instance, validated_data):
        nombre_ciudad_nuevo = validated_data.get('nombre', instance.nombre)

        if nombre_ciudad_nuevo != instance.nombre and Ciudad.objects.filter(nombre=nombre_ciudad_nuevo).exists():
            Ciudad.objects.filter(nombre=nombre_ciudad_nuevo).exclude(id=instance.id).delete()
            instance.nombre = nombre_ciudad_nuevo
        else:
            instance.nombre = nombre_ciudad_nuevo

        departamento_data = validated_data.pop('departamento', None)
        if departamento_data:
            departamento_name = departamento_data.get('nombre')
            if departamento_name:
                pais_data = departamento_data.get('pais')
                if pais_data:
                    pais_instance, _ = Pais.objects.get_or_create(**pais_data)
                    departamento_instance, _ = Departamento.objects.get_or_create(pais=pais_instance,
                                                                                   nombre=departamento_name)
                    instance.departamento = departamento_instance

        instance.save()
        return instance


class SectorSerializer(serializers.ModelSerializer):
    nombre = NormalizedCharField(max_length=255)

    class Meta:
        model = Sector
        fields = '__all__'

    def create(self, validated_data):
        try:
            sector_data = validated_data
            sector_name = sector_data['nombre']
            sector_instance = Sector.objects.create(nombre=sector_name)
            return sector_instance
        except IntegrityError:
            raise serializers.ValidationError("Ya existe una sector con el mismo nombre.")

class TipoDeCaracteristicaSerializer(serializers.ModelSerializer):
    nombre = NormalizedCharField(max_length=255)

    class Meta:
        model = TipoDeCaracteristica
        fields = '__all__'

    def create(self, validated_data):
        try:
            tipoDeCaracteristica_data = validated_data
            tipoDeCaracteristica_name = tipoDeCaracteristica_data['nombre']
            tipoDeCaracteristica_instance = TipoDeCaracteristica.objects.create(nombre=tipoDeCaracteristica_name)
            return tipoDeCaracteristica_instance
        except IntegrityError:
            raise serializers.ValidationError("Ya existe una tipo De Caracteristica con el mismo nombre.")
        
class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id', 'nombre', 'apellido', 'username', 'email', 'edad']


class UsuarioLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=200)
    password = serializers.CharField(max_length=255, style={'input_type': 'password'})


class UsuarioRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['email', 'password', 'nombre', 'apellido', 'username', 'edad']


class CaracteristicaSerializer(serializers.ModelSerializer):
    tipoDeCaracteristica = TipoDeCaracteristicaSerializer()
    nombre = NormalizedCharField(max_length=255)

    class Meta:
        model = Caracteristica
        fields = '__all__'

    def create(self, validated_data):
        tipo_data = validated_data.pop('tipoDeCaracteristica')
        tipo_instance, _ = TipoDeCaracteristica.objects.get_or_create(**tipo_data)
        caracteristica_instance = Caracteristica.objects.create(tipoDeCaracteristica=tipo_instance, **validated_data)
        try:
            tipoDeCaracteristica_data = validated_data.pop('tipoDeCaracteristica')
            tipoDeCaracteristica_name = tipoDeCaracteristica_data['nombre']
            tipoDeCaracteristica_instance = TipoDeCaracteristica.objects.get_or_create(nombre=tipoDeCaracteristica_name)
            caracteristica_instance = Caracteristica.objects.create(tipoDeCaracteristica=tipoDeCaracteristica_instance, **validated_data)
            return caracteristica_instance
        except IntegrityError:
            raise serializers.ValidationError("Ya existe una caracteristica con el mismo nombre.")

    def update(self, instance, validated_data):
        nombre_nuevo = validated_data.get('nombre', instance.nombre)

        if nombre_nuevo != instance.nombre and Caracteristica.objects.filter(nombre=nombre_nuevo).exists():
            Caracteristica.objects.filter(nombre=nombre_nuevo).exclude(id=instance.id).delete()
            instance.nombre = nombre_nuevo
        else:
            instance.nombre = nombre_nuevo

        tipo_data = validated_data.pop('tipoDeCaracteristica', None)
        if tipo_data:
            tipo_instance, _ = TipoDeCaracteristica.objects.get_or_create(**tipo_data)
            instance.tipoDeCaracteristica = tipo_instance
        instance.save()
        return instance


class TipoDeInmuebleSerializer(serializers.ModelSerializer):
    nombre = NormalizedCharField(max_length=255, allow_null=True)

    class Meta:
        model = TipoDeInmueble
        fields = '__all__'
     
    def create(self, validated_data):
        try:
            tipoDeInmueble_data = validated_data
            tipoDeInmueble_name = tipoDeInmueble_data['nombre']
            tipoDeInmueble_instance = TipoDeInmueble.objects.create(nombre=tipoDeInmueble_name)
            return tipoDeInmueble_instance
        except IntegrityError:
            raise serializers.ValidationError("Ya existe una tipo de inmueble con el mismo nombre.")


class InmuebleSerializer(serializers.ModelSerializer):
    sector = SectorSerializer()
    ciudad = CiudadSerializer()
    tipoDeInmueble = TipoDeInmuebleSerializer()
    caracteristicas = CaracteristicaSerializer(many=True)

    class Meta:
        model = Inmueble
        fields = '__all__'

    def update(self, instance, validated_data):
        url_nuevo = validated_data.get('url', instance.nombre)

        if url_nuevo != instance.url and Inmueble.objects.filter(url=url_nuevo).exists():
            Inmueble.objects.filter(url=url_nuevo).exclude(id=instance.id).delete()
            instance.url = url_nuevo
        else:
            instance.url = url_nuevo

        instance.nombre = validated_data.get('nombre', instance.nombre)
        instance.descripcion = validated_data.get('descripcion', instance.descripcion)

        sector_data = validated_data.get('sector')
        if sector_data:
            sector_instance, _ = Sector.objects.get_or_create(**sector_data)
            instance.sector = sector_instance

        ciudad_data = validated_data.get('ciudad')
        if ciudad_data:
            departamento_data = ciudad_data.get('departamento')
            departamento_name = departamento_data.get('nombre')
            pais_data = departamento_data.get('pais')
            if pais_data:
                pais_instance, _ = Pais.objects.get_or_create(**pais_data)
                departamento_instance, _ = Departamento.objects.get_or_create(pais=pais_instance,
                                                                              nombre=departamento_name)
                ciudad_instance, _ = Ciudad.objects.get_or_create(departamento=departamento_instance, **ciudad_data)
                instance.ciudad = ciudad_instance

        tipo_inmueble_data = validated_data.get('tipoDeInmueble')
        if tipo_inmueble_data:
            tipo_inmueble_instance, _ = TipoDeInmueble.objects.get_or_create(**tipo_inmueble_data)
            instance.tipoDeInmueble = tipo_inmueble_instance

        caracteristicas_data = validated_data.get('caracteristicas')
        if caracteristicas_data:
            for caracteristica_data in caracteristicas_data:
                tipoDeCaracteristica_data = caracteristica_data.pop('tipoDeCaracteristica')
                tipoDeCaracteristica_instance, _ = TipoDeCaracteristica.objects.get_or_create(
                    **tipoDeCaracteristica_data)
                caracteristica_instance, _ = Caracteristica.objects.get_or_create(
                    tipoDeCaracteristica=tipoDeCaracteristica_instance, **caracteristica_data)
                instance.caracteristicas.add(caracteristica_instance)

        instance.save()
        return instance

    def create(self, validated_data):
        sector_data = validated_data.pop('sector')
        ciudad_data = validated_data.pop('ciudad', None)
        tipo_inmueble_data = validated_data.pop('tipoDeInmueble')
        caracteristicas_data = validated_data.pop('caracteristicas')

        sector_instance, _ = Sector.objects.get_or_create(**sector_data)

        tipo_inmueble_instance, _ = TipoDeInmueble.objects.get_or_create(**tipo_inmueble_data)

        ciudad_instance = None
        if ciudad_data:
            departamento_data = ciudad_data.pop('departamento', None)
            departamento_name = departamento_data['nombre']
            pais_data = departamento_data.pop('pais', None)
            if pais_data:
                pais_instance, _ = Pais.objects.get_or_create(**pais_data)
            else:
                pais_instance = None
            if departamento_data:
                departamento_instance, _ = Departamento.objects.get_or_create(pais=pais_instance, nombre=departamento_name)
            else:
                departamento_instance = None

            ciudad_name = slugify(ciudad_data['nombre'])
            ciudad_name = ciudad_data['nombre']
            try:
                ciudad_instance = Ciudad.objects.get(nombre=ciudad_name)
            except Ciudad.DoesNotExist:
                ciudad_instance = Ciudad.objects.create(nombre=ciudad_name,departamento=departamento_instance)

        inmueble_instance = Inmueble.objects.create(
            sector=sector_instance,
            ciudad=ciudad_instance,
            tipoDeInmueble=tipo_inmueble_instance,
            **validated_data
        )

        if caracteristicas_data:
            for caracteristica_data in caracteristicas_data:
                tipoDeCaracteristica_data = caracteristica_data.pop('tipoDeCaracteristica')
                tipoDeCaracteristica_instance, _ = TipoDeCaracteristica.objects.get_or_create(**tipoDeCaracteristica_data)
                caracteristica_instance, _ = Caracteristica.objects.get_or_create(tipoDeCaracteristica=tipoDeCaracteristica_instance, **caracteristica_data)
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

    def update(self, instance, validated_data):
        instance.fecha = validated_data.get('fecha', instance.fecha)
        instance.comentario = validated_data.get('comentario', instance.comentario)

        usuario_data = validated_data.get('usuario')
        if usuario_data:
            usuario_instance = Usuario.objects.get(username=usuario_data.get('username'))
            instance.usuario = usuario_instance

        inmueble_data = validated_data.get('inmueble')
        if inmueble_data:
            inmueble_instance = Inmueble.objects.get(url=inmueble_data.get('url'))
            instance.inmueble = inmueble_instance

        instance.save()
        return instance