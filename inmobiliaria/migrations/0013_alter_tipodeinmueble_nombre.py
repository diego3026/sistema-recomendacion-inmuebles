# Generated by Django 4.2.7 on 2024-04-08 18:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inmobiliaria', '0012_alter_tipodeinmueble_nombre'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tipodeinmueble',
            name='nombre',
            field=models.CharField(blank=True, max_length=255, null=True, unique=True),
        ),
    ]
