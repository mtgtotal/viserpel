#coding=utf-8
from __future__ import unicode_literals
from django.shortcuts import render
import json
from django.shortcuts import redirect, render_to_response,  get_object_or_404
from Viserpel.settings import JSON_ROOT, BASE_DIR, STATIC_ROOT, MEDIA_ROOT, APP_DIR
from models import Lista_Pelis, Pelicula, Generos
import os
from Provider_NewPct1 import NewPct, renombra, reemplaza
from Provider_MejorTorrent import MejorTorrent
from busquedas import C_Busqueda
from peliculas_datos import Peliculas_ficha
import sys
from PIL import Image
from urllib import urlopen
from StringIO import StringIO
import logging
from guardar_datos import BBDD
import logging.config
from Viserpel.settings import LOGGING
import threading

logging.config.dictConfig(LOGGING)
#fichero_log = os.path.join(APP_DIR, 'log', 'vi_peli.log')
logger = logging.getLogger(__name__)
"""
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s : %(levelname)s : %(message)s',
                    filename = fichero_log,
                    )
"""

def index(request):
    # prueba = JSON_ROOTDçew
    miorder = 'titulo, year'
    pelisbd = Pelicula.objects.order_by('titulo', 'year')
    peli_ant = ""
    imagen_ant = ""
    misprov = []
    mispelis = []
    """for peli in pelisbd:
        print (peli)
        tit_peli = peli.titulo
        if peli_ant == "" or peli_ant <> tit_peli:
            if peli_ant <> "":
                mipeli = {'titulo': peli_ant, 'imagen':imagen_ant, 'datos':misprov}
                mispelis.append(mipeli)
            peli_ant = peli.titulo
            imagen_ant = peli.imagen
            prov = {'proveedor':peli.proveedor, 'torrent': peli.torrent, 'calidad':peli.calidad}
            misprov = misprov.append(prov)
        else:
            prov = {'proveedor': peli.proveedor, 'torrent': peli.torrent, 'calidad': peli.calidad}
            misprov = misprov.append(prov)
        #ultima peli
        mipeli = {'titulo': peli_ant, 'imagen': imagen_ant, 'datos': misprov}
        mispelis.append(mipeli)
        print (mispelis)
    """
    mispelis = pelisbd
    return render(request, 'vi_peli/index.html', {'pelis': mispelis})

def busqueda (request):
    lista_generos =  Generos.objects.order_by('nom_genero')
    #lista_calidad = llena_calidad()
    logger.debug ('entro en busqueda')
    titulo = None
    generos = None
    calidad = None
    letra = None
    anio = None

    titulo = request.GET.get('titulo', '')
    if titulo:
        logger.debug ('titulo: ' + str(titulo))
        titulo = titulo.strip()
    else:
        titulo = None

    generos = request.GET.get('Generos', '')
    if generos:
        logger.debug ('generos:')
        logger.debug (generos)
        generos = generos.strip()
    else:
        generos = None
    calidad = request.GET.get('Calidad', '')
    if calidad:
        calidad = calidad.strip()
        logger.debug ('calidades:')
        logger.debug(calidad)
    else:
        calidad = None
    letra = request.GET.get('letra', '')
    if letra:
        logger.debug ('letra: ' + str(letra))
        letra = letra.strip()
    else:
        letra = None
    anio = request.GET.get('anio', '')
    if anio:
        logger.debug('anio: ' + str(anio))
        anio = anio.strip()
    else:
        anio = None
    print ('titulo, letra, año, generos, calidad')
    print (titulo)
    print (letra)
    print (anio)
    print (generos)
    print (calidad)
    if titulo or letra or anio or generos or calidad:
        resultados = C_Busqueda().busca_bbdd(vtitulo=titulo, vletra=letra, vyear=anio, lgeneros=generos, lcalidad=calidad)
    else:
        resultados = None

    return render_to_response("vi_peli/busqueda.html", {"pelis_busqueda": resultados, "lista_generos":lista_generos})
    #return render("vi_peli/busqueda.html", {"pelis_busqueda": resultados})


