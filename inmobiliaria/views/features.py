from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from inmobiliaria.permissions import IsSuperUser
from inmobiliaria.models import *
from inmobiliaria.serializers import *


class TipoDeCaracteristicaViewSet(viewsets.ModelViewSet):
    queryset = TipoDeCaracteristica.objects.all()
    serializer_class = TipoDeCaracteristicaSerializer

    # Agregar acción delete
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

