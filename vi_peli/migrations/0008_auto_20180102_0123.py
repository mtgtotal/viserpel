# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-01-02 00:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vi_peli', '0007_auto_20180102_0114'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lista_pelis',
            name='fecha_busqueda',
            field=models.DateTimeField(null=True),
        ),
    ]