# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-01-01 21:32
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vi_peli', '0004_auto_20171230_0000'),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name='lista_pelis',
            name='vi_peli_lis_torrent_3c4a65_idx',
        ),
    ]