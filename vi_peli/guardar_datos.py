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


    def insertar_peli (self, peli, proveedor):
        logger.debug(peli)
        existe_torrent = Lista_Pelis.objects.filter(torrent__exact=peli["torrent"])
        existe_enlace = Lista_Pelis.objects.filter(enlace__exact=peli["enlace"])
        if len(existe_torrent) == 0 and len(existe_enlace) == 0:
            titu_peli = renombra(peli["titulo"]).upper()
            logger.info(titu_peli)
            peli_ins = Lista_Pelis(titulo=titu_peli,
                                   titulo_orig=peli["titulo_orig"],
                                   enlace=peli["enlace"],
                                   imagen=peli["imagen"],
                                   anyo=peli["anio"],
                                   torrent=peli["torrent"],
                                   calidad=peli["calidad"],
                                   proveedor=proveedor,
                                   fecha_publicacion=peli["fecha"],
                                   sinopsis=peli["sinopsis"],
                                   tamanio=peli["tamanio"]
                                   )

            peli_ins.save()
            logger.debug('titulo-->' + peli["titulo"])

            try:
                existe_peli = Pelicula.objects.filter(titulo__iexact=peli["titulo"])
                logger.debug(existe_peli)

                if len(existe_peli) == 0:
                    ficha_peli = Peliculas_ficha()
                    ficha = ficha_peli.fichas_pelis(p_titulo=peli["titulo_orig"], p_titulo_es=peli["titulo"],
                                                    p_idFicha=None, p_anio=peli["anio"], p_sinopsis=peli["sinopsis"])
                    logger.debug('Ficha Encontrada -->')
                    logger.debug(ficha)
                    if ficha <> None:
                        try:
                            existe_ficha = Pelicula.objects.filter(idFicha__exact=ficha["idFicha"])
                            logger.debug(existe_ficha)
                        except:
                            logger.error("Error al buscar el idficha" + ficha["idFicha"])
                            existe_ficha = None
                            # print ('Peli Repe --> ' + str(existe_ficha))
                    else:
                        logger.warning("NO SE HA ENCONTRADO LA PELICULA " + peli["titulo"])

                    if len(existe_ficha) > 0:
                        logger.info('La peli existe, actualizo el idFicha ' + ficha["idFicha"])
                        peli_ins.idFicha = ficha["idFicha"]
                        peli_ins.save()
                    elif ficha <> None:

                        if ficha["imagen"] <> None:
                            URL = ficha["imagen"]
                            punto = URL[-5:].find('.') + 1 - 5
                            extension = URL[punto:]
                            data = urlopen(URL).read()
                            file = StringIO(data)
                            imagen_ficha = Image.open(file)
                            nombre = ficha["idFicha"]
                            ruta_imagen = '/Imagenes/' + nombre + '.' + extension
                            logger.debug(ruta_imagen)
                            try:
                                imagen_ficha.save(MEDIA_ROOT + '/' + nombre + '.' + extension)
                            except:
                                ruta_imagen = ficha["imagen"]
                                logger.error('Error al grabar la imagen')
                            logger.debug("Grabo imagen --> " + nombre)
                            # print (imagen_ficha)
                            # foto = SimpleUploadedFile(nombre+'.'+extension, file.read(),"image/jpeg")
                        else:
                            ruta_imagen = None

                        logger.debug("Voy a grabar la Ficha")
                        titu_peli = renombra(ficha["titulo"]).upper()
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
                                             idFicha=ficha["idFicha"])

                        ficha_ins.save()
                        logger.info ("Grabado en PELICULA")
                        if ficha["idFicha"] <> None:
                            logger.info("Voy a grabar el idficha " + ficha_ins.idFicha)
                            peli_ins.idFicha = ficha_ins.idFicha
                            peli_ins.save()
                            logger.debug("grabado el idficha")

                    else:
                        logger.error("Pelicula no encontrada -->" + peli["titulo"])
                else:
                    # Si la ficha de la peli ya existe, lo grabamos en el listado.
                    logger.debug(existe_peli.idFicha)
                    peli_ins.idFicha = existe_peli.idFicha
                    peli_ins.save()

                if ficha_ins.idFicha == None:
                    peli_ins.idFicha = "Non-"+str(ficha_ins.id)
                    ficha_ins.idFicha = "Non-"+str(ficha_ins.id)

                    # Grabo la imagen sacada de NewPct1
                    logger.info ("imagen --> " + peli_ins.imagen)
                    if peli_ins.imagen <> None:
                        URL = peli_ins.imagen
                        punto = URL[-5:].find('.') + 1 - 5
                        extension = URL[punto:]
                        data = urlopen(URL).read()
                        file = StringIO(data)
                        imagen_ficha = Image.open(file)
                        nombre = ficha_ins.idFicha
                        ruta_imagen = '/Imagenes/' + nombre + '.' + extension
                        logger.debug(ruta_imagen)
                        try:
                            imagen_ficha.save(MEDIA_ROOT + '/' + nombre + '.' + extension)
                        except:
                            ruta_imagen = ficha_ins.idFicha
                            logger.error('Error al grabar la imagen')
                        logger.debug("Grabo imagen --> " + nombre)
                    else:
                        ruta_imagen = None

                    if ruta_imagen <> None:
                        ficha_ins.imagen = ruta_imagen

                    logger.info("imagen 2--> " + ficha_ins.imagen)
                    peli_ins.save()
                    ficha_ins.save()
            except:
                logger.error("Error en busqueda de pelicula")
                logger.error(sys.exc_info())

        else:
            logger.warning('Existe torrent o enlance en la bbdd')
            # Grabo la pelicula en la tabla PELICULAS.
    def guardar_hilo (pelis, proveedor):
        print ("Ejecutando Hilo")
        for peli in pelis:
            print ("Peli -->" + peli["titulo"])
            self.insertar_peli(peli, proveedor)