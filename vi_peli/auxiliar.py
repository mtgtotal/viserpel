#coding=utf-8
from __future__ import unicode_literals
from Viserpel.settings import JSON_ROOT, BASE_DIR, STATIC_ROOT, MEDIA_ROOT, APP_DIR
from models import Lista_Pelis, Pelicula, MisPelis
from peliculas_datos import Peliculas_ficha
import sys
from PIL import Image
from urllib import urlopen
from StringIO import StringIO
import logging
import logging.config
from Viserpel.settings import LOGGING
import os

logging.config.dictConfig(LOGGING)
logger = logging.getLogger(__name__)


def log_datos(peli):

    try:
        for key, value in peli.iteritems():
            try:
                logger.debug(key + ' --> ' + value)
            except:
                logger.debug(key + ' --> None')
    except:
        try:
            for key, value in peli.viewitems():
                try:
                    logger.debug(key + ' --> ' + value)
                except:
                    logger.debug(key + ' --> None')
        except:
            logger.debug ('>-- Pelicula --<')
            logger.debug (peli)


def reemplaza (texto):
    a = texto
    a = a.replace(u'\xc3\xb1', u'ñ')
    a = a.replace(u'\xc3\u2018', u'Ñ')
    a = a.replace(u'\xc3\xa1', u'á')
    a = a.replace(u'\xc3\xa9', u'é')
    a = a.replace(u'\xc3\xad', u'í')
    a = a.replace(u'\xc3\xb3', u'ó')
    a = a.replace(u'\xc3\xba', u'ú')
    a = a.replace(u'\xc3\x81', u'Á')
    a = a.replace(u'\xc3\u2030', u'É')
    a = a.replace(u'\xc3\x8d', u'Í')
    a = a.replace(u'\xc3\u201c', u'Ó')
    a = a.replace(u'\xc3\u0161', u'Ú')

    return a

def renombra(fila_ini):

    source = fila_ini
    source = source.replace(u'|', '-')
    source = source.replace(u'\/', '-')
    source = source.replace(u'\\', '-')
    source = source.replace(u':', '-')
    source = source.replace(u'?', '')
    source = source.replace(u'*', '-')
    source = source.replace(u'<', '')
    source = source.replace(u'>', '')
    source = source.replace(u'"', '')

    source = source.replace(u'ñ', 'n')
    source = source.replace(u'á', 'a')
    source = source.replace(u'é', 'e')
    source = source.replace(u'í', 'i')
    source = source.replace(u'ó', 'o')
    source = source.replace(u'ú', 'u')
    source = source.replace(u'Á', 'A')
    source = source.replace(u'É', 'E')
    source = source.replace(u'Í', 'I')
    source = source.replace(u'Ó', 'O')
    source = source.replace(u'Ú', 'U')
    source = source.replace(u'/x93', '')
    source = source.replace(u'/x94', '')
    # os.renamestr (fila_ini, source)
    return source

def renombra_archivo(fila_ini):
    source = fila_ini
    source = source.replace(u'|', '-')
    source = source.replace(u'\/', '-')
    source = source.replace(u'\\', '-')
    source = source.replace(u':', '-')
    source = source.replace(u'?', '')
    source = source.replace(u'*', '-')
    source = source.replace(u'<', '')
    source = source.replace(u'>', '')
    source = source.replace(u'"', '')

    source = source.replace(u'ñ', 'n')
    source = source.replace(u'á', 'a')
    source = source.replace(u'é', 'e')
    source = source.replace(u'í', 'i')
    source = source.replace(u'ó', 'o')
    source = source.replace(u'ú', 'u')
    source = source.replace(u'Á', 'A')
    source = source.replace(u'É', 'E')
    source = source.replace(u'Í', 'I')
    source = source.replace(u'Ó', 'O')
    source = source.replace(u'Ú', 'U')
    source = source.replace(u'/x93', '')
    source = source.replace(u'/x94', '')
    # os.renamestr (fila_ini, source)
    return source

def prepara_titu (self, titulo):
    source = titulo
    source = source.replace(u'|', '')
    source = source.replace(u'\/', '')
    source = source.replace(u'\\', '')
    source = source.replace(u':', '')
    source = source.replace(u'?', '')
    source = source.replace(u'*', '')
    source = source.replace(u'<', '')
    source = source.replace(u'>', '')
    source = source.replace(u'"', '')
    source = source.replace(u"'", '')
    source = source.replace(u'.', '')
    source = source.replace(u'¡', '')
    source = source.replace(u'¿', '')
    source = source.replace(u'!', '')
    source = source.replace(u'$', '')
    source = source.replace(u'%', '')
    source = source.replace(u'[', '')
    source = source.replace(u']', '')
    source = source.replace(u'{', '')
    source = source.replace(u'}', '')
    source = source.replace(u'+', '')
    source = source.replace(u'^', '')
    source = source.replace(u'-', '')
    source = source.replace(u'_', '')
    source = source.replace(u'&', 'y')
    source = source.replace(u'(', '')
    source = source.replace(u')', '')
    source = source.replace(u',', '')

    source = source.replace(u'   ', '')
    source = source.replace(u'  ', '')
    source = source.replace(u' ', '')

    source = source.replace(u'ñ', 'n')
    source = source.replace(u'Ñ', 'N')
    source = source.replace(u'á', 'a')
    source = source.replace(u'é', 'e')
    source = source.replace(u'í', 'i')
    source = source.replace(u'ó', 'o')
    source = source.replace(u'ú', 'u')
    source = source.replace(u'Á', 'A')
    source = source.replace(u'É', 'E')
    source = source.replace(u'Í', 'I')
    source = source.replace(u'Ó', 'O')
    source = source.replace(u'Ú', 'U')
    source = source.replace(u'/x93', '')
    source = source.replace(u'/x94', '')
    source = source.upper()
    return source

def transforma(self,texto):
    a = texto
    a = a.replace(u' ', u'%20')
    a = a.replace(u'ñ', u'%C3%B1')
    a = a.replace(u'+', u'%2B')
    a = a.replace(u':', u'%3A')
    a = a.replace(u'(', u'%28')
    a = a.replace(u')', u'%29')
    a = a.replace(u',', u'')
    a = a.replace(u'¡', u'%C2%A1')
    a = a.replace(u'!', u'%21')
    a = a.replace(u'¿', u'%C2%BF')
    a = a.replace(u'?', u'%3F')
    a = a.replace(u'á', u'%C3%A1')
    a = a.replace(u'é', u'%C3%A9')
    a = a.replace(u'í', u'%C3%AD')
    a = a.replace(u'ó', u'%C3%B3')
    a = a.replace(u'ú', u'%C3%BA')
    a = a.replace(u'Á', u'%C3%81')
    a = a.replace(u'É', u'%C3%89')
    a = a.replace(u'Í', u'%C3%8D')
    a = a.replace(u'Ó', u'%C3%93')
    a = a.replace(u'Ú', u'%C3%9A')
    return a

def sinacento(self, fila_ini):

    source = fila_ini

    source = source.replace(u'ñ', 'n')
    source = source.replace(u'á', 'a')
    source = source.replace(u'é', 'e')
    source = source.replace(u'í', 'i')
    source = source.replace(u'ó', 'o')
    source = source.replace(u'ú', 'u')
    source = source.replace(u'Á', 'A')
    source = source.replace(u'É', 'E')
    source = source.replace(u'Í', 'I')
    source = source.replace(u'Ó', 'O')
    source = source.replace(u'Ú', 'U')

    return source