from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from inmobiliaria.permissions import IsSuperUser
from inmobiliaria.serializers import *
from inmobiliaria.models import *

class InteresViewSet(viewsets.ModelViewSet):
    queryset = Interes.objects.all()
    serializer_class = InteresSerializer

    # Agregar acción delete
    @action(detail=True, methods=['delete'],permission_classes=[IsSuperUser])
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({'status': 'interest deleted'}, status=status.HTTP_204_NO_CONTENT)
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        interes_data = serializer.validated_data['nombre']
        try:
            interes_instance = Interes.objects.create(nombre=interes_data)
        except IntegrityError:
            return Response({"Ya existe un interes con este nombre"}, status=status.HTTP_302_FOUND)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

class InteresPorUsuarioViewSet(viewsets.ModelViewSet):
    queryset = InteresPorUsuario.objects.all()
    serializer_class = InteresPorUsuarioSerializer

    @action(detail=True, methods=['delete'],permission_classes=[IsSuperUser])
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({'status': 'interes por usuario deleted'}, status=status.HTTP_204_NO_CONTENT)
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        usuario_data = serializer.validated_data['usuario']
        interes_data = serializer.validated_data['interes']

        usuario_instance = Usuario.objects.get(username=usuario_data)
        interes_instance, _ = Interes.objects.get_or_create(nombre=interes_data)

        try:
            interes_usuario_instance = InteresPorUsuario.objects.create(
                usuario=usuario_instance,
                interes=interes_instance,
            )
        except IntegrityError:
            return Response({"Ya existe un usuario con este interes"}, status=status.HTTP_302_FOUND)

        return Response(serializer.data, status=status.HTTP_201_CREATED)