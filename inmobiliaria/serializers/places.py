from django.db import IntegrityError
from rest_framework import serializers

from .normalized_char import *
from inmobiliaria.models import *

class PaisSerializer(serializers.ModelSerializer):
    nombre = NormalizedCharField(max_length=255)

    class Meta:
        model = Pais
        fields = '__all__'


class DepartamentoSerializer(serializers.ModelSerializer):
    pais = PaisSerializer()
    nombre = NormalizedCharField(max_length=255)

    class Meta:
        model = Departamento
        fields = '__all__'

    def create(self, validated_data):
        pais_data = validated_data.pop('pais')
        pais_name = pais_data['nombre']
        pais_instance, _ = Pais.objects.get_or_create(nombre=pais_name)
        departamento_instance = Departamento.objects.create(pais=pais_instance, **validated_data)
        return departamento_instance

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

