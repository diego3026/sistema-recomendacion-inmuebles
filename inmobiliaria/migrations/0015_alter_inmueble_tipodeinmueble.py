# Generated by Django 4.2.7 on 2024-04-08 18:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inmobiliaria', '0014_alter_inmueble_tipodeinmueble'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inmueble',
            name='tipoDeInmueble',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='inmobiliaria.tipodeinmueble'),
        ),
    ]
