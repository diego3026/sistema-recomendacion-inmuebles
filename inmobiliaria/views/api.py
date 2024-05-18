from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from inmobiliaria.serializers import *
from inmobiliaria.models import *

class RegisterAPIView(APIView):
    permission_classes = [AllowAny]

    @action(detail=False, methods=['post'])
    def post(self, request):
        serializer = UsuarioRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = Usuario.objects.create_user(
                email=serializer.data['email'],
                nombre=serializer.data['nombre'],
                apellido=serializer.data['apellido'],
                username=serializer.data['username'],
                edad=serializer.data['edad'],
                password=serializer.data['password']
            )
            if user:
                refresh = RefreshToken.for_user(user)
                intereses_serializer = InteresSerializer(user.intereses.all(), many=True)

                user_data = {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'nombre': user.nombre,
                    'apellido': user.apellido,
                    'edad': user.edad,
                    'intereses': intereses_serializer.data
                }
                return Response({
                    'user': user_data,
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginAPIView(APIView):
    permission_classes = [AllowAny]
    queryset = Usuario.objects.all().values('username', 'password')

    @action(detail=True, methods=['post'])
    def post(self, request):
        serializer = UsuarioLoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            try:
                user = Usuario.objects.get(username=username)
                intereses_serializer = InteresSerializer(user.intereses.all(), many=True)
                if user.check_password(password):
                    refresh = RefreshToken.for_user(user)
                    user_data = {
                        'id': user.id,
                        'username': user.username,
                        'email': user.email,
                        'nombre': user.nombre,
                        'apellido': user.apellido,
                        'edad': user.edad,
                        'intereses':intereses_serializer.data
                    }
                    return Response({
                        'user': user_data,
                        'refresh': str(refresh),
                        'access': str(refresh.access_token),
                    }, status=status.HTTP_200_OK)
                else:
                    return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
            except Usuario.DoesNotExist:
                return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
