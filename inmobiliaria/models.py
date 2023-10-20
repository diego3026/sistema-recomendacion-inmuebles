from django.db import models
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model

class Sector(models.Model):
    idSector = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)

    def __str__(self):
        return 

class TipoDeCaracteristica(models.Model):
    idtipoDeCaracteristicas = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    
class Usuario(models.Model):
    idUsuario = models.BigAutoField(primary_key=True)
    email = models.CharField(max_length = 30, unique = True)
    password = models.CharField(max_length = 255)
    nombre = models.CharField(max_length=255)
    apellido = models.CharField(max_length=255)
    edad = models.PositiveIntegerField()

    def save(self, **kwargs):
        clave = 'mMUj0DrIK6vgtdIYepkIxN'
        self.password = make_password(self.password, clave)
        super().save(**kwargs)

class Caracteristica(models.Model):
    idCaracteristicas = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    idTipoCaracteristica = models.ForeignKey(TipoDeCaracteristica, on_delete=models.CASCADE)

class Pais(models.Model):
    idPais = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    
class Ciudad(models.Model):
    idCiudad = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    idPais = models.ForeignKey(Pais, on_delete=models.CASCADE)   

class TipoDeInmueble(models.Model):
    idTipoDeInmueble = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    
class Inmueble(models.Model):
    idInmueble = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=100)
    estrato = models.IntegerField()
    cantidadDeHabitantes = models.IntegerField()
    cantidadDeBaños = models.IntegerField()
    cantidadDeParqueaderos = models.IntegerField()
    piso = models.IntegerField()
    antiguedad = models.IntegerField()
    estado = models.CharField(max_length=50)
    url = models.CharField(max_length=100)
    areaPrivada = models.IntegerField()
    areaConstruida = models.IntegerField()
    precioAdministracion = models.IntegerField()
    precio = models.IntegerField()
    direccion = models.CharField(max_length=300)
    idSector = models.ForeignKey(Sector, on_delete=models.CASCADE)
    idCiudad = models.ForeignKey(Ciudad, on_delete=models.CASCADE)
    idTipoDeInmueble = models.ForeignKey(TipoDeInmueble, on_delete = models.CASCADE)
    caracteristicas = models.ManyToManyField(Caracteristica)

    def __str__(self):
        return self.nombre

class InmueblePorUsuario(models.Model):
    idUsuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    idInmueble = models.ForeignKey(Inmueble, on_delete=models.CASCADE)
    clasificacion = models.FloatField()
    

# # class UsuarioManager(models.Manager):
#     @classmethod
#     def autenticar_usuario(cls, email, password):
#         try:
#             # Buscar un usuario por correo y contraseña en la base de datos
#             usuario = get_user_model().objects.get(email=email, password=password)
#             return usuario
#         except get_user_model().DoesNotExist:
#             return None
    
#     @classmethod
#     def registrar_usuario(usuario_data):
#         try:
#             # Crea un nuevo objeto Usuario y guárdalo en la base de datos
#             usuario = Usuario(
#                 email=usuario_data['email'],
#                 password=usuario_data['password'],
#                 nombre=usuario_data['nombre'],
#                 apellido=usuario_data['apellido'],
#                 edad=usuario_data['edad'],
#             )
#             usuario.save()
#             return usuario
#         except Exception as e:
#             # Manejar cualquier excepción que pueda ocurrir al guardar el usuario
#             # Por ejemplo, manejar la excepción de violación de restricción única en el campo 'email'
#             return None
    
#     @classmethod
#     def ver_usuarios(cls):
#         # Recuperar todos los usuarios desde la base de datos utilizando el ORM de Django
#         usuarios = cls.get_queryset().all()
#         return usuarios
    
