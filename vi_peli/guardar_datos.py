#coding=utf-8
from __future__ import unicode_literals
from Viserpel.settings import JSON_ROOT, BASE_DIR, STATIC_ROOT, MEDIA_ROOT, APP_DIR
from models import Lista_Pelis, Pelicula, MisPelis
from Provider_NewPct1 import NewPct, renombra, reemplaza
from peliculas_datos import Peliculas_ficha
import sys
from PIL import Image
from urllib import urlopen
from StringIO import StringIO
import logging
import logging.config
from Viserpel.settings import LOGGING

logging.config.dictConfig(LOGGING)
logger = logging.getLogger(__name__)


class BBDD():
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

    def insertar_peli (self, peli, proveedor):
        logger.debug(peli)
        existe_torrent = Lista_Pelis.objects.filter(torrent__exact=peli["torrent"])
        existe_enlace = Lista_Pelis.objects.filter(enlace__exact=peli["enlace"])
        if len(existe_torrent) == 0 and len(existe_enlace) == 0:
            titu_peli = renombra(peli["titulo"]).upper()
            logger.info(titu_peli)
            v_titulo_bes = self.prepara_titu(peli["titulo"])
            if peli["titulo_orig"] <> None:
                v_titulo_ben = self.prepara_titu(peli["titulo_orig"])
            else:
                v_titulo_ben = None

            peli_ins = Lista_Pelis(titulo=peli["titulo"],
                                   titulo_orig=peli["titulo_orig"],
                                   enlace=peli["enlace"],
                                   imagen=peli["imagen"],
                                   anyo=peli["anio"],
                                   torrent=peli["torrent"],
                                   calidad=peli["calidad"],
                                   proveedor=proveedor,
                                   fecha_publicacion=peli["fecha"],
                                   sinopsis=peli["sinopsis"],
                                   tamanio=peli["tamanio"],
                                   titulo_bes = v_titulo_bes,
                                   titulo_ben = v_titulo_ben,
                                   )

            peli_ins.save()
            logger.debug('titulo-->' + peli["titulo"])
            try:
                self.inserta_ficha(peli_ins)
            except:
                logger.error("Se ha producido un error al insertar la Ficha de la pelicula " + peli_ins.titulo)
                logger.error(sys.exc_info())


        else:
            logger.warning('Existe torrent o enlance en la bbdd')
            # Grabo la pelicula en la tabla PELICULAS.

    def inserta_ficha (self, peli):
        logger.debug ("--------------------------------------INSERTA FICHA---------------------------------------------")
        logger.debug (peli.titulo)
        logger.debug (peli.titulo_orig)

        peli_ins = Lista_Pelis.objects.get(id=peli.id)
        logger.debug (peli_ins)
        logger.debug(peli_ins.idFicha)
        logger.debug(peli_ins.titulo_bes)
        logger.debug(peli_ins.id)
        try:
            # Comprobamos si existe la ficha.
            try:

                logger.debug (peli.titulo_bes)
                existe_peli = Pelicula.objects.get(titulo_bes__iexact=peli.titulo_bes)
                logger.debug(existe_peli)
                logger.debug(existe_peli.idFicha)
                logger.debug(existe_peli.id)

            except:
                logger.error("Error en existe_peli")
                logger.error(sys.exc_info())
            # Si no existe por la busqueda en Español, buscamos con el titulo original.
            if existe_peli and peli.titulo_ben<> None:
                try:
                    existe_peli = Pelicula.objects.get(titulo_ben__iexact=peli.titulo_ben)
                except:
                    logger.error("Error en existe_peli2")
                    logger.error(sys.exc_info())

            # Si no lo hemos encontrado
            if existe_peli: #
                ficha_peli = Peliculas_ficha()
                ficha = ficha_peli.fichas_pelis(p_titulo=peli.titulo_orig, p_titulo_es=peli.titulo, p_idFicha=None, p_anio=peli.anyo, p_sinopsis=peli.sinopsis)
                logger.debug('Ficha Encontrada -->')
                logger.debug(ficha)
                if ficha <> None:
                    try:
                        logger.debug (ficha["idFicha"])
                        logger.debug (peli.idFicha)
                        existe_ficha = Pelicula.objects.filter(idFicha__in=ficha["idFicha"])
                        logger.debug(existe_ficha)
                    except:
                        logger.error("No se ha encontrado la idficha" + ficha["idFicha"])
                        existe_ficha = None
                        # print ('Peli Repe --> ' + str(existe_ficha))
                else:
                    logger.error("NO SE HA ENCONTRADO LA PELICULA " + peli["titulo"])

                if len(existe_ficha) > 0:
                    logger.info('La peli existe, actualizo el idFicha a ' + ficha["id"])
                    peli_ins.idFicha = str(ficha["id"])
                    peli_ins.save()
                elif ficha <> None:

                    if ficha["imagen"] <> None:
                        nombre_img = ficha["idFicha"]
                        ruta_imagen = self.guarda_imagen(ficha["imagen"], nombre_img)
                    else:
                        ruta_imagen = None

                    logger.debug("Voy a grabar la Ficha")
                    titu_peli = ficha["titulo"]
                    v_titulo_bes = self.prepara_titu(ficha["titulo"])
                    if peli["titulo_orig"] <> None:
                        v_titulo_ben = self.prepara_titu(ficha["titulo_orig"])
                    else:
                        v_titulo_ben = None
                    logger.debug(titu_peli)
                    ficha_ins = Pelicula(titulo=titu_peli,
                                         titulo_orig=ficha["titulo_orig"],
                                         generos=ficha["generos"],
                                         year=ficha["anio"],
                                         imagen=ruta_imagen,  # ficha["imagen"],
                                         # img = foto,
                                         pais=ficha["pais"],
                                         escritor=ficha["escritor"],
                                         director=ficha["director"],
                                         actores=ficha["actores"],
                                         duracion=ficha["duracion"],
                                         sinopsis=ficha["sinopsis"],
                                         sinopsis_es=ficha["sinopsis_es"],
                                         idFicha=ficha["idFicha"],
                                         titulo_bes=v_titulo_bes,
                                         titulo_ben=v_titulo_ben
                                         )

                    ficha_ins.save()
                    logger.info("Grabado en PELICULA")
                    if ficha["idFicha"] <> None:
                        logger.info("Voy a grabar el idficha " + ficha_ins.idFicha)
                        peli_ins.idFicha = str(ficha_ins.id)
                        peli_ins.save()
                        logger.debug("grabado el idficha")

                else:
                    logger.error("Pelicula no encontrada en los buscadores -->" + peli["titulo"])
                    #deberia guardarla en algul lado.
            else:
                # Si la ficha de la peli ya existe, grabamos en Lista_Pelis el idFicha.
                logger.debug(existe_peli["idFicha"])
                peli_ins.idFicha = str(existe_peli.id)
                peli_ins.save()
            #Si no se ha encontrado ficha grabamos
            if ficha_ins.idFicha == None:
                peli_ins.idFicha = str(ficha_ins.id)

                # Grabo la imagen sacada del proveedor
                logger.info("imagen --> " + peli_ins.imagen)
                if peli_ins.imagen <> None:
                    nombre_img = peli_ins.titulo+str(peli_ins.idFicha)
                    ruta_imagen = self.guarda_imagen(peli_ins.imagen, nombre_img)
                else:
                    ruta_imagen = None

                if ruta_imagen <> None:
                    ficha_ins.imagen = ruta_imagen
                    peli_ins.imagen = ruta_imagen

                logger.info("imagen 2--> " + ficha_ins.imagen)
                peli_ins.save()
                ficha_ins.save()
        except:
            logger.error("Error en busqueda de pelicula")
            logger.error(sys.exc_info())

    def guardar_hilo (self, pelis, proveedor):
        print ("Ejecutando Hilo")
        for peli in pelis:
            print ("Peli -->" + peli["titulo"])
            self.insertar_peli(peli, proveedor)

    def guarda_imagen (self, v_imagen, v_nombre):
        try:
            URL = v_imagen
            punto = URL[-5:].find('.') + 1 - 5
            extension = URL[punto:]
            data = urlopen(URL).read()
            file = StringIO(data)
            imagen_ficha = Image.open(file)
            ruta_imagen = '/Imagenes/' + v_nombre + '.' + extension
            logger.debug(ruta_imagen)
        except:
            logger.error("Se ha producido un error al guardar la Imagen de la pelicula")
            logger.error(sys.exc_info())
        try:
            imagen_ficha.save(MEDIA_ROOT + '/' + v_nombre + '.' + extension)
        except:
            ruta_imagen = v_imagen
            logger.error('Error al grabar la imagen')

        logger.debug("Grabo imagen --> " + v_nombre)

        return ruta_imagen
