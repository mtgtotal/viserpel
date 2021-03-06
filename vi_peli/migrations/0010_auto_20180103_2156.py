# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-01-03 20:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vi_peli', '0009_auto_20180102_0126'),
    ]

    operations = [
        migrations.AddField(
            model_name='lista_pelis',
            name='sinopsis',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='pelicula',
            name='img',
            field=models.ImageField(null=True, upload_to='Imagenes', verbose_name='Imagen'),
        ),
        migrations.AddField(
            model_name='pelicula',
            name='sinopsis_es',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='lista_pelis',
            name='enlace',
            field=models.TextField(db_tablespace='indexes', unique=True),
        ),
        migrations.AlterField(
            model_name='lista_pelis',
            name='torrent',
            field=models.TextField(db_tablespace='indexes', unique=True),
        ),
    ]
