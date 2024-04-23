from inmobiliaria.models import *
from .normalized_char import *

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