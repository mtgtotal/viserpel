#coding=utf-8
from Viserpel.settings import JSON_ROOT, BASE_DIR, STATIC_ROOT, MEDIA_ROOT, APP_DIR
from models import Lista_Pelis, Pelicula, Generos
import os
import logging.config
from Viserpel.settings import LOGGING
from django.db.models import Q
import sqlite3

logging.config.dictConfig(LOGGING)
#fichero_log = os.path.join(APP_DIR, 'log', 'vi_peli.log')
logger = logging.getLogger(__name__)

class C_Busqueda():
    numeros =['0','1','2','3','4','5','6','7','8','9']

    def busca_bbdd(self, vtitulo=None, vletra=None, vyear=None, lgeneros=None, lcalidad=None):

        q=Pelicula.objects.filter()

        if vtitulo <> None or vtitulo == "":
            print ("entra titulo")
            q = q.filter(titulo__contains=vtitulo)

        if vletra <> None or vletra == "":
            print ("entra letra")
            cons = ""
            if vletra == '0-9':
                q = q.filter((Q(titulo__startswith="0") | Q(titulo__startswith="1") | Q(titulo__startswith="2") | Q(titulo__startswith="3") | Q(titulo__startswith="4") | Q(titulo__startswith="5") | Q(titulo__startswith="6") | Q(titulo__startswith="7") | Q(titulo__startswith="8") | Q(titulo__startswith="9")))
            elif vletra == 'otros':
                q = q.filter((Q(titulo__startswith=u"¿") | Q(titulo__startswith=u"¡")))
            else:
                q = q.filter(titulo__startswith = vletra)

        if vyear <> None or vyear == "":
            print ("entra anio")
            q = q.filter(year__exact = vyear)

        if lgeneros <> None or lgeneros == "":
            print ("entra genero")

            genero = Generos.objects.get(id_gen = lgeneros)
            print (genero)
            l_gen = genero.desc_generos.split('-')
            print (l_gen)

            q = q.filter(generos__contains = l_gen[0])|q.filter(generos__contains = l_gen[1])

        if lcalidad <> None or lcalidad == "":
            print ("entra calidad")
            q = q.filter(calidad__contains = lcalidad)

        resultado = q

        #logger.debug (resultado)

        return resultado

