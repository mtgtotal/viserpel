# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-29 22:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vi_peli', '0002_auto_20171229_2212'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lista_pelis',
            name='enlace',
            field=models.TextField(db_tablespace='indexes'),
        ),
        migrations.AlterField(
            model_name='lista_pelis',
            name='titulo',
            field=models.TextField(db_tablespace='indexes'),
        ),
        migrations.AlterField(
            model_name='lista_pelis',
            name='torrent',
            field=models.TextField(db_tablespace='indexes'),
        ),
    ]