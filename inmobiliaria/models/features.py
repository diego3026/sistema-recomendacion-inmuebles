from django.contrib.auth.hashers import make_password
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from unidecode import unidecode


class TipoDeCaracteristica(models.Model):
    nombre = models.CharField(max_length=255,unique=True)

    def save(self, *args, **kwargs):
        self.nombre = unidecode(self.nombre).lower()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nombre
    
class Caracteristica(models.Model):
    nombre = models.CharField(max_length=255,unique=True)
    tipoDeCaracteristica = models.ForeignKey(TipoDeCaracteristica, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.nombre = unidecode(self.nombre).lower()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nombre} - {self.idTipoCaracteristica.nombre}"