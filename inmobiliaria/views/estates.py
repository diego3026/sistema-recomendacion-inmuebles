from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from inmobiliaria.permissions import IsSuperUser
from inmobiliaria.serializers import *
from inmobiliaria.models import *

class TipoDeInmuebleViewSet(viewsets.ModelViewSet):
    queryset = TipoDeInmueble.objects.all()
    serializer_class = TipoDeInmuebleSerializer

    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

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
    

    def update(self, request, *args, **kwargs):
        permission_classes = [IsSuperUser]
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

class InmuebleViewSet(viewsets.ModelViewSet):
    queryset = Inmueble.objects.all()
    serializer_class = InmuebleSerializer

    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @action(detail=True, methods=['delete'],permission_classes=[IsSuperUser])
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({'status': 'inmueble deleted'}, status=status.HTTP_204_NO_CONTENT)
    
    def update(self, request, *args, **kwargs):
        permission_classes = [IsSuperUser]
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


    def create(self, request, *args, **kwargs):
        permission_classes = [IsSuperUser]
        if isinstance(request.data, list):
            #serializer = self.get_serializer(data=request.data,many=True)
            serialized_data = []
            errors = []#2095
            for data in request.data:
                serializer = self.get_serializer(data=data)
                if serializer.is_valid():
                    try:
                        instance = serializer.create(serializer.data)
                        serialized_data.append(instance)
                    except ValidationError as e:
                        errors.append({'error': str(e), 'data': data})
                else:
                    errors.append({'error': serializer.errors, 'data': data})

            if errors:
                return Response(errors, status=status.HTTP_400_BAD_REQUEST)

            return Response(serialized_data, status=status.HTTP_200_OK)
 
        else:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.create(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

class InmueblePorUsuarioViewSet(viewsets.ModelViewSet):
    queryset = InmueblePorUsuario.objects.all()
    serializer_class = InmueblePorUsuarioSerializer

    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @action(detail=True, methods=['delete'],permission_classes=[IsSuperUser])
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({'status': 'inmueble por usuario deleted'}, status=status.HTTP_204_NO_CONTENT)
    

    def update(self, request, *args, **kwargs):
        permission_classes = [IsSuperUser]
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


        try:
            inmueble_usuario_instance = InmueblePorUsuario.objects.create(usuario=usuario_instance,
                                                                    inmueble=inmueble_instance)
        except IntegrityError:
            return Response({"Ya existe una usuario para este inmueble con este nombre"}, status=status.HTTP_302_FOUND)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
