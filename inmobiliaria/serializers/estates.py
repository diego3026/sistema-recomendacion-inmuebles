from rest_framework import serializers

from .normalized_char import *
from .places import *
from .features import *
from inmobiliaria.models import *


class TipoDeInmuebleSerializer(serializers.ModelSerializer):
    nombre = NormalizedCharField(max_length=255, allow_null=True)

    class Meta:
        model = TipoDeInmueble
        fields = '__all__'
     
    def create(self, validated_data):
        try:
            tipoDeInmueble_data = validated_data
            tipoDeInmueble_name = tipoDeInmueble_data['nombre']
            tipoDeInmueble_instance = TipoDeInmueble.objects.create(nombre=tipoDeInmueble_name)
            return tipoDeInmueble_instance
        except IntegrityError:
            raise serializers.ValidationError("Ya existe una tipo de inmueble con el mismo nombre.")

class InmuebleSerializer(serializers.ModelSerializer):
    sector = SectorSerializer()
    ciudad = CiudadSerializer()
    tipoDeInmueble = TipoDeInmuebleSerializer()
    caracteristicas = CaracteristicaSerializer(many=True)

    class Meta:
        model = Inmueble
        fields = '__all__'

    def update(self, instance, validated_data):
        url_nuevo = validated_data.get('url', instance.nombre)

        if url_nuevo != instance.url and Inmueble.objects.filter(url=url_nuevo).exists():
            Inmueble.objects.filter(url=url_nuevo).exclude(id=instance.id).delete()
            instance.url = url_nuevo
        else:
            instance.url = url_nuevo

        instance.nombre = validated_data.get('nombre', instance.nombre)
        instance.descripcion = validated_data.get('descripcion', instance.descripcion)
        instance.calificacion = validated_data.get('calificacion',instance.calificacion)
        instance.comentarios = validated_data.get('comentarios',instance.comentarios)

        sector_data = validated_data.get('sector')
        if sector_data:
            sector_instance, _ = Sector.objects.get_or_create(**sector_data)
            instance.sector = sector_instance

        ciudad_data = validated_data.get('ciudad')
        if ciudad_data:
            departamento_data = ciudad_data.get('departamento')
            departamento_name = departamento_data.get('nombre')
            pais_data = departamento_data.get('pais')
            if pais_data:
                pais_instance, _ = Pais.objects.get_or_create(**pais_data)
                departamento_instance, _ = Departamento.objects.get_or_create(pais=pais_instance,
                                                                              nombre=departamento_name)
                ciudad_instance, _ = Ciudad.objects.get_or_create(departamento=departamento_instance, **ciudad_data)
                instance.ciudad = ciudad_instance

        tipo_inmueble_data = validated_data.get('tipoDeInmueble')
        if tipo_inmueble_data:
            tipo_inmueble_instance, _ = TipoDeInmueble.objects.get_or_create(**tipo_inmueble_data)
            instance.tipoDeInmueble = tipo_inmueble_instance

        caracteristicas_data = validated_data.get('caracteristicas')
        if caracteristicas_data:
            for caracteristica_data in caracteristicas_data:
                tipoDeCaracteristica_data = caracteristica_data.pop('tipoDeCaracteristica')
                tipoDeCaracteristica_instance, _ = TipoDeCaracteristica.objects.get_or_create(
                    **tipoDeCaracteristica_data)
                caracteristica_instance, _ = Caracteristica.objects.get_or_create(
                    tipoDeCaracteristica=tipoDeCaracteristica_instance, **caracteristica_data)
                instance.caracteristicas.add(caracteristica_instance)

        instance.save()
        return instance

    def create(self, validated_data):
        sector_data = validated_data.pop('sector')
        ciudad_data = validated_data.pop('ciudad', None)
        tipo_inmueble_data = validated_data.pop('tipoDeInmueble')
        caracteristicas_data = validated_data.pop('caracteristicas')

        sector_instance, _ = Sector.objects.get_or_create(**sector_data)

        tipo_inmueble_instance, _ = TipoDeInmueble.objects.get_or_create(**tipo_inmueble_data)

        ciudad_instance = None
        if ciudad_data:
            departamento_data = ciudad_data.pop('departamento', None)
            departamento_name = departamento_data['nombre']
            pais_data = departamento_data.pop('pais', None)
            if pais_data:
                pais_instance, _ = Pais.objects.get_or_create(**pais_data)
            else:
                pais_instance = None
            if departamento_data:
                departamento_instance, _ = Departamento.objects.get_or_create(pais=pais_instance, nombre=departamento_name)
            else:
                departamento_instance = None

            ciudad_name = slugify(ciudad_data['nombre'])
            ciudad_name = ciudad_data['nombre']
            try:
                ciudad_instance = Ciudad.objects.get(nombre=ciudad_name)
            except Ciudad.DoesNotExist:
                ciudad_instance = Ciudad.objects.create(nombre=ciudad_name,departamento=departamento_instance)

        inmueble_instance = Inmueble.objects.create(
            sector=sector_instance,
            ciudad=ciudad_instance,
            tipoDeInmueble=tipo_inmueble_instance,
            **validated_data
        )

        if caracteristicas_data:
            for caracteristica_data in caracteristicas_data:
                tipoDeCaracteristica_data = caracteristica_data.pop('tipoDeCaracteristica')
                tipoDeCaracteristica_instance, _ = TipoDeCaracteristica.objects.get_or_create(**tipoDeCaracteristica_data)
                caracteristica_instance, _ = Caracteristica.objects.get_or_create(tipoDeCaracteristica=tipoDeCaracteristica_instance, **caracteristica_data)
                inmueble_instance.caracteristicas.add(caracteristica_instance)

        return inmueble_instance

class InmueblePorUsuarioSerializer(serializers.ModelSerializer):
    usuario = serializers.SlugRelatedField(slug_field='username', queryset=Usuario.objects.all())
    inmueble = serializers.SlugRelatedField(slug_field='url', queryset=Inmueble.objects.all())

    class Meta:
        model = InmueblePorUsuario
        fields = '__all__'

    def create(self, validated_data):
        usuario_data = validated_data.pop('usuario')
        inmueble_data = validated_data.pop('inmueble')

        inmueblePorUsuario_instance = InmueblePorUsuario.objects.create(usuario=usuario_data, inmueble=inmueble_data,
                                                                        **validated_data)
        return inmueblePorUsuario_instance

    def update(self, instance, validated_data):
        instance.clasificacion = validated_data.get('clasificacion', instance.clasificacion)
        instance.numeroDeClicks = validated_data.get('numeroDeClicks', instance.numeroDeClicks)
        instance.favorito = validated_data.get('favorito',instance.favorito)

        usuario_data = validated_data.get('usuario')
        if usuario_data:
            usuario_instance = Usuario.objects.get(username=usuario_data.get('username'))
            instance.usuario = usuario_instance

        inmueble_data = validated_data.get('inmueble')
        if inmueble_data:
            inmueble_instance = Inmueble.objects.get(url=inmueble_data.get('url'))
            instance.inmueble = inmueble_instance

        instance.save()
        return instance
