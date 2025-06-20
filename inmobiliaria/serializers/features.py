from django.db import IntegrityError
from rest_framework import serializers
from .normalized_char import *
from inmobiliaria.models import *

class TipoDeCaracteristicaSerializer(serializers.ModelSerializer):
    nombre = NormalizedCharField(max_length=255)

    class Meta:
        model = TipoDeCaracteristica
        fields = '__all__'


class CaracteristicaSerializer(serializers.ModelSerializer):
    tipoDeCaracteristica = TipoDeCaracteristicaSerializer()
    nombre = NormalizedCharField(max_length=255)

    class Meta:
        model = Caracteristica
        fields = '__all__'

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
