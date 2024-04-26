from django.db import models
from unidecode import unidecode

from .users import *

class Interes(models.Model):
    nombre = models.CharField(max_length=255,unique=True)

    def save(self, *args, **kwargs):
        self.nombre = unidecode(self.nombre).lower()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nombre

class InteresPorUsuario(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    interes = models.ForeignKey(Interes, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.usuario} - {self.interes}'

