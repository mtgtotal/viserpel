#coding=utf-8
from __future__ import unicode_literals
from Viserpel.settings import JSON_ROOT, BASE_DIR, STATIC_ROOT, MEDIA_ROOT, APP_DIR
from models import Lista_Pelis, Pelicula, MisPelis
from Provider_NewPct1 import NewPct
from auxiliar import renombra, reemplaza, log_datos, sinacento, prepara_titu
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



class BBDD():

    def insertar_peli (self, peli, proveedor):
        logger.debug ('Insertamos la pelicula en LISTA_PELIS')
        log_datos(peli)
        existe_torrent = Lista_Pelis.objects.filter(torrent__exact=peli["torrent"])
        existe_enlace = Lista_Pelis.objects.filter(enlace__exact=peli["enlace"])
        if len(existe_torrent) == 0 and len(existe_enlace) == 0:
            titu_peli = renombra(peli["titulo"]).upper()
            logger.info(titu_peli)
            v_titulo_bes = prepara_titu(peli["titulo"])
            if peli["titulo_orig"] <> None:
                v_titulo_ben = prepara_titu(peli["titulo_orig"])
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
            logger.info('Pelicula Grabada - titulo-->' + peli["titulo"])
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
        salir = False
        error = False
        #Recuperamos los datos de la pelicula para modificarlos.
        logger.debug ('Peli que buscamos:')
        logger.debug (peli)
        peli_ins = Lista_Pelis.objects.get(id=peli.id)
        logger.debug('Pelicula encontrada en LISTA_PELIS')
        logger.debug(peli_ins)
        log_datos(peli_ins)
        intento = 0
        if peli_ins.idFicha <> None:
            salir = True
            logger.debug ("La pelicula ya tiene ficha asignada")
        else:
            try:
                # Comprobamos si existe la ficha.
                logger.debug ('Comprobamos si existe la ficha.')
                try:
                    hay_ficha = 0
                    logger.debug (peli.titulo_bes)
                    # Primero comprobamos si la peli ya tiene una ficha asociada y ademas coincide el titulo_bes.
                    print (peli_ins.idFicha)
                    print ('tras peli_ins.idFicha')
                    if peli_ins.idFicha <> None:
                        intento = 1
                        logger.debug('intento nº--> '+str(intento))
                        logger.debug (peli_ins.idFicha)
                        logger.debug(peli_ins.idFicha.id)
                        #existe_ficha = peli_ins.lista_pelis_set.filter(titulo_bes = peli.titulo_bes)
                        existe_ficha = Pelicula.objects.filter(id=peli_ins.idFicha.id, titulo_bes = peli.titulo_bes)
                        logger.debug (existe_ficha)
                        if len(existe_ficha)==0:
                            hay_ficha = 0
                        else:
                            hay_ficha = len(existe_ficha)
                            existe_ficha_x = existe_ficha[0]
                            log_datos(existe_ficha_x)

                    #Segundo comprobamos con el titulo_bes
                    if hay_ficha == 0:
                        intento = 2
                        logger.debug('intento nº--> '+ str(intento))
                        logger.debug (peli.titulo_bes)
                        existe_ficha = Pelicula.objects.filter(titulo_bes__iexact=peli.titulo_bes)
                        logger.debug(existe_ficha)
                        if len(existe_ficha)==0:
                            hay_ficha = 0
                        else:
                            hay_ficha = len(existe_ficha)
                            for dato in existe_ficha:
                                log_datos (dato)
                    #Tercero comprobamos con el titulo_ben
                    if hay_ficha == 0 and peli.titulo_ben <> None:
                        intento = 3
                        logger.debug('intento nº--> ' + str(intento))
                        logger.debug(u'año --> ' + str(peli.anyo))
                        if peli.anyo <> None:
                            existe_ficha = Pelicula.objects.filter(titulo_ben__iexact=peli.titulo_ben, year = peli.anyo)
                        else:
                            existe_ficha = Pelicula.objects.filter(titulo_ben__iexact=peli.titulo_ben)
                        logger.debug (existe_ficha)
                        if len(existe_ficha)==0:
                            hay_ficha = 0
                        else:
                            hay_ficha = len(existe_ficha)
                            for dato in existe_ficha:
                                log_datos (dato)
                    # Modifico el idFicha de la Pelicula con el id de la Ficha.
                    if hay_ficha > 0:
                        salir = True
                        logger.debug ('Fichas encontradas --> ' + str(hay_ficha))
                        logger.debug (existe_ficha)
                        for x in existe_ficha:
                            logger.debug('La ficha de la peli ya existe, cogemos la primera, grabamos en Lista_Pelis el idFicha = ficha.id')
                            ficha_ins = x
                            logger.debug (ficha_ins)
                            break
                        #peli_ins.idFicha = ficha_ins
                        if peli_ins.idFicha == None:
                            logger.debug ('La pelicula no tiene ficha asignada, la asignamos')
                            logger.info ('Asignada la ficha ' + ficha_ins.titulo + " - " + str(ficha_ins.id) + " a la pelicula " + peli_ins.titulo + " - " + str (peli_ins.id))
                            ficha_ins.lista_pelis_set.add(peli_ins)
                        else:
                            logger.info('La pelicula tiene ficha asignada --> ' + str(peli_ins.idFicha.id) + "(" + peli_ins.idFicha.titulo + ")")
                        # Si lo encontramos por nombre en ingles, ponemos en Lista_pelis el titulo en Español.
                        if intento == 3:
                            logger.debug ('Actualizamos el titulo para ponerlo en Español en Lista_Pelis')
                            peli_ins.titulo = ficha_ins.titulo
                            peli_ins.save()



                except:
                    logger.error("Error en existe_ficha")
                    logger.error(sys.exc_info())
                    error = True
                if not salir and not error:
                    ficha_peli = Peliculas_ficha()
                    ficha = ficha_peli.fichas_pelis(p_titulo=peli.titulo_orig, p_titulo_es=peli.titulo, p_idFicha=None, p_anio=peli.anyo, p_sinopsis=peli.sinopsis)
                    logger.debug('Ficha Encontrada -->')
                    log_datos(ficha)
                    if ficha <> None:
                        # Comprobamos de nuevo si existe la Ficha, esta vez comparando el idFicha
                        try:
                            if ficha["idFicha"] <> None:
                                logger.debug (ficha["idFicha"])
                                logger.debug (peli.idFicha)
                                LidFicha = ficha["idFicha"].split(',')
                                logger.debug (LidFicha)
                                cuantos = len(LidFicha)
                                logger.debug (cuantos)
                                for x in LidFicha:
                                    logger.debug(x)
                                    existe_ficha = Pelicula.objects.filter(idFicha__contain = x)
                                    if len(existe_ficha) > 0:
                                        intento = 4
                                        logger.debug('intento nº--> ' + str(intento))
                                        logger.info ('Hemos encontrado la ficha ' + ficha["titulo"])
                                        logger.debug(existe_ficha.id)
                                        peli_ins.idFicha = existe_ficha
                                        peli_ins.save()
                                        salir = True
                                        break

                        except:
                            logger.error("No se ha encontrado la idficha" + ficha["idFicha"])
                            existe_ficha = None
                            # print ('Peli Repe --> ' + str(existe_ficha))
                    else:
                        logger.error("NO SE HA ENCONTRADO LA PELICULA " + peli["titulo"])

                    if ficha <> None and not salir:
                        intento = 5
                        logger.debug('intento nº--> ' + str(intento))

                        v_titulo_bes = prepara_titu(ficha["titulo"])

                        if ficha["titulo_orig"] <> None:
                            v_titulo_ben = prepara_titu(ficha["titulo_orig"])
                        else:
                            v_titulo_ben = None

                        logger.debug("Voy a grabar la Ficha")
                        titu_peli = ficha["titulo"]

                        ficha_ins = Pelicula(titulo=titu_peli,
                                             titulo_orig=ficha["titulo_orig"],
                                             generos=ficha["generos"],
                                             year=ficha["anio"],
                                             imagen= ficha["imagen"],
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

                        logger.debug('*** FICHA DE LA PELICULA ***')
                        log_datos(ficha_ins)
                        logger.debug ('VAMOS A GRABAR LA FICHA DE LA PELICULA')
                        ficha_ins.save()
                        logger.info("Grabada la ficha " + ficha_ins.titulo + " - " + str(ficha_ins.id))
                        peli_ins.idFicha = ficha_ins
                        peli_ins.save()
                        logger.info("Actualizada la pelicula " + peli_ins.titulo + " con la ficha " + str(ficha_ins.id))

                        """
                        if ficha["imagen"] <> None:
                            nombre_img = v_titulo_bes + '_' + str(ficha["id"])
                            ruta_imagen = self.guarda_imagen(ficha["imagen"], nombre_img)
                        else:
                            ruta_imagen = None
                        ficha_ins.imagen = ruta_imagen
                        ficha_ins.save()
                        """
                        logger.debug("grabado el idficha " + str(intento))
                    elif salir:
                        logger.debug ('salir')
                        #ficha_ins = existe_ficha
                        logger.info ("Se ha actualizado la pelicula con la ficha encontrada" + str (intento))
                    else:
                        logger.error("Pelicula no encontrada en los buscadores -->" + peli["titulo"])
                        #Nunca deberia darse este caso
                elif error:
                    logger.debug ("Salimos porque se ha producido un error tras el intento " + str(intento))
                else:
                    logger.debug ('Salimos ya que hemos encontrado la ficha en el principio '+ str(intento))
                    #ficha_ins = existe_ficha
            except:
                logger.error("Error en busqueda de pelicula tras el intento " + str(intento))
                logger.error(sys.exc_info())

            try:
                #Actualizo las imagenes en Pelicula y Ficha.
                if not error:
                    logger.debug('Comienzo el actualizar Imagenes Final')
                    logger.debug (peli_ins)
                    logger.debug(ficha_ins)
                    if ficha_ins.imagen <> None and ficha_ins.imagen.find("/Imagenes/") == -1:
                        nombre_img = ficha_ins.titulo_bes + '_' + str(ficha_ins.id)
                        ruta_imagen = self.guarda_imagen(ficha_ins.imagen, nombre_img)
                    elif ficha_ins.imagen <> None and ficha_ins.imagen.find("/Imagenes/") <> -1:
                        ruta_imagen =  ficha_ins.imagen
                    elif peli_ins.imagen <> None:
                        nombre_img = peli_ins.titulo_bes + '_' + str(peli_ins.idFicha.id)
                        ruta_imagen = self.guarda_imagen(peli_ins.imagen, nombre_img)
                        logger.debug (ruta_imagen)
                    else:
                        ruta_imagen = None

                    if ruta_imagen <> None:
                        if ficha_ins.imagen <> None and ficha_ins.imagen.find("/Imagenes/") == -1:
                            ficha_ins.imagen = ruta_imagen
                            ficha_ins.save()
                        if peli_ins.imagen <> None and peli_ins.imagen.find("/Imagenes/") == -1:
                            peli_ins.imagen = ruta_imagen
                            peli_ins.save()
                        if peli_ins.imagen <> None and ficha_ins.imagen == None:
                            ficha_ins.imagen = ruta_imagen
                            ficha_ins.save()
                        if peli_ins.imagen == None and ficha_ins.imagen <> None:
                            peli_ins.imagen = ruta_imagen
                            peli_ins.save()
                    logger.debug("Fin del grabado de la imagen en BBDD")
            except:
                logger.error ('Error al actualizar las imagenes.')
                logger.error(sys.exc_info())


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

    def limpia_imagenes(self):
        rootDir = MEDIA_ROOT
        for fullDir, subdirList, fileList in os.walk(rootDir, topdown=False):
            logger.debug (file)

