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
    nombre = NormalizedCharField(max_length=255,allow_null=True)

    class Meta:
        model = Departamento
        fields = '__all__'

class CiudadSerializer(serializers.ModelSerializer):
    departamento = DepartamentoSerializer()
    nombre = NormalizedCharField(max_length=255)

    class Meta:
        model = Ciudad
        fields = '__all__'

    def update(self, instance, validated_data):
        nombre_ciudad_nuevo = validated_data.get('nombre', instance.nombre)

        if nombre_ciudad_nuevo != instance.nombre and Ciudad.objects.filter(nombre=nombre_ciudad_nuevo).exists():
            Ciudad.objects.filter(nombre=nombre_ciudad_nuevo).exclude(id=instance.id).delete()
            instance.nombre = nombre_ciudad_nuevo
        else:
            instance.nombre = nombre_ciudad_nuevo

        departamento_data = validated_data.get('departamento', None)
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