#coding=utf-8
from Viserpel.settings import JSON_ROOT, BASE_DIR, STATIC_ROOT, MEDIA_ROOT, APP_DIR
from models import Lista_Pelis, Pelicula, Generos, Calidades
import os
import logging.config
from Viserpel.settings import LOGGING
from django.db.models import Q
import sqlite3

logging.config.dictConfig(LOGGING)
#fichero_log = os.path.join(APP_DIR, 'log', 'vi_peli.log')
logger = logging.getLogger(__name__)

class C_Busqueda():


    def busca_bbdd(self, vtitulo=None, vletra=None, vyear=None, lgeneros=None, lcalidad=None):

        q=Pelicula.objects.filter()


        if vtitulo <> None or vtitulo == "":
            logger.debug ("entra titulo")
            q = q.filter(titulo__contains=vtitulo)

        if vletra <> None or vletra == "":
            logger.debug ("entra letra")
            cons = ""
            numeros = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
            if vletra == '0-9':
                q = q.filter(reduce(lambda x, y: x | y, [Q(titulo__startswith=item) for item in numeros]))
                #q = q.filter((Q(titulo__startswith="0") | Q(titulo__startswith="1") | Q(titulo__startswith="2") | Q(titulo__startswith="3") | Q(titulo__startswith="4") | Q(titulo__startswith="5") | Q(titulo__startswith="6") | Q(titulo__startswith="7") | Q(titulo__startswith="8") | Q(titulo__startswith="9")))
            elif vletra == 'otros':
                q = q.filter((Q(titulo__startswith=u"¿") | Q(titulo__startswith=u"¡")))
            else:
                q = q.filter(titulo__startswith = vletra)

        if vyear <> None or vyear == "":
            logger.debug ("entra anio")
            q = q.filter(year__exact = vyear)

        if lgeneros <> None or lgeneros == "":
            logger.debug ("entra genero")

            genero = Generos.objects.get(id_gen = lgeneros)
            logger.debug (genero)
            l_gen = genero.desc_generos.split('-')
            logger.debug (l_gen)

            q = q.filter(generos__contains = l_gen[0])|q.filter(generos__contains = l_gen[1])

        if lcalidad <> None or lcalidad == "":
            logger.debug ("entra calidad")

            lq = Lista_Pelis.objects.filter()

            cal = Calidades.objects.get(nombre = lcalidad)
            l_gen = cal.otros_nombres.split(',')
            logger.debug (l_gen)
            cuantos = len(l_gen)
            print (cuantos)
            lq = lq.filter(reduce(lambda x, y: x | y, [Q(calidad__contains = item) for item in l_gen]))
            print (lq)
            lista_fichas=[]
            for x in lq:
                logger.debug (x.titulo)
                lista_fichas.append(x.titulo)

            if len(lista_fichas) > 0:
                lista_fichas = set(lista_fichas)
                logger.info(lista_fichas)

                q = q.filter(reduce(lambda x, y: x | y, [Q(titulo=item) for item in lista_fichas]))
            else:
                return None
        if len(q)>0:
            resultado = q
        else:
            resultado = None
        #logger.debug (resultado)

        return resultado

