# Generated by Django 4.2.7 on 2024-04-08 18:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inmobiliaria', '0011_alter_tipodeinmueble_nombre'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tipodeinmueble',
            name='nombre',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
