from .models import *
from django.contrib import admin

admin.site.register(users.Usuario)
admin.site.register(places.Ciudad)
admin.site.register(places.Departamento)
admin.site.register(places.Pais)
