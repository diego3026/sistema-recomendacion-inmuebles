from django.contrib.auth.hashers import make_password
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from unidecode import unidecode

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
