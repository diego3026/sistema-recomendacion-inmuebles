from rest_framework import serializers

from .normalized_char import *
from inmobiliaria.models import *

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
