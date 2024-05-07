from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from inmobiliaria.permissions import IsSuperUser
from inmobiliaria.serializers import *
from inmobiliaria.models import *
import pdb;

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

        sector_data = serializer.validated_data.get('sector')
        ciudad_data = serializer.validated_data.get('ciudad')
        tipo_inmueble_data = serializer.validated_data.get('tipoDeInmueble')
        caracteristicas_data = serializer.validated_data.get('caracteristicas')

        if sector_data:
            sector_instance, _ = Sector.objects.get_or_create(nombre=sector_data['nombre'])

        #pdb.set_trace()

        try:
            tipo_inmueble_instance = TipoDeInmueble.objects.get(nombre=tipo_inmueble_data['nombre'])
        except TipoDeInmueble.DoesNotExist:
            tipo_inmueble_instance = TipoDeInmueble.objects.create(nombre=tipo_inmueble_data['nombre'])

        ciudad_instance = None
        if ciudad_data:
            ciudad_name = ciudad_data.get('nombre', None)

            try:
                ciudad_instance = Ciudad.objects.get(nombre=ciudad_name)
            except Ciudad.DoesNotExist:
                departamento_data = ciudad_data.get('departamento', None)
                departamento_name = None

                if departamento_data:
                    departamento_name = departamento_data.get('nombre', None)

                ciudad_instance = Ciudad.objects.create(nombre=ciudad_name)

                if departamento_name is not None:
                    try:
                        departamento_instance = Departamento.objects.get(nombre=departamento_name)
                    except Departamento.DoesNotExist:
                        pais_data = departamento_data.get('pais', None)
                        pais_name = pais_data.get('nombre', None)
                        if pais_data:
                            pais_instance = Pais.objects.get(nombre=pais_name)
                        departamento_instance = Departamento.objects.create(nombre=departamento_name,pais=pais_instance)


                    ciudad_instance.departamento = departamento_instance
                    ciudad_instance.save()

        try:
            inmueble_instance, created = Inmueble.objects.get_or_create(
                ciudad=ciudad_instance,
                sector=sector_instance,
                tipoDeInmueble=tipo_inmueble_instance,
                defaults=serializer.validated_data
            )

        except IntegrityError:
            return Response({"Ya existe un inmueble con esta url"}, status=status.HTTP_302_FOUND)


        if caracteristicas_data:
            for caracteristica_data in caracteristicas_data:
                tipoDeCaracteristica_data = caracteristica_data.get('tipoDeCaracteristica')
                tipoDeCaracteristica_instance, _ = TipoDeCaracteristica.objects.get_or_create(nombre=tipoDeCaracteristica_data['nombre'])
                try:
                    caracteristica_instance = Caracteristica.objects.get(nombre=caracteristica_data['nombre'])
                except Caracteristica.DoesNotExist:
                    caracteristica_instance = Caracteristica.objects.create(nombre=caracteristica_data['nombre'], tipoDeCaracteristica=tipoDeCaracteristica_instance)

                inmueble_instance.caracteristicas.add(caracteristica_instance)

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

        inmueble_data = serializer.validated_data['url']
        usuario_data = serializer.validated_data['username']

        usuario_instance = Usuario.objects.get(username=usuario_data)
        inmueble_instance = Inmueble.objects.get(url=inmueble_data)

        try:
            inmueble_usuario_instance = InmueblePorUsuario.objects.create(usuario=usuario_instance,
                                                                    inmueble=inmueble_instance)
        except IntegrityError:
            return Response({"Ya existe una usuario para este inmueble con este nombre"}, status=status.HTTP_302_FOUND)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
