# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-03-01 11:30
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vi_peli', '0019_auto_20180219_1803'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lista_pelis',
            name='idFicha',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='miid', to='vi_peli.Pelicula'),
        ),
    ]
