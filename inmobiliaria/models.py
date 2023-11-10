from django.db import models
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model

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
    
class Ciudad(models.Model):
    nombre = models.CharField(max_length=255)
    pais = models.ForeignKey(Pais, on_delete=models.CASCADE)   
    
    def __str__(self):
        return self.nombre

class TipoDeInmueble(models.Model):
    nombre = models.CharField(max_length=255)
    
    def __str__(self):
        return self.nombre
    
class Inmueble(models.Model):
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
    sector = models.ForeignKey(Sector, on_delete=models.CASCADE)
    ciudad = models.ForeignKey(Ciudad, on_delete=models.CASCADE)
    tipoDeInmueble = models.ForeignKey(TipoDeInmueble, on_delete = models.CASCADE)
    caracteristicas = models.ManyToManyField('Caracteristica', related_name='caracteristicas')

    def __str__(self):
        return self.nombre

class Usuario(models.Model):
    email = models.CharField(max_length = 30, unique = True)
    password = models.CharField(max_length = 255)
    nombre = models.CharField(max_length=255)
    apellido = models.CharField(max_length=255)
    role = models.CharField(max_length=255)
    edad = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

class InmueblePorUsuario(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    inmueble = models.ForeignKey(Inmueble, on_delete=models.CASCADE)
    clasificacion = models.FloatField()
    
    def __str__(self):
        return f'{self.usuario} - {self.inmueble}'
    

# class UsuarioManager(models.Manager):
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
    

    
