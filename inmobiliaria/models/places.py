from django.db import models
from unidecode import unidecode

class Sector(models.Model):
    nombre = models.CharField(max_length=255,unique=True)

    def save(self, *args, **kwargs):
        self.nombre = unidecode(self.nombre).lower()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nombre
    
class Pais(models.Model):
    nombre = models.CharField(max_length=255,unique=True)

    def __str__(self):
        return self.nombre

    def save(self, *args, **kwargs):
        self.nombre = unidecode(self.nombre).lower()
        super().save(*args, **kwargs)


class Departamento(models.Model):
    nombre = models.CharField(max_length=255,null=True,blank=True,unique=True)
    pais = models.ForeignKey(Pais, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.nombre = unidecode(self.nombre).lower()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nombre


class Ciudad(models.Model):
    nombre = models.CharField(max_length=255,null=True,blank=True,unique=True)
    departamento = models.ForeignKey(Departamento,on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.nombre = unidecode(self.nombre).lower()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nombre