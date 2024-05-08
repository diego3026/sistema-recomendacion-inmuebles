from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from inmobiliaria.permissions import IsSuperUser
from inmobiliaria.serializers import *
from inmobiliaria.models import *

class TipoDeInmuebleViewSet(viewsets.ModelViewSet):
    queryset = TipoDeInmueble.objects.all()
    serializer_class = TipoDeInmuebleSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        tipo_inmueble_data = serializer.validated_data['nombre']

        try:
            tipo_inmueble_instance = TipoDeInmueble.objects.create(nombre=tipo_inmueble_data)
        except IntegrityError:
            return Response({"Ya existe un tipo de inmueble con este nombre"}, status=status.HTTP_302_FOUND)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # Agregar acción delete
    @action(detail=True, methods=['delete'],permission_classes=[IsSuperUser])
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({'status': 'tipo de inmueble deleted'}, status=status.HTTP_204_NO_CONTENT)
    
    permission_classes = [IsSuperUser]
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

class InmuebleViewSet(viewsets.ModelViewSet):
    queryset = Inmueble.objects.all()
    serializer_class = InmuebleSerializer

    @action(detail=True, methods=['delete'],permission_classes=[IsSuperUser])
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({'status': 'inmueble deleted'}, status=status.HTTP_204_NO_CONTENT)
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    permission_classes = [IsSuperUser]
    def create(self, request, *args, **kwargs):
        if isinstance(request.data, list):
            serializer = self.get_serializer(data=request.data,many=True)
        else:
            serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.create(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class InmueblePorUsuarioViewSet(viewsets.ModelViewSet):
    queryset = InmueblePorUsuario.objects.all()
    serializer_class = InmueblePorUsuarioSerializer

    # Agregar acción delete
    @action(detail=True, methods=['delete'],permission_classes=[IsSuperUser])
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({'status': 'inmueble por usuario deleted'}, status=status.HTTP_204_NO_CONTENT)
    
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

        inmueble_data = serializer.validated_data['inmueble']
        usuario_data = serializer.validated_data['usuario']

        usuario_instance = Usuario.objects.get(username=usuario_data)
        inmueble_instance = Inmueble.objects.get(url=inmueble_data)

        try:
            inmueble_usuario_instance = InmueblePorUsuario.objects.create(usuario=usuario_instance,
                                                                    inmueble=inmueble_instance)
        except IntegrityError:
            return Response({"Ya existe una usuario para este inmueble con este nombre"}, status=status.HTTP_302_FOUND)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