def pagina_carga(request):
    logger.debug ("Pagina de Carga")
    proveedor = request.GET.get('prov', '')
    logger.debug ('Proveedor' + str(proveedor))
    if proveedor:
        tipoCarga = request.GET.get('tipoC','')
        npaginas = request.GET.get('pag', '')
        letras = request.GET.get('let', '')
        logger.debug(tipoCarga)
        logger.debug("Paginas antes --> " + str(npaginas))

        if tipoCarga:
            if proveedor == "NewPct1_HD":
                url = 'http://newpct1.com/peliculas-hd/'
                nombre = 'NewPct1_hd'
                clase = 'NewPct'
            elif proveedor == "NewPct1":
                url = 'http://newpct1.com/peliculas/'

                nombre = 'NewPct1'
                clase = 'NewPct'
            elif proveedor == "MejorTorrent":
                url = 'MejorTorrent'
                nombre = 'MejorTorrent'
                clase = 'MejorTorrent'
            elif proveedor == "MejorTorrent_HD":
                url = 'MejorTorrent_HD'
                nombre = 'MejorTorrent_HD'
                clase = 'MejorTorrent'
            elif proveedor == "MejorTorrent_Todo":
                url = 'MejorTorrent_Todo'
                nombre = 'MejorTorrent_Letra'
                clase = 'MejorTorrent'

            #----------------------------------------------
            if tipoCarga == "Web":
                if clase == "NewPct":
                    pelisjson = NewPct()
                elif clase == "MejorTorrent":
                    pelisjson = MejorTorrent()
                logger.debug ('Antes de Busca Pelis')

                if npaginas:
                    npag = str(npaginas)
                else:
                    npag = None

                if proveedor ==  "MejorTorrent_Todo":
                    if letras:
                        npag = letras
                    else:
                        npag = None


                print("Paginas antes --> " + str(npag))

                #ultimaPeli = Busca_ultima_peli(proveedor) #Buscamos la url de la última peli cargada

                ultimaPeli = None
                todasPelis = pelisjson.busca_pelis(url, ultimaPeli, npag)
                results = todasPelis
                with open(JSON_ROOT + '/' + nombre + '.json', 'w') as file:
                    json.dump(todasPelis, file)
                logger.info ("Guardado JSON")
            elif tipoCarga == "JSon":
                archivo = JSON_ROOT + '/' + nombre + '.json'
                logger.debug (archivo)
                with open(archivo, 'r') as file:
                    data = json.load(file)
                    todasPelis = data
                logger.info ("Cargado JSON")
                results = todasPelis

        else:
            tipoCarga = ""
            results = []
    else:
        proveedor = ""
        tipoCarga = ""
        results = []
    return render_to_response("vi_peli/pagina_carga.html", {"pelisjson": results, "proveedor": proveedor,  "tipoCarga": tipoCarga })

def guarda_total(request, proveedor):
    logger.debug ('Guarda_total- Proveedor: '+ proveedor)
    archivo = JSON_ROOT + '/' + proveedor + '.json'
    if os.path.isfile(archivo):
        with open(archivo, 'r') as file:
            data = json.load(file)
            #t = threading.Thread(target=BBDD().guardar_hilo, args=(data,proveedor))
            #t.start()
            guarda = BBDD().guardar_hilo(data,proveedor)
            #for peli in data:
            #    BBDD().insertar_peli (peli, proveedor)



    else:
        logger.info ("No hay nada para guardar")
        resultado = "No hay nada para guardar"

    return render(request, 'vi_peli/index.html', {})

def guarda_pelicula(request, proveedor, indice):
    archivo = JSON_ROOT + '/' + proveedor + '.json'
    if os.path.isfile(archivo):
        with open(archivo, 'r') as file:
            data = json.load(file)
        logger.debug('Indice --> '+ str(indice))
        print('Indice --> ' + str(indice))

        peli = data[int(indice)]
        print (peli)
        logger.debug(peli)
        BBDD().insertar_peli(peli, proveedor)


    return redirect  ('/')
    #return render("vi_peli/pagina_carga.html",{})

def ficha (request, pk):
    logger.info('Ficha')
    peli = get_object_or_404(Pelicula, pk=pk)
    logger.debug(peli.idFicha)
    enlaces = Lista_Pelis.objects.filter(idFicha__exact=peli.idFicha)
    logger.info (enlaces)
    if len(enlaces) == 0:
        logger.error("No hay enlaces")
        enlaces = None

    return render(request, 'vi_peli/ficha_peli.html', {'peli': peli, 'enlaces': enlaces})