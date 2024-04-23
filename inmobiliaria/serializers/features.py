from inmobiliaria.models import *
from .normalized_char import *

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

    def create(self, validated_data):
        tipo_data = validated_data.pop('tipoDeCaracteristica')
        tipo_instance, _ = TipoDeCaracteristica.objects.get_or_create(**tipo_data)
        caracteristica_instance = Caracteristica.objects.create(tipoDeCaracteristica=tipo_instance, **validated_data)
        return caracteristica_instance
