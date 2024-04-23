from django.db import IntegrityError
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

class SectorSerializer(serializers.ModelSerializer):
    nombre = NormalizedCharField(max_length=255)

    class Meta:
        model = Sector
        fields = '__all__'