from rest_framework import viewsets, status, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import *


class PaisViewSet(viewsets.ModelViewSet):
    queryset = Pais.objects.all()
    serializer_class = PaisSerializer

    # Agregar acción delete
    @action(detail=True, methods=['delete'])
    def delete_pais(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({'status': 'pais deleted'}, status=status.HTTP_204_NO_CONTENT)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

class CiudadViewSet(viewsets.ModelViewSet):
    queryset = Ciudad.objects.all()
    serializer_class = CiudadSerializer

    # Agregar acción delete
    @action(detail=True, methods=['delete'])
    def delete_ciudad(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({'status': 'ciudad deleted'}, status=status.HTTP_204_NO_CONTENT)
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


class SectorViewSet(viewsets.ModelViewSet):
    queryset = Sector.objects.all()
    serializer_class = SectorSerializer

    @action(detail=True, methods=['delete'])
    def delete_sector(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({'status': 'sector deleted'}, status=status.HTTP_204_NO_CONTENT)
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


class TipoDeCaracteristicaViewSet(viewsets.ModelViewSet):
    queryset = TipoDeCaracteristica.objects.all()
    serializer_class = TipoDeCaracteristicaSerializer

    # Agregar acción delete
    @action(detail=True, methods=['delete'])
    def delete_tipo_de_caracteristica(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({'status': 'tipo de característica deleted'}, status=status.HTTP_204_NO_CONTENT)
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

    # Agregar acción delete
    @action(detail=True, methods=['delete'])
    def delete_usuario(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({'status': 'usuario deleted'}, status=status.HTTP_204_NO_CONTENT)
    
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
    @action(detail=True, methods=['delete'])
    def delete_caracteristica(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({'status': 'caracteristica deleted'}, status=status.HTTP_204_NO_CONTENT)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

class TipoDeInmuebleViewSet(viewsets.ModelViewSet):
    queryset = TipoDeInmueble.objects.all()
    serializer_class = TipoDeInmuebleSerializer

    # Agregar acción delete
    @action(detail=True, methods=['delete'])
    def delete_tipo_de_inmueble(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({'status': 'tipo de inmueble deleted'}, status=status.HTTP_204_NO_CONTENT)
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


class InmuebleViewSet(viewsets.ModelViewSet):
    queryset = Inmueble.objects.all()
    serializer_class = InmuebleSerializer

    # Agregar acción delete
    @action(detail=True, methods=['delete'])
    def delete_inmueble(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({'status': 'inmueble deleted'}, status=status.HTTP_204_NO_CONTENT)
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


class InmueblePorUsuarioViewSet(viewsets.ModelViewSet):
    queryset = InmueblePorUsuario.objects.all()
    serializer_class = InmueblePorUsuarioSerializer

    # Agregar acción delete
    @action(detail=True, methods=['delete'])
    def delete_inmueble_por_usuario(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({'status': 'inmueble por usuario deleted'}, status=status.HTTP_204_NO_CONTENT)
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
