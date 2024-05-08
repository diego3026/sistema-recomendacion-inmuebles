from django.db import models
from unidecode import unidecode

class Interes(models.Model):
    nombre = models.CharField(max_length=255,unique=True)

    def save(self, *args, **kwargs):
        self.nombre = unidecode(self.nombre).lower()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nombre