# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-01-05 18:29
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vi_peli', '0010_auto_20180103_2156'),
    ]

    operations = [
        migrations.CreateModel(
            name='MisPelis',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=200)),
                ('titulo_orig', models.CharField(max_length=200)),
                ('calidad', models.CharField(max_length=50, null=True)),
                ('directorio', models.TextField()),
            ],
        ),
        migrations.AddField(
            model_name='pelicula',
            name='duracion',
            field=models.CharField(max_length=15, null=True),
        ),
        migrations.AddField(
            model_name='pelicula',
            name='escritor',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='pelicula',
            name='pais',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='pelicula',
            name='director',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='pelicula',
            name='titulo',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='pelicula',
            name='titulo_orig',
            field=models.CharField(max_length=200),
        ),
        migrations.AddField(
            model_name='mispelis',
            name='idPeli',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mipeli', to='vi_peli.Pelicula'),
        ),
    ]
