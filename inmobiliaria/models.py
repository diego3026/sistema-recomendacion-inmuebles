from django.contrib.auth.hashers import make_password
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class Sector(models.Model):
    nombre = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre


class TipoDeCaracteristica(models.Model):
    nombre = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre


class Caracteristica(models.Model):
    nombre = models.CharField(max_length=255)
    tipoDeCaracteristica = models.ForeignKey(TipoDeCaracteristica, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nombre} - {self.idTipoCaracteristica.nombre}"


class Pais(models.Model):
    nombre = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre


class Departamento(models.Model):
    nombre = models.CharField(max_length=255)
    pais = models.ForeignKey(Pais, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre


class Ciudad(models.Model):
    nombre = models.CharField(max_length=255)
    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre


class TipoDeInmueble(models.Model):
    nombre = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre


class Inmueble(models.Model):
    nombre = models.CharField(max_length=150)
    descripcion = models.CharField(max_length=600, null=True)
    estrato = models.CharField(max_length=200, null=True)
    cantidadDeHabitaciones = models.IntegerField(null=True)
    cantidadDeBaños = models.IntegerField(null=True)
    cantidadDeParqueaderos = models.CharField(max_length=200, null=True)
    piso = models.CharField(max_length=150, null=True)
    antiguedad = models.CharField(max_length=200, null=True)
    precioM2 = models.FloatField(null=True)
    url = models.CharField(max_length=200, unique=True)
    areaPrivada = models.CharField(max_length=200, null=True)
    areaConstruida = models.CharField(max_length=200, null=True)
    precioAdministracion = models.IntegerField(null=True)
    precio = models.FloatField(null=True)
    estado = models.CharField(max_length=200, null=True)
    direccion = models.CharField(max_length=300, null=True, blank=True)
    sector = models.ForeignKey(Sector, blank=True, on_delete=models.CASCADE, null=True)
    ciudad = models.ForeignKey(Ciudad, null=True, blank=True, on_delete=models.CASCADE)
    tipoDeInmueble = models.ForeignKey(TipoDeInmueble, on_delete=models.CASCADE, null=True)
    caracteristicas = models.ManyToManyField(Caracteristica, related_name='caracteristicas', blank=True)

    def __str__(self):
        return self.nombre


class UsuarioManager(BaseUserManager):
    def create_user(self, email, nombre, apellido, username, edad, password=None):
        if not email:
            raise ValueError('El email es obligatorio')
        email = self.normalize_email(email)
        user = self.model(email=email, nombre=nombre, apellido=apellido, username=username, edad=edad)
        if password:
            user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, nombre, apellido, username, edad, password=None):
        user = self.create_user(email, nombre, apellido, username, edad, password=password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class Usuario(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    nombre = models.CharField(max_length=255)
    apellido = models.CharField(max_length=255)
    username = models.CharField(max_length=200, unique=True)
    edad = models.PositiveIntegerField()

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UsuarioManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['nombre', 'apellido', 'email', 'edad']

    def __str__(self):
        return f"{self.nombre} {self.apellido}"


class InmueblePorUsuario(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    inmueble = models.ForeignKey(Inmueble, on_delete=models.CASCADE)
    clasificacion = models.FloatField(null=True)

    def __str__(self):
        return f'{self.usuario} - {self.inmueble}'

