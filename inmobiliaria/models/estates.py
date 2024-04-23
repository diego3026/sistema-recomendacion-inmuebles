from django.db import models
from unidecode import unidecode

from .places import *
from .features import *
from .users import *

class TipoDeInmueble(models.Model):
    nombre = models.CharField(max_length=255, unique=True, null=True, blank=True)

    def __str__(self):
        return self.nombre

    def save(self, *args, **kwargs):
        self.nombre = unidecode(self.nombre).lower()
        super().save(*args, **kwargs)

class Inmueble(models.Model):
    nombre = models.CharField(max_length=150)
    descripcion = models.CharField(max_length=600, null=True)
    estrato = models.CharField(max_length=200, null=True)
    cantidadDeHabitaciones = models.IntegerField(null=True)
    cantidadDeBaños = models.IntegerField(null=True)
    cantidadDeParqueaderos = models.CharField(max_length=200, null=True)
    piso = models.CharField(max_length=150, null=True)
    antiguedad = models.CharField(max_length=200, null=True)
    precioM2 = models.CharField(max_length=200,null=True)
    url = models.CharField(max_length=200, unique=True)
    areaPrivada = models.CharField(max_length=200, null=True)
    areaConstruida = models.CharField(max_length=200, null=True)
    precioAdministracion = models.CharField(max_length=200,null=True)
    precio = models.FloatField(null=True)
    estado = models.CharField(max_length=200, null=True)
    direccion = models.CharField(max_length=300, null=True, blank=True)
    sector = models.ForeignKey(Sector, blank=True, on_delete=models.CASCADE, null=True)
    ciudad = models.ForeignKey(Ciudad, null=True, blank=True, on_delete=models.CASCADE)
    tipoDeInmueble = models.ForeignKey(TipoDeInmueble, on_delete=models.CASCADE,null=True, blank=True)
    caracteristicas = models.ManyToManyField(Caracteristica, related_name='caracteristicas', blank=True)

    def __str__(self):
        return self.nombre

class InmueblePorUsuario(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    inmueble = models.ForeignKey(Inmueble, on_delete=models.CASCADE)
    clasificacion = models.FloatField(null=True)

    def __str__(self):
        return f'{self.usuario} - {self.inmueble}'

