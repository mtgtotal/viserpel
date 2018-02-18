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
import httplib, urllib
reload(sys)
sys.setdefaultencoding("utf-8")

logging.config.dictConfig(LOGGING)
#fichero_log = os.path.join(APP_DIR, 'log', 'vi_peli.log')
logger = logging.getLogger(__name__)

# Create your views here.

def reemplaza(texto):
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
    a = a.replace(u'\xc3\xa0', u' ')

    return a


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


def renombra(fila_ini):
    source = fila_ini

    # source = source.replace(u'ñ', 'n')
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


class enviar_datos:
    def conectar(self, host, campo, valor):
        self.variables = []
        self.valores = []
        self.campo = campo
        self.valor = valor
        self.host = host
        self.datos = {}
        for campo_variables, valor_variables in zip(self.campo.split(":"), self.valor.split(":")):
            self.variables.append(campo_variables)
            self.valores.append(valor_variables)
        for variable, valor in zip(self.variables, self.valores):
            self.datos['%s' % variable] = valor
        print (self.datos)
        try:
            return urllib.urlopen(self.host, urllib.urlencode(self.datos)).read()
        except:
            return "No se puede conectar a %s" % (self.host)


class MejorTorrent():
    def __init__(self):

        base = "http://www.mejortorrent.com"
        self.url = 'http://www.mejortorrent.com'
        self.urls = {'search': urljoin(self.url, '/secciones.php?sec=descargas&ap=peliculas&p='),
                     'search_hd': urljoin(self.url, '/secciones.php?sec=descargas&ap=peliculas_hd&p='),
                     'todas': '/peliculas-buscador.html', }

        self.letras = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '0-9', 'otros']

    def busca_pelis(self, url, ultima_peli, paginas):
        print ('busca_pelis')

        resultados = []
        if paginas <> None:
            try:
                # Si es un nº de página x aqui, si no se va por except
                npag = int(paginas)
            except:
                misletras = []
                letra = 'AC0-9otros'
                if letra.find('0-9'):
                    misletras.append('0-9')
                if letra.find('otros'):
                    misletras.append('otros')
                for l in letra:
                    if l in self.letras:
                        misletras.append(l)
        else:
            misletras = self.letras
            npag = None

        if url == 'MejorTorrent':
            xurl = self.urls["search"]
        elif url == 'MejorTorrent_HD':
            xurl = self.urls["search_hd"]
        elif url == 'MejorTorrent_Todo':
            xurl = self.urls["todas"]

        if url == 'MejorTorrent_Todo':
            # Cogemos todos por letras
            indice = 0
            for let in misletras:
                print (let)
                """
                parametros = urllib.urlencode({'campo': 'letra', 'valor': '', 'valor2': '', 'valor3': let, 'valor4': ''})
                print (parametros)
                cabeceras = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
                print ('0')
                abrir_conexion = httplib.HTTPConnection("www.mejortorrent.com:80")
                print ('1')
                abrir_conexion.request("POST", '/peliculas-buscador.html', parametros, cabeceras)
                print ('2')
                respuesta = abrir_conexion.getresponse()
                print ('3')
                """
                url = 'http://www.mejortorrent.com/peliculas-buscador.html'
                variables = "campo:valor:valor2:valor3:valor4:"
                valores = "letra:::"+let+":"
                conec = enviar_datos()
                ver_source = conec.conectar(url, variables, valores)

                if ver_source <> "No se puede conectar a %s" % url:
                    html_t = BeautifulSoup(ver_source, "html.parser")
                    tabla = html_t.find('table',
                                        {'width': '90%', 'align': 'center', 'cellspacing': '0', 'cellpadding': '0',
                                         'border': '0'})
                    enlaces = tabla.find_all('a')
                    for link in enlaces:
                        idioma = re.search(r'\[Subs. integrados\]', str(link))
                        if not idioma:
                            enlace = urljoin(self.url, link.get('href'))
                            peli = self.datos_pelis(enlace, indice)
                            if peli <> None:
                                resultados.append(peli)
                                indice +=1
        else:

            # Descargamos sólo las páginas indicadas de las paginas principales.

            if npag > 50:
                npag = 50
            indice = 0
            logger.info ('Nº de Paginas --> '+  str(npag))

            for pag in range(1, npag):
                logger.debug('Pagina Actual --> ' + str(pag))
                req = requests.get(xurl + str(pag))
                logger.debug(xurl + str(pag))
                html_t = BeautifulSoup(req.text, "html.parser")
                enlaces = html_t.find_all('a')
                logger.debug ('Nº de Enlaces encontrados --> ' + str(len(enlaces)))
                print ('Nº de Enlaces encontrados --> ' + str(len(enlaces)))
                for link in enlaces:
                    peli = True
                    try:
                        imagen = urljoin(self.url, link.find('img').get('src'))
                        logger.debug('Imagen --> ' + imagen)
                    except:
                        peli = False
                    if peli:

                        enlace = urljoin(self.url, link.get('href'))
                        logger.debug('enlace--> ' + enlace)
                        pelicula = self.datos_pelis(enlace, indice)
                        if pelicula <> None:
                            resultados.append(pelicula)
                            indice = indice + 1

        return resultados

    def datos_pelis(self, url, indice):
        logger.info (indice)
        try:
            req = requests.get(url)
            html_t = BeautifulSoup(req.text, "html.parser")

            imagen = html_t.find('img', {'width': '120', 'height': '165'})
            if imagen:
                imagen = imagen.get('src')
                logger.info(imagen)
            else:
                logger.error("No se ha encontrado la imagen")
            try:
                enlace = html_t.find('a', {'style': 'font-size:12px;'})
                #logger.debug(str(enlace))
                ref = enlace.get('href')
                logger.debug(ref)
                pag_torrent = urljoin(self.url, ref)
                logger.debug('Pagina del torrent --> ' + pag_torrent)
            except:
                logger.error ("Error al buscar la web del Torrent")
                logger.error (sys.exc_info())

            tablas = html_t.find('table', {'width': '450'})
            tabla = tablas
            peli = True
            # logger.warning (tabla)
            # tabla = reemplaza(tabla)
            # tabla = renombra(tabla)
            # logger.warning("----------------------tabla 2------------------------")
            # logger.warning(tabla)
            titu = tabla.find('span', {'style': 'font-size:18px; color:#0A3A86;'})
            titulo = titu.find('b').text
            logger.info('Titulo --> ' + titulo)
            print ("Titulo --> " + titulo + " Indice--> " + str(indice))
            # print (tabla)
            try:
                tabla = unicode(tabla.text)
                tabla = reemplaza(tabla)
                tabla = renombra(tabla)
                logger.debug ('Tras Reemplazar etc')
                generos = re.search(r'nero:(.+)\.', unicode(tabla))
                if not generos:
                    generos = None
                    logger.warning("Generos no encontrados")
                else:
                    generos = generos.group(1).strip()
                    # generos = generos.replace(u"  ", "")
                    generos = generos.replace(" - ", ",")
                    logger.info(generos)

                anio = re.search(r'Año:.*([0-9]{4})', unicode(tabla))
                if not anio:
                    anio = None
                    logger.warning("Año no encontrado")
                else:
                    anio = anio.group(1)
                    anio = anio.replace("  ", "")
                    logger.info(anio)

                director = re.search(r'Director:(.+)', unicode(tabla))
                if not director:
                    director = None
                    logger.warning("director no encontrado")
                else:
                    director = director.group(1)
                    director = director.replace("  ", "")
                    logger.info(director)

                actores = re.search(r'Actores:(.+)\.', unicode(tabla))
                if not actores:
                    actores = None
                    logger.warning("actores no encontrado")
                else:
                    actores = actores.group(1)
                    actores = actores.replace("  ", "")
                    logger.info(actores)

                formato = re.search(r'Formato:(.+)', unicode(tabla))
                if not formato:
                    formato = None
                    logger.warning("formato no encontrado")
                else:
                    formato = formato.group(1)
                    formato = formato.replace("  ", "")
                    logger.info(formato)

                fecha = re.search(r'Fecha:(.+)', unicode(tabla))
                if not fecha:
                    fecha = None
                    logger.error("fecha no encontrado")
                else:
                    fecha = fecha.group(1)
                    fecha = fecha.replace("  ", "")
                    logger.info(fecha)

                tamanio = re.search(r'Tamaño:(.+)', unicode(tabla))
                if not tamanio:
                    tamanio = None
                    logger.error("tamanio no encontrado")
                else:
                    tamanio = tamanio.group(1)
                    tamanio = tamanio.replace("  ", "")
                    logger.info(tamanio)

            except:
                logger.error ('Se ha producido un error al buscar la información de la película ' + titulo)
                logger.error(sys.exc_info())
            try:
                sinopsis = tablas.find('div', {'align': 'justify'})
                sinopsis = unicode(sinopsis.getText)
                logger.info('SINOPSIS --> ' + sinopsis)
            except:
                logger.error('Se ha producido un error al buscar la sinopsis ' + titulo)
                logger.error(sys.exc_info())

            req.close()
            # Buscamos el torrent
            try:
                if pag_torrent:
                    req1 = requests.get(pag_torrent)
                    html = BeautifulSoup(req1.text, "html.parser")

                    torrents = html.find_all('a')
                    for x in torrents:
                        if x.text == "aquí":
                            torrent = urljoin(self.url, x.get('href'))
                            logger.info ('Torrent--> '+torrent)
            except:
                logger.error('Se ha producido un error al buscar el torrent ' + titulo)
                logger.error(sys.exc_info())

            item = {
                'titulo': unicode(titulo),
                'titulo_orig': None,
                'anio': anio,
                'enlace': pag_torrent,
                'calidad': formato,
                'imagen': imagen,
                'torrent': torrent,
                'sinopsis': unicode(sinopsis),
                'tamanio': tamanio,
                'fecha': fecha,
                'indice': indice

            }
            logger.debug("==================================================================================================")
            return item
        except:
           logger.error("Error General en Busca de Datos")
           return None
