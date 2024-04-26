from django.db import IntegrityError
from rest_framework import serializers
from .normalized_char import *
from inmobiliaria.models import *

class InteresSerializer(serializers.ModelSerializer):
    nombre = NormalizedCharField(max_length=255)

    class Meta:
        model = Interes
        fields = '__all__'

    def create(self, validated_data):
        try:
            interes_data = validated_data
            interes_name = interes_data['nombre']
            interes_instance = Interes.objects.create(nombre=interes_name)
            return interes_instance
        except IntegrityError:
            raise serializers.ValidationError("Ya existe un interes con el mismo nombre.")

class InteresPorUsuarioSerializer(serializers.ModelSerializer):
    usuario = serializers.SlugRelatedField(slug_field='username', queryset=Usuario.objects.all())
    interes = serializers.SlugRelatedField(slug_field='interes', queryset=Interes.objects.all())

    class Meta:
        model = InteresPorUsuario
        fields = '__all__'

    def create(self, validated_data):
        usuario_data = validated_data.pop('usuario')
        interes_data = validated_data.pop('interes')

        interesPorUsuario_instance = InteresPorUsuario.objects.create(usuario=usuario_data, interes=interes_data,
                                                                        **validated_data)
        return interesPorUsuario_instance