#coding=utf-8
from __future__ import unicode_literals
from requests.compat import urljoin
import requests
from django.shortcuts import render
import json
from django.shortcuts import redirect, render_to_response,  get_object_or_404
from Viserpel.settings import JSON_ROOT, BASE_DIR
from time import timezone
from models import Lista_Pelis, Pelicula, MisPelis
import os
from peliculas_datos import Peliculas_ficha
from bs4 import BeautifulSoup
import re

# Create your views here.
def vprint (texto):
    try:
        print (unicode(texto))
    except:
        try:
            print (texto)
        except:
            print ("No se ha podido imprimir")
def reemplaza (texto):
    return texto
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

    source = source.replace(u'ñ', 'ny')
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
        nombre =  'NewPct1_hd'
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

        salir = True
        indice = 1
        while int(pg) <= int(pg_max) and salir == True:
            xurl = url + 'pg/' + str(pg)
            vprint(xurl)
            req = requests.get(xurl)
            data = req.text
            if data == "":
                vprint("ho hay datos")
                salir = False
            html = BeautifulSoup(data, "html.parser")
            if html == "":
                vprint("Html vacio")
                salir = False
            # Busqueda en primera página.
            pg += 1
            vprint(str(pg))
            torrent_table = html.find('ul', class_='pelilist')
            torrent_rows = torrent_table('li') if torrent_table else []

            # Continue only if at least one release is found
            if not len(torrent_rows):
                vprint("no rows encontradas")
                salir = False
                return resultados

            for row in torrent_rows:
                try:
                    torrent_anchor = row.find_all('a')[0]

                    #titulo = torrent_anchor.find('h2').getText()
                    titulo = torrent_anchor.get('title', '').replace ('Descargar','').replace ('gratis','').strip()
                    titulo = reemplaza (titulo)
                    vprint ('titulo:' + titulo)

                    calidad = torrent_anchor.find('span').getText()
                    imagen = torrent_anchor.find('img').get('src')
                    vprint (calidad)
                    vprint (imagen)
                    download_url = torrent_anchor.get('href', '')
                    vprint (download_url)
                    if ultima_peli == download_url and ultima_peli != None:
                        vprint("Fin del Proceso - Encontrada ultima peli")
                        return resultados


                    if not all([titulo, download_url]):
                        continue

                    req_t = requests.get(download_url)
                    data_t = req_t.text
                    html_t = BeautifulSoup(data_t, "html.parser")
                    entradas = html_t.find('div', {'class': 'descripcion_top'})
                    texto = entradas.text
                    vprint('------------------------------------Antes des renombrar-------------------------------------')
                    texto = reemplaza(texto)
                    vprint('------------------------------------Antes des renombrar-------------------------------------')


                    texto = renombra(texto)
                    vprint ('------------------------------------Texto tras renombrar-------------------------------------')
                    try:
                        vprint(texto)
                    except:
                        vprint ('No se ha podido imprimir el texto')
                    # vprint (texto)
                    entradas = html_t.find('div', {'class': 'sinopsis'})
                    sinopsis = entradas.text
                    sinopsis = reemplaza(sinopsis)
                    # vprint (sinopsis)

                    match = re.search(r'http://newpct1.com/descargar-torrent/\d+_[^\"]*', str(html_t), re.DOTALL)
                    if not match:
                        vprint ("not match")
                        continue
                    else:
                        torrent = match.group()
                        vprint (torrent)


                    titulo_orig = re.search(r'Titulo original\s+([a-zA-Z\s&0-9\-]+)\s{1,}[Pais|Anyo]', texto)
                    if not titulo_orig:
                        titulo_orig = ""
                    else:
                        titulo_orig = titulo_orig.group(1)

                    ##          vprint ("--------------")
                        vprint ('Titulo Original: '+titulo_orig)

                    anio = re.search(r'Anyo\s+(\d{4})\s+Dura', texto)
                    if not anio:
                        anio = ""
                    else:
                        anio = anio.group(1)
                        vprint (anio)
                    ###entry-left
                    try:
                        entradas = html_t.find('div', {'class': 'entry-left'})
                        tamanio = re.search(r'Size:<\/strong>\s+([a-zA-Z\s&0-9\-\.]+)<\/span>', str(entradas),re.DOTALL).group(1)
                        fecha = re.search(r'Fecha:<\/strong>\s+([a-zA-Z\s&0-9\-\.]+)<\/span>', str(entradas), re.DOTALL).group(1)
                        vprint(str(tamanio))
                        vprint(str(fecha))
                    except:
                        tamanio = None
                        fecha = None

                    # vprint (u'Año: ' + str(anio))
                    item = {
                        'titulo': unicode(titulo),
                        'titulo_orig': unicode(titulo_orig),
                        'anio': anio,
                        'enlace': download_url,
                        'calidad': calidad,
                        'imagen': imagen,
                        'torrent': torrent,
                        'sinopsis': unicode(sinopsis),
                        'tamanio': tamanio,
                        'fecha': fecha,
                    }

                    resultados.append(item)

                    # vprint ('=================================================')
                    indice = indice + 1
                ##          vprint ('******** INDICE: ' + str(indice))
                ##          if indice == 15:
                ##            return resultados
                ##

                except (AttributeError, TypeError):
                    vprint(sys.exc_info())
                    return 0
                    # continue
        vprint ("Fin del Proceso")
        return resultados

    def busca_paginas(self, url):
        pagina = 1
        req = requests.get(url)
        data = req.text
        if data == "":
            vprint("ho hay datos")
            salir = False
        html = BeautifulSoup(data, "html.parser")

        if html == "":
            vprint("Html vacio")
            salir = False

        torrent_table = html.find('ul', class_='pagination')
        torrent_rows = torrent_table('li') if torrent_table else []

        if not len(torrent_rows):
            vprint("no rows encontradas")
            return 1

        for row in torrent_rows:
            pagina_new = row.find_all('a')[0]
            pagina_new = pagina_new.text
            if pagina_new == "Next":
                return pagina
            pagina = pagina_new

        return pagina
