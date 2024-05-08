from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from inmobiliaria.permissions import IsSuperUser
from inmobiliaria.serializers import *
from inmobiliaria.models import *

class TipoDeCaracteristicaViewSet(viewsets.ModelViewSet):
    queryset = TipoDeCaracteristica.objects.all()
    serializer_class = TipoDeCaracteristicaSerializer

    @action(detail=True, methods=['delete'],permission_classes=[IsSuperUser])
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({'status': 'tipo de característica deleted'}, status=status.HTTP_204_NO_CONTENT)
    
    permission_classes = [IsSuperUser]
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        tipo_data = serializer.validated_data['nombre']

        try:
            tipo_instance = TipoDeCaracteristica.objects.create(nombre=tipo_data)
        except IntegrityError:
            return Response({"Ya existe un tipo de caracteristica con este nombre"}, status=status.HTTP_302_FOUND)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
class CaracteristicaViewSet(viewsets.ModelViewSet):
    queryset = Caracteristica.objects.all()
    serializer_class = CaracteristicaSerializer

    # Agregar acción delete
    @action(detail=True, methods=['delete'],permission_classes=[IsSuperUser])
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({'status': 'caracteristica deleted'}, status=status.HTTP_204_NO_CONTENT)

    permission_classes = [IsSuperUser]
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        caracteristica_data = serializer.validated_data['nombre']
        tipo_data = serializer.validated_data['tipoDeCaracteristica']
        tipo_instance, _ = TipoDeCaracteristica.objects.get_or_create(nombre=tipo_data['nombre'])
        try:
            caracteristica_instance = Caracteristica.objects.create(nombre=caracteristica_data,
                                                                    tipoDeCaracteristica=tipo_instance)
        except IntegrityError:
            return Response({"Ya existe una caracteristica con este nombre"}, status=status.HTTP_302_FOUND)

        return Response(serializer.data, status=status.HTTP_201_CREATED)