from rest_framework import serializers
import unicodedata
import re

def custom_slugify(text):
    # Eliminar tildes
    text = ''.join((c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn' or c == 'ñ'))
    
    # Convertir la cadena a minúsculas
    text = text.lower()
    
    # Reemplazar espacios y otros caracteres especiales por guiones medios
    text = re.sub(r'[-\s]+', '-', text)
    
    # Normalizar la cadena eliminando caracteres no alfanuméricos o guiones medios
    text = re.sub(r'[^\w\s-]', '', text)
    
    # Eliminar guiones medios duplicados
    text = re.sub(r'[-]+', '-', text)
    
    return text

class NormalizedCharField(serializers.CharField):
    def to_internal_value(self, data):
        return custom_slugify(data)