from django.utils.text import slugify
from rest_framework import serializers

class NormalizedCharField(serializers.CharField):
    def to_internal_value(self, data):
        return slugify(data)