#coding=utf-8
from __future__ import unicode_literals
from requests.compat import urljoin
import requests
import json
from Viserpel.settings import JSON_ROOT, BASE_DIR
from time import timezone
import sys
from bs4 import BeautifulSoup
import re
import logging.config
from Viserpel.settings import LOGGING


logging.config.dictConfig(LOGGING)
#fichero_log = os.path.join(APP_DIR, 'log', 'vi_peli.log')
logger = logging.getLogger(__name__)

# Create your views here.

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

class NewPct():
    def __init__(self):

        self.url = 'http://newpct1.com'
        self.urls = {'search_hd': urljoin(self.url, '/peliculas-hd/'),
                     'search': urljoin(self.url, '/peliculas/'),
                     'downloadregex': 'http://newpct1.com//descargar-torrent/\d+_[^\"]+', }


    def run(self):
        datos = self.busca_pelis(self.urls['search_hd'], None, 1)
        nombre = 'NewPct1_hd'
        with open('/json/'+ nombre +'.json', 'w') as file:
            json.dump(datos, file)

    def busca_pelis(self, url, ultima_peli, paginas):

        resultados = []
        pg_max = 1

        if paginas == None:
            pg_max = self.busca_paginas(url)
        else:
            pg_max = paginas
        pg = 1
        logger.debug ('Paginas: '+ str(pg_max))
        salir = True
        indice = 0
        while int(pg) <= int(pg_max) and salir == True:
            xurl = url + 'pg/' + str(pg)
            logger.debug(xurl)
            req = requests.get(xurl)
            data = req.text
            if data == "":
                logger.error("ho hay datos")
                salir = False
            html = BeautifulSoup(data, "html.parser")
            if html == "":
                logger.error("Html vacio")
                salir = False
            # Busqueda en primera página.
            logger.debug("Pagina actual: " + str(pg))
            pg += 1
            logger.debug ("---------------------------------------------------")
            torrent_table = html.find('ul', class_='pelilist')
            torrent_rows = torrent_table('li') if torrent_table else []

            # Continue only if at least one release is found
            if not len(torrent_rows):
                logger.warning("no rows encontradas")
                salir = False
                return resultados

            for row in torrent_rows:
                try:
                    torrent_anchor = row.find_all('a')[0]

                    #titulo = torrent_anchor.find('h2').getText()
                    titulo = torrent_anchor.get('title', '').replace ('Descargar','').replace ('gratis','').strip()
                    logger.debug(titulo)
                    titulo = reemplaza (titulo)
                    calidad = torrent_anchor.find('span').getText()
                    imagen = torrent_anchor.find('img').get('src')
                    logger.debug (calidad)
                    logger.debug (imagen)
                    download_url = torrent_anchor.get('href', '')


                    if ultima_peli == download_url and ultima_peli != None:
                        logger.info("Fin del Proceso - Encontrada ultima peli")
                        return resultados


                    if not all([titulo, download_url]):
                        continue

                    req_t = requests.get(download_url)
                    data_t = req_t.text
                    html_t = BeautifulSoup(data_t, "html.parser")
                    entradas = html_t.find('div', {'class': 'descripcion_top'})
                    texto = entradas.text
                    #logger.debug('------------------------------------Antes des renombrar-------------------------------------')
                    texto = reemplaza(texto)
                    #logger.debug('------------------------------------Antes des renombrar-------------------------------------')
                    texto = renombra(texto)
                    #logger.debug ('------------------------------------Texto tras renombrar-------------------------------------')
                    #logger.debug(texto)
                    entradas = html_t.find('div', {'class': 'sinopsis'})
                    sinopsis = entradas.text
                    sinopsis = reemplaza(sinopsis)
                    #logger.debug (sinopsis)

                    match = re.search(r'http://newpct1.com/descargar-torrent/\d+_[^\"]*', str(html_t), re.DOTALL)
                    if not match:
                        logger.debug ("No encontrado Torrent")
                        continue
                    else:
                        torrent = match.group()
                        logger.debug (torrent)


                    titulo_orig = re.search(r'Titulo original\s+([a-zA-Z\s&0-9\-]+)\s{1,}[Pais|Anyo]', texto)

                    if not titulo_orig:
                        logger.debug("No titulo original")
                        titulo_orig = None
                    else:
                        titulo_orig = titulo_orig.group(1)
                        titulo_orig = unicode(titulo_orig)
                        logger.debug ('Titulo Original: '+titulo_orig)
                        logger.debug('titulo:' + titulo + "   Indice:" + str(indice) + "  Url: " + download_url + '  Titulo Original: '+titulo_orig)

                    anio = re.search(r'Ano\s+(\d{4})\s+Dura', texto)
                    logger.info (anio)
                    if not anio:
                        try:
                            entradas = html_t.find('h1', {})
                            texto = entradas.text
                            logger.debug(texto)
                            texto = reemplaza(texto)
                            texto = renombra(texto)
                            logger.debug (texto)
                            match = re.search(r'\[([0-9]{4})^p\]*', str(texto), re.DOTALL)
                            if not match:
                                logger.info ("No se ha encontrado año")
                            else:
                                anio = match.group(1)
                                logger.debug ("Año encontrado --> " + anio)
                        except:
                            anio = None
                    else:
                        anio = anio.group(1)
                        #logger.debug (anio)
                    ###entry-left

                    try:
                        entradas = html_t.find('div', {'class': 'entry-left'})
                        tamanio = re.search(r'Size:<\/strong>\s+([a-zA-Z\s&0-9\-\.]+)<\/span>', str(entradas),re.DOTALL).group(1)
                        fecha = re.search(r'Fecha:<\/strong>\s+([a-zA-Z\s&0-9\-\.]+)<\/span>', str(entradas), re.DOTALL).group(1)
                        #logger.debug(str(tamanio))
                        #logger.debug(str(fecha))
                    except:
                        tamanio = None
                        fecha = None

                    # logger.debug (u'Año: ' + str(anio))
                    item = {
                        'titulo': unicode(titulo),
                        'titulo_orig': titulo_orig,
                        'anio': anio,
                        'enlace': download_url,
                        'calidad': calidad,
                        'imagen': imagen,
                        'torrent': torrent,
                        'sinopsis': unicode(sinopsis),
                        'tamanio': tamanio,
                        'fecha': fecha,
                        'indice':indice

                    }

                    resultados.append(item)

                    logger.debug ('=======================================================================')
                    indice = indice + 1
                ##          logger.debug ('******** INDICE: ' + str(indice))
                ##          if indice == 15:
                ##            return resultados
                ##

                except (AttributeError, TypeError):
                    logger.error(sys.exc_info())
                    return 0
                    # continue
        logger.info ("Fin del Proceso")
        return resultados

    def busca_paginas(self, url):

        pagina = 1
        req = requests.get(url)
        data = req.text
        if data == "":
            logger.debug("ho hay datos")
            salir = False
        html = BeautifulSoup(data, "html.parser")

        if html == "":
            logger.warning("Html vacio")
            salir = False

        torrent_table = html.find('ul', class_='pagination')
        torrent_rows = torrent_table('li') if torrent_table else []

        if not len(torrent_rows):
            logger.debug("no rows encontradas")
            return 1

        for row in torrent_rows:
            pagina_new = row.find_all('a')[0]
            pagina_new = pagina_new.text
            if pagina_new == "Next":
                return pagina
            pagina = pagina_new

        return pagina
