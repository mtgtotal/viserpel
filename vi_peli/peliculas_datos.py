#coding=utf-8
from __future__ import unicode_literals
import omdb
import python_filmaffinity
import http.client
import json
from bs4 import BeautifulSoup
import requests
import re
from auxiliar import renombra, reemplaza, log_datos, transforma, sinacento, log_info
import logging.config
from Viserpel.settings import LOGGING

logging.config.dictConfig(LOGGING)
logger = logging.getLogger(__name__)

class Peliculas_ficha():

    def fichas_pelis(self, p_titulo=None, p_titulo_es=None, p_idFicha=None, p_anio=None, p_sinopsis=None):

        peli_movdb = self.datos_peli_moviedb(titulo=p_titulo, idFicha=p_idFicha, anio=p_anio, titulo_es=p_titulo_es,
                                             sinopsis=p_sinopsis)
        logger.debug(peli_movdb)
        peli_film = self.datos_peli_film(titulo=p_titulo, idFicha=p_idFicha, anio=p_anio, titulo_es=p_titulo_es,
                                         sinopsis=p_sinopsis)
        logger.debug(peli_film)
        peli_imbd = self.datos_peli_imbd(titulo=p_titulo, idFicha=p_idFicha, anio=p_anio, titulo_es=p_titulo_es,
                                         sinopsis=p_sinopsis)
        logger.debug(peli_imbd)
        if peli_movdb <> None:
            peli = peli_movdb
            if peli_film <> None and peli_film["idFicha"] <> None:
                peli["idFicha"] = peli["idFicha"] + "," + peli_film["idFicha"]
        elif peli_film <> None:
            peli = peli_film

        elif peli_imbd <> None:
            peli = peli_imbd
            nomb = []
            logger.debug(peli.titulo)
            logger.debug(peli.anio)
            nomb = self.nombre_imdb(peli.idFicha)
            logger.log(nomb)
            peli.titulo = nomb["nombre"]
            if peli.anio == "":
                peli.anio = nomb["anio"]

            logger.debug (peli.titulo)
            logger.debug (peli.anio)
        else:
            logger.warning("No se ha encontrado")
            logger.debug(p_titulo)
            logger.debug(p_titulo_es)

            if p_titulo == None and p_titulo_es <> None:
                v_titulo = p_titulo_es
                v_titulo_orig = None
                grabar = True
            elif p_titulo <> None and p_titulo_es == None:
                v_titulo = p_titulo
                v_titulo_orig = None
                grabar = True
            elif p_titulo <> None and p_titulo_es <> None:
                v_titulo = p_titulo_es
                v_titulo_orig = p_titulo
                grabar = True
            else:
                grabar = False

            if grabar:
                if p_anio == None or p_anio == '':
                    v_anio = None
                else:
                    v_anio = p_anio
                logger.info(p_anio)
                peli = {'titulo': v_titulo,
                        'titulo_orig': v_titulo_orig,
                        'anio': v_anio,
                        'generos': None,
                        'imagen': None,
                        'pais': None,
                        'escritor': None,
                        'director': None,
                        'actores': None,
                        'duracion': None,
                        'sinopsis': p_sinopsis,
                        'sinopsis_es': p_sinopsis,
                        'idFicha': None,

                        }

        logger.info ("***************** PELICULA ENCONTRADA FINAL ************************")
        log_info(peli)

        return peli

    def datos_peli_moviedb(self, titulo=None, idFicha=None, anio=None, sinopsis=None, titulo_es=None, **kwargs):
        logger.debug ('-------------- BUSCAMOS EN MOVIEDB --------------------')
        ruta_img = "https://image.tmdb.org/t/p/w300_and_h450_bestv2"
        conn = http.client.HTTPSConnection("api.themoviedb.org")
        print ('Entro en datos_peli_mviedb')
        payload = "{}"
        clave = '6954e616bbca6eb84ea9de73788e6e5f'
        pelicula = []
        if titulo_es == None and idFicha == None and titulo == None:
            logger.warning("No hay parámetros para la busqueda (MovieDB)")
            pelicula = []
        elif idFicha <> None:
            conn.request("GET", "/3/movie/" + str(idFicha) + "?language=es-ES&api_key=" + clave, payload)
            res = conn.getresponse()
            data = res.read()
            peli = json.loads(data)

        elif titulo_es <> None or titulo <> None:
            encontrado = False
            if titulo_es <> None:
                v_titulo = titulo_es
                v_idioma = 'es-ES'
            else:
                v_titulo = titulo
                v_idioma = 'en-US'
            print (v_titulo)
            tit = transforma(v_titulo)
            print (tit)
            if anio <> None:
                year = "year=" + str(anio) + "&"
            else:
                year = ""
            print (u'año:'+  str(year))
            conn.request("GET",
                         "/3/search/movie?" + year + "include_adult=false&page=1&query=" + tit + "&language=" + v_idioma + "&api_key=" + clave,
                         payload)
            res = conn.getresponse()
            data = res.read()

            #print (data)
            cadena_json = json.loads(data)
            resultados = int(cadena_json["total_results"])
            if resultados == 0:
                print ("Sin resultados")
                return None
            print ('Nº de Resultados --> ' + str(resultados))
            pelis = cadena_json["results"]
            #print (pelis)
            logger.debug('PELI')
            numero = 1
            for pelic in pelis:
                # print (pelic)
                logger.debug('FICHA ' + str(numero))
                log_datos(pelic)

                if (sinacento(v_titulo).upper() == sinacento(pelic["title"]).upper()) or (sinacento(v_titulo).upper() == sinacento(pelic["original_title"]).upper()):
                    logger.debug ('Titulo = al encontrado')
                    encontrado = True
                    v_idFicha = str(pelic['id'])
                    print ('ID de la Ficha -->' + str(v_idFicha))
                    conn.request("GET", "/3/movie/" + v_idFicha + "?language=es-ES&api_key=" + clave, payload)
                    res2 = conn.getresponse()
                    data2 = res2.read()
                    peli = json.loads(data2)
                    logger.debug('FICHA QUE COINCIDE EL TITULO COMPLETO')
                    log_datos(peli)
                    print (peli["imdb_id"])
                    if peli["imdb_id"] <> None:
                        vapikey = 'c3ca59d0'
                        omdb.set_default('apikey', vapikey)
                        logger.debug('FICHA_IMBD')
                        peli_imdb = omdb.imdbid(peli["imdb_id"])
                        log_datos(peli_imdb)
                    else:
                        print ('No tiene imbd')
                        peli_imdb = None
                    break
                """
                if encontrado == False and numero == 1 and pelic["overview"] <> "":
                    logger.debug('Guardamos el primer registro encontrado')
                    v_idFicha = str(pelic['id'])
                    conn.request("GET", "/3/movie/" + v_idFicha + "?language=es-ES&api_key=" + clave, payload)
                    res2 = conn.getresponse()
                    data2 = res2.read()
                    peli1 = json.loads(data2)
                    logger.debug("peli1")
                    log_datos(peli1)

                    vapikey = 'c3ca59d0'
                    omdb.set_default('apikey', vapikey)
                    logger.debug('FICHA_IMBD')
                    print (peli1["imdb_id"])
                    peli_imbd1 = omdb.imdbid(peli1["imdb_id"])
                    log_datos(peli_imbd1)
                """
                numero = numero + 1

            if encontrado == False:
                logger.warning('CUIDADO!! Quizás no coicida la pelicula')
                peli = None
                peli_imdb = None

        print ('vamos a preparar la Ficha')
        if peli:

            generos = ""
            if peli_imdb == None:
                imagen = None
                escritor = None
                director = None
                actores = None
                sinopsis_en = None
                pais = None
            else:
                anio = peli_imdb.year
                imagen = peli_imdb.poster
                escritor = peli_imdb.writer
                director = peli_imdb.director
                actores = peli_imdb.actors
                sinopsis_en = peli_imdb.plot
                pais = peli_imdb.country

            if imagen == None or imagen == "":
                imagen = ruta_img + peli["poster_path"]

            for g in peli["genres"]:
                generos = generos + "," + unicode(g["name"])
            generos = generos[1:]
            v_Ficha = ""
            if peli_imdb:
                v_Ficha = 'Imdb-' + str(peli["imdb_id"]) + "," + "movdb-" + str(peli["id"])
            else:
                v_Ficha = "movdb-" + str(peli["id"])
            print ('a x el item')

            item = {'titulo': unicode(peli["title"]),
                    'titulo_orig': unicode(peli["original_title"]),
                    'anio': anio,
                    'generos': generos,
                    'imagen': imagen,
                    'pais': pais,
                    'escritor': escritor,
                    'director': director,
                    'actores': actores,
                    'duracion': peli["runtime"],
                    'sinopsis': unicode(sinopsis_en),
                    'sinopsis_es': unicode(peli["overview"]),
                    'idFicha': v_Ficha,

                    }

            logger.debug('Finalmente nos queda ')
            log_datos(item)

        else:
            return None

        return item

    def datos_peli_imbd(self, titulo=None, idFicha=None, anio=None, sinopsis=None, titulo_es=None):
        logger.debug('-------------- BUSCAMOS EN IMBD --------------------')
        vapikey = 'c3ca59d0'
        omdb.set_default('apikey', vapikey)
        pelicula = []
        if titulo == None and idFicha == None:
            logger.error ("No hay parámetros para la busqueda")
            pelicula = []
        elif idFicha <> None:
            pelicula = omdb.imdbid(idFicha)

        elif titulo <> None:
            if anio == None:
                pelicula = omdb.get(title=titulo)
            else:
                pelicula = omdb.get(title=titulo, year=anio)

        if pelicula:
            log_datos(pelicula)

            item = {'titulo': titulo_es,
                    'titulo_orig': pelicula.title,
                    'anio': pelicula.year,
                    'generos': pelicula.genre,
                    'imagen': pelicula.poster,
                    'pais': pelicula.country,
                    'escritor': pelicula.writer,
                    'director': pelicula.director,
                    'actores': pelicula.actors,
                    'duracion': pelicula.runtime,
                    'sinopsis': pelicula.plot,
                    'sinopsis_es': sinopsis,
                    'idFicha': 'Imdb-' + pelicula.imdb_id,

                    }

            logger.debug('Finalmente nos queda ')
            log_datos(item)
        else:
            return None

        return item

    def datos_peli_film(self, titulo=None, idFicha=None, anio=None, sinopsis=None, titulo_es=None):
        logger.debug('-------------- BUSCAMOS EN FILMAFFINITY --------------------')
        service = python_filmaffinity.FilmAffinity(lang='es')
        service2 = python_filmaffinity.FilmAffinity(lang='en')
        pelicula = []
        if titulo_es == None and idFicha == None:
            print ("No hay parámetros para la busqueda")
            pelicula = []
        elif idFicha <> None:
            pelicula = service.get_movie(id=idFicha, images=True)
            pelicula2 = service2.get_movie(id=idFicha, images=True)

        elif titulo_es <> None:
            continuar = 0
            if anio == None:
                try:
                    busqueda = service.search(title=titulo_es)
                    if len(busqueda) > 1:
                        print ('Existen más de 1 resultado')
                        # return None
                    for peli in busqueda:
                        pelicula = service.get_movie(id=peli['id'], images=True)
                        pelicula2 = service2.get_movie(id=pelicula['id'], images=True)
                        continuar = 1
                        break
                except:
                    logger.error("Error en la búsqueda en español")

            else:
                try:
                    busqueda = service.search(title=titulo_es, from_year=anio, to_year=anio)
                    if len(busqueda) > 1:
                        print ('Existen más de 1 resultado')
                        # return None
                    for x in busqueda:
                        pelicula = service.get_movie(id=x['id'], images=True)
                        pelicula2 = service2.get_movie(id=pelicula['id'], images=True)
                        continuar = 1
                        break
                except:
                    logger.error("Error en la búsqueda en español")

        if titulo <> None and (continuar == 0 or titulo_es == None):
            if anio == None:
                try:
                    busqueda = service.search(title=titulo)
                    if len(busqueda) > 1:
                        print ('Existen más de 1 resultado')
                        # return None
                    for peli in busqueda:
                        pelicula2 = service2.get_movie(title=peli['title'], images=True)
                        pelicula = service.get_movie(id=pelicula2['id'], images=True)

                        logger.debug('Pelicula Español')
                        log_datos(pelicula)
                        logger.debug('Pelicula Ingles')
                        log_datos(pelicula2)

                        break
                except:
                    logger.error("Error en la búsqueda en original")
            else:
                try:
                    resul = service2.search(title=titulo, from_year=anio, to_year=anio)

                    if len(resul) > 1:
                        print ('Existen más de 1 resultado')
                        # return None
                    for x in resul:
                        pelicula2 = service2.get_movie(id=x['id'], images=True)
                        pelicula = service.get_movie(id=x['id'], images=True)

                        logger.debug('Pelicula Español')
                        log_datos(pelicula)
                        logger.debug('Pelicula Ingles')
                        log_datos(pelicula2)


                        break
                except:
                    logger.error("Error en la búsqueda en original")
        # xml_content = res.content
        # print (pelicula)

        if pelicula:
            item = {'titulo': pelicula['title'],
                    'titulo_orig': pelicula2['title'],
                    'anio': pelicula['year'],
                    'generos': ', '.join(pelicula['genre']),
                    'imagen': pelicula['poster'],
                    'pais': pelicula['country'],
                    'escritor': None,
                    'director': ', '.join(pelicula['directors']),
                    'actores': ', '.join(pelicula['actors']),
                    'duracion': pelicula['duration'],
                    'sinopsis': pelicula2['description'],
                    'sinopsis_es': pelicula['description'],
                    'idFicha': 'Film-' + pelicula['id'],

                    }
            logger.debug('Finalmente nos queda ')
            log_datos(item)
        else:
            return None


        return item


    def tituloes_moviedb(self, idFicha=None, **kwargs):
        # conn.request("GET", "/3/find/%7Bexternal_id%7D?external_source=imdb_id&language=en-US&api_key=%3C%3Capi_key%3E%3E", payload)
        ruta_img = "https://image.tmdb.org/t/p/w300_and_h450_bestv2"
        conn = http.client.HTTPSConnection("api.themoviedb.org")
        print ('Entro en datos_peli_mviedb')
        payload = "{}"
        clave = '6954e616bbca6eb84ea9de73788e6e5f'
        pelicula = []
        idFicha = idFicha.replace('Imdb-', '')
        conn.request("GET", "/3/find/" + idFicha + "?external_source=imdb_id&language=es-ES&api_key=" + clave, payload)
        res = conn.getresponse()
        data = res.read()

        ##    print (peli)
        ##    for p in peli:
        ##        #print (p)
        ##        print ('----------------------------------------')
        ##        for key, value in p.iteritems():
        ##
        ##            print (key,value)
        if data:
            pelic = json.loads(data)
            peli = pelic["movie_results"]
            return peli[0]["title"]
        else:
            return None


    def nombre_imdb(self, idFicha):

        urlx = "https://www.imdb.com/title/" + idFicha + "/?ref_=nv_sr_1"

        req = requests.get(urlx)

        html_t = BeautifulSoup(req.text, "html.parser")

        enlaces = html_t.find('div', {'class': 'title_wrapper'})
        nombre = enlaces.find('h1', {'itemprop': 'name'})
        print (nombre.text)
        anio = nombre.find('a').text
        nombre_mio = re.search(r'(.+)(\([0-9]{4}\))', unicode(nombre.text))
        if not nombre_mio:
            nombre_mio = None
            logger.warning("nombre_mio no encontrado")
        else:
            nombre_mio = nombre_mio.group(1)
            nombre_mio = nombre_mio.replace(u"Â ", "")
            nombre_es = nombre_mio.strip()
        logger.debug("=========================")
        logger.debug(nombre_mio.strip())
        logger.debug(anio)
        logger.debug("=========================")

        item = {"nombre": nombre_es,
                "anio": anio}

        return item