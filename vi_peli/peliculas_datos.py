#coding=utf-8
import omdb
import python_filmaffinity
import logging
import logging.config
from Viserpel.settings import LOGGING
import http.client
import json

logging.config.dictConfig(LOGGING)
#fichero_log = os.path.join(APP_DIR, 'log', 'vi_peli.log')
logger = logging.getLogger(__name__)

class Peliculas_ficha():

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

        print ("***************************************************")
        for key, value in peli.iteritems():
            print (key, value)

        return peli

    def datos_peli_moviedb(self, titulo=None, idFicha=None, anio=None, sinopsis=None, titulo_es=None, **kwargs):

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
            tit = self.transforma(v_titulo)
            if anio <> None:
                year = "year=" + str(anio) + "&"
            else:
                year = ""

            conn.request("GET",
                         "/3/search/movie?" + year + "include_adult=false&page=1&query=" + tit + "&language=" + v_idioma + "&api_key=" + clave,
                         payload)
            res = conn.getresponse()
            data = res.read()

            print (data)
            cadena_json = json.loads(data)
            resultados = int(cadena_json["total_results"])
            if resultados == 0:
                print ("Sin resultados")
                return None
            print (resultados)
            pelis = cadena_json["results"]
            print (pelis)
            logger.debug('PELI')
            numero = 1
            for pelic in pelis:
                # print (pelic)

                if self.sinacento(v_titulo).upper() == self.sinacento(pelic["title"]).upper():
                    encontrado = True
                    v_idFicha = str(pelic['id'])
                    conn.request("GET", "/3/movie/" + v_idFicha + "?language=es-ES&api_key=" + clave, payload)
                    res2 = conn.getresponse()
                    data2 = res2.read()
                    peli = json.loads(data2)
                    logger.debug('FICHA')
                    for key, value in pelic.iteritems():
                        print (key, value)
                    vapikey = 'c3ca59d0'
                    omdb.set_default('apikey', vapikey)
                    logger.debug('FICHA_IMBD')
                    peli_imbd = omdb.imdbid(peli["imdb_id"])
                    for key, value in peli_imbd.iteritems():
                        print (key, value)
                    break
                if encontrado == False and numero == 1 and pelic["overview"] <> "":
                    logger.debug('Guardamos el primer registro encontrado')
                    v_idFicha = str(pelic['id'])
                    conn.request("GET", "/3/movie/" + v_idFicha + "?language=es-ES&api_key=" + clave, payload)
                    res2 = conn.getresponse()
                    data2 = res2.read()
                    peli1 = json.loads(data2)
                    logger.debug(peli1)
                    for key, value in peli1.iteritems():
                        print (key, value)
                    vapikey = 'c3ca59d0'
                    omdb.set_default('apikey', vapikey)
                    logger.debug('FICHA_IMBD')
                    print (peli1["imdb_id"])
                    peli_imbd1 = omdb.imdbid(peli1["imdb_id"])
                    for key, value in peli_imbd1.iteritems():
                        print (key, value)
                    numero = numero + 1

            if encontrado == False:
                logger.warning('CUIDADO!! Quizás no coicida la pelicula')
                peli = peli1
                peli_imbd = peli_imbd1

        generos = ""
        anio = peli_imbd.year
        imagen = peli_imbd.poster
        if imagen == None or imagen == "":
            imagen = ruta_img + peli["poster_path"]
        escritor = peli_imbd.writer
        director = peli_imbd.director
        actores = peli_imbd.actors
        sinopsis_en = peli_imbd.plot
        pais = peli_imbd.country
        for g in peli["genres"]:
            generos = generos + "," + unicode(g["name"])
        generos = generos[1:]

        if peli:

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
                    'idFicha': 'Imdb-' + str(peli["imdb_id"]) + "," + "movdb-" + str(peli["id"]),

                    }
        else:
            return None

        return item

    def datos_peli_imbd(self, titulo=None, idFicha=None, anio=None, sinopsis=None, titulo_es=None):
        # type: (object, object, object) -> object
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
        else:
            return None

        return item

    def datos_peli_film(self, titulo=None, idFicha=None, anio=None, sinopsis=None, titulo_es=None):
        # type: (object, object, object) -> object
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
        else:
            return None


        return item



