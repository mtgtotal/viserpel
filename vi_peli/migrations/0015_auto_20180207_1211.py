# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-02-07 11:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vi_peli', '0014_auto_20180116_2147'),
    ]

    operations = [
        migrations.CreateModel(
            name='Generos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_gen', models.CharField(max_length=20)),
                ('nom_genero', models.CharField(max_length=200)),
                ('desc_generos', models.TextField(max_length=200, null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='pelicula',
            name='img',
        ),
        migrations.AlterField(
            model_name='pelicula',
            name='titulo_orig',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
