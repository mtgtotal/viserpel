# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-01-02 00:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vi_peli', '0006_auto_20180102_0107'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lista_pelis',
            name='fecha_busqueda',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
