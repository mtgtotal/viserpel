# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import Lista_Pelis, Pelicula, MisPelis

admin.site.register(Lista_Pelis)
admin.site.register(Pelicula)
admin.site.register(MisPelis)