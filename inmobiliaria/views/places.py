from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from inmobiliaria.permissions import IsSuperUser
from inmobiliaria.serializers import *
from inmobiliaria.models import *

class PaisViewSet(viewsets.ModelViewSet):
    queryset = Pais.objects.all()
    serializer_class = PaisSerializer

    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @action(detail=True, methods=['delete'],permission_classes=[IsSuperUser])
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(data={'status': 'pais deleted'}, status=status.HTTP_204_NO_CONTENT)

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
        pais_data = serializer.validated_data['nombre']
        try:
            pais_instance = Pais.objects.create(nombre=pais_data)
        except IntegrityError:
            return Response({"Ya existe un pais con este nombre"}, status=status.HTTP_302_FOUND)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

class CiudadViewSet(viewsets.ModelViewSet):
    queryset = Ciudad.objects.all()
    serializer_class = CiudadSerializer

    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @action(detail=True, methods=['delete'],permission_classes=[IsSuperUser])
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({'status': 'ciudad deleted'}, status=status.HTTP_204_NO_CONTENT)

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

        ciudad_data = serializer.validated_data['nombre']

        departamento_data = serializer.validated_data['departamento']
        pais_data = departamento_data['pais']
        pais_instance, _ = Pais.objects.get_or_create(nombre=pais_data['nombre'])

        departamento_instance, _ = Departamento.objects.get_or_create(nombre=departamento_data['nombre'],
                                                                      pais=pais_instance)

        try:
            ciudad_instance = Ciudad.objects.create(departamento=departamento_instance, nombre=ciudad_data)
        except IntegrityError:
            return Response({"Ya existe una ciudad con este nombre"}, status=status.HTTP_302_FOUND)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

class SectorViewSet(viewsets.ModelViewSet):
    queryset = Sector.objects.all()
    serializer_class = SectorSerializer

    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @action(detail=True, methods=['delete'],permission_classes=[IsSuperUser])
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({'status': 'sector deleted'}, status=status.HTTP_204_NO_CONTENT)

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
        sector_data = serializer.validated_data['nombre']

        if sector_data is None:
            sector_instance = None
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        try:
            sector_instance = Sector.objects.create(nombre=sector_data)
        except IntegrityError:
            return Response({"Ya existe un sector con este nombre"}, status=status.HTTP_302_FOUND)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
