# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-02-19 17:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vi_peli', '0018_auto_20180218_1734'),
    ]

    operations = [
        migrations.AddField(
            model_name='lista_pelis',
            name='titulo_ben',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='lista_pelis',
            name='titulo_bes',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='pelicula',
            name='titulo_ben',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='pelicula',
            name='titulo_bes',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
