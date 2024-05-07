from django.db import IntegrityError
from .normalized_char import *
from inmobiliaria.models import *
from .normalized_char import custom_slugify,NormalizedCharField
from .users import *

class InteresSerializer(serializers.ModelSerializer):
    nombre = NormalizedCharField(max_length=255)

    class Meta:
        model = Interes
        fields = '__all__'

class InteresPorUsuarioSerializer(serializers.ModelSerializer):
    interes = NormalizedCharField(max_length=255)

    class Meta:
        model = InteresPorUsuario
        fields = '__all__'