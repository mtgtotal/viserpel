# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-29 23:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vi_peli', '0003_auto_20171229_2357'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='lista_pelis',
            index=models.Index(fields=['torrent'], name='vi_peli_lis_torrent_3c4a65_idx'),
        ),
    ]
