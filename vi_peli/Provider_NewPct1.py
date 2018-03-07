#coding=utf-8
from __future__ import unicode_literals
from requests.compat import urljoin
import requests
import json
from Viserpel.settings import JSON_ROOT, BASE_DIR
from time import timezone
import sys
from auxiliar import reemplaza, renombra
from bs4 import BeautifulSoup
import re
import logging.config
from Viserpel.settings import LOGGING
from .models import Lista_Pelis
from django.db.models import Q


logging.config.dictConfig(LOGGING)
#fichero_log = os.path.join(APP_DIR, 'log', 'vi_peli.log')
logger = logging.getLogger(__name__)

# Create your views here.

class NewPct():


    def __init__(self):

        self.proveedor_old = 'newpct1.com'
        self.proveedor_new = 'descargas2020.com'

        self.url = 'http://descargas2020.com'
        self.urls = {'search_hd': urljoin(self.url, '/peliculas-hd/'),
                     'search': urljoin(self.url, '/peliculas/'),
                     'downloadregex': 'http://descargas2020.com//descargar-torrent/\d+_[^\"]+', }


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
                    download_url = torrent_anchor.get('href', '')
                    logger.debug ('enlace: '+download_url)
                    enlace_ant = download_url.replace(self.proveedor_new, self.proveedor_old)
                    logger.debug ('enlace_old: ' + enlace_ant)
                    busca_enlace = Lista_Pelis.objects.filter(Q(enlace__iexact = download_url) | Q(enlace__iexact = enlace_ant))

                    logger.debug(len(busca_enlace))

                    if len(busca_enlace)==0:
                        seguidos = 0
                        #titulo = torrent_anchor.find('h2').getText()
                        titulo = torrent_anchor.get('title', '').replace ('Descargar','').replace ('gratis','').strip()
                        logger.debug(titulo)
                        titulo = reemplaza (titulo)
                        calidad = torrent_anchor.find('span').getText()
                        imagen = torrent_anchor.find('img').get('src')
                        logger.debug (calidad)
                        logger.debug (imagen)

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
                        #http://descargas2020.com/descargar-torrent/104804_-1519459792-thor-ragnarok--blurayrip-ac3-51
                        match = re.search(r'http://'+ self.proveedor_new +'/descargar-torrent/\d+_[^\"]*', str(html_t), re.DOTALL)
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

                    else:
                        seguidos= seguidos+1
                        if seguidos > 5:
                            return resultados
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
