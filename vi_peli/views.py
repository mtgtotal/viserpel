#coding=utf-8
from __future__ import unicode_literals
from django.shortcuts import render
import json
from django.shortcuts import redirect, render_to_response,  get_object_or_404
from Viserpel.settings import JSON_ROOT, BASE_DIR, STATIC_ROOT, MEDIA_ROOT, APP_DIR
from models import Lista_Pelis, Pelicula, Generos, Calidades
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
from task import guardar_hilo
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
#from pure_pagination.paginator import Paginator as Paginator2, EmptyPage as EmptyPage2, PageNotAnInteger as PageNotAnInteger2
from pure_pagination.paginator import Paginator as Paginator2, Page
from django.views.generic import ListView






#from django.views.generic.list_detail import object_list

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
    letras = ['Todas','0-9','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','Otros']
    numeros = ['0','1','2','3','4','5','6','7','8','9']

    letra = request.GET.get('letra','Todas')

    if letra == '0-9':
        pelisbd = Pelicula.objects.filter(reduce(lambda x, y: x | y, [Q(titulo__startswith=item) for item in numeros]))
        # q = q.filter((Q(titulo__startswith="0") | Q(titulo__startswith="1") | Q(titulo__startswith="2") | Q(titulo__startswith="3") | Q(titulo__startswith="4") | Q(titulo__startswith="5") | Q(titulo__startswith="6") | Q(titulo__startswith="7") | Q(titulo__startswith="8") | Q(titulo__startswith="9")))
    elif letra == 'Otros':
        pelisbd = Pelicula.objects.filter((Q(titulo__startswith=u"¿") | Q(titulo__startswith=u"¡") | Q(titulo__startswith=u"#")))
    elif letra <> "Todas" and letra <> '0-9' and letra <> 'Otros':
        print (letra)
        pelisbd = Pelicula.objects.filter(titulo__startswith = letra)
    else:
        pelisbd = Pelicula.objects.order_by('titulo', 'year')
    print (pelisbd)


    """
    paginator = Paginator(pelisbd, 80)
    

    try:
        pelis = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        pelis = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        pelis = paginator.page(paginator.num_pages)
    """
    try:
        page_num = request.GET.get('page', 1)
        page_num = int(page_num)
    except PageNotAnInteger:
        page = 1
        page_act = 1

    p = Paginator2(pelisbd, 60,  request=request)
    #page = p.page(page)
    page = p.page(page_num)
    page_act = page.number

    parametros = request.GET.copy()
    print (parametros)

    if parametros.has_key('page'):
        del parametros['page']

    return render_to_response('vi_peli/index.html', {"page": page, "letras":letras, "letra_act":letra, "page_act":page_act, "parametros":parametros})

  #  peli_ant = ""
  #  imagen_ant = ""
  #  misprov = []
  #  mispelis = []

   # mispelis = pelisbd
   # return render(request, 'vi_peli/index.html', {'pelis': mispelis})


def listar_pelis (request):
    letras = ['Todas','0-9','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','Otros']
    numeros = ['0','1','2','3','4','5','6','7','8','9']
    letra = request.GET.get('letra','Todas')

    #pelis = lpelis
    logger.debug ('listar pelis')
    parametros = None
    if letra == '0-9':
        lpelis = Lista_Pelis.objects.filter(reduce(lambda x, y: x | y, [Q(titulo__startswith=item) for item in numeros])).order_by("titulo")
        # q = q.filter((Q(titulo__startswith="0") | Q(titulo__startswith="1") | Q(titulo__startswith="2") | Q(titulo__startswith="3") | Q(titulo__startswith="4") | Q(titulo__startswith="5") | Q(titulo__startswith="6") | Q(titulo__startswith="7") | Q(titulo__startswith="8") | Q(titulo__startswith="9")))
    elif letra == 'Otros':
        lpelis = Lista_Pelis.objects.filter((Q(titulo__startswith=u"¿") | Q(titulo__startswith=u"¡") | Q(titulo__startswith=u"#"))).order_by("titulo")
    elif letra <> "Todas" and letra <> '0-9' and letra <> 'Otros':
        print (letra)
        lpelis = Lista_Pelis.objects.filter(titulo__startswith = letra).order_by("titulo")
    else:
        lpelis = Lista_Pelis.objects.order_by('titulo', 'anyo')

    try:
        page_num = request.GET.get('page', 1)
        page_num = int(page_num)
    except PageNotAnInteger:
        page = 1
        page_act = 1

    #lpelis = Lista_Pelis.objects.order_by('titulo')
    print (lpelis)
    tit_pelis = []
    for i in lpelis:

        tit_pelis.append(i.titulo)


    p = Paginator2(lpelis, 60,  request=request)
    #pelis = p.page(page)
    page = p.page(page_num)
    page_act = page.number

    parametros = request.GET.copy()
    print (parametros)

    if parametros.has_key('page'):
        del parametros['page']
    """
    paginator = Paginator(lpelis, 80)

    page = request.GET.get('page')

    try:
        pelis = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        pelis = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        pelis = paginator.page(paginator.num_pages)
        
    """
    return render_to_response('vi_peli/lista_pelis.html', {"page": page, "page_act":page_act, "letras":letras, "letra_act":letra, "parametros":parametros})
    #return render(request, 'vi_peli/lista_pelis.html', {'pelis': pelis})



def busqueda (request):
    lista_generos =  Generos.objects.order_by('nom_genero')
    lista_calidad =  Calidades.objects.order_by('id')
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
    parametros = None

    if titulo or letra or anio or generos or calidad:
        resultados = C_Busqueda().busca_bbdd(vtitulo=titulo, vletra=letra, vyear=anio, lgeneros=generos, lcalidad=calidad)

        parametros = request.GET.copy()
        print (parametros)

        if parametros.has_key('page'):
            del parametros['page']

        """
        paginator = Paginator(resultados, 40)
        page = request.GET.get('page')

        try:
            pelis = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            pelis = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            pelis = paginator.page(paginator.num_pages)
        """
        try:
            page_num = request.GET.get('page', 1)
            page_num = int(page_num)
        except PageNotAnInteger:
            page = 1
            page_act = 1

        p = Paginator2(resultados, 60, request=request)
        # page = p.page(page)
        page = p.page(page_num)
        page_act = page.number

    else:
        page = 1
        page_act = 1

#titulo={{titulo}}&anio={{anio}}&letra={{letra}}&Generos={{generos}}&Calidad
    return render_to_response("vi_peli/busqueda.html", {"page": page, "page_act":page_act ,"lista_generos":lista_generos, "lista_calidad":lista_calidad, "parametros":parametros})
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
                nombre = 'MejorTorrent_Todo'
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


                logger.debug("Paginas antes --> " + str(npag))

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
                    todasPelis = []
                logger.info ("Cargado JSON")

                for peli in data:
                    existe_peli = Lista_Pelis.objects.filter(torrent__iexact = peli["torrent"])
                    if len(existe_peli)==0:
                        todasPelis.append(peli)

                results = todasPelis

        else:
            tipoCarga = ""
            results = []
    else:
        proveedor = ""
        tipoCarga = ""
        results = []

    try:
        page_num = request.GET.get('page', 1)
        page_num = int(page_num)
    except PageNotAnInteger:
        page = 1
        page_act = 1

    p = Paginator2(results, 60, request=request)
    # page = p.page(page)
    page = p.page(page_num)
    page_act = page.number

    return render_to_response("vi_peli/pagina_carga.html", {"page": page, "page_act":page_act, "proveedor": proveedor,  "tipoCarga": tipoCarga })

def guarda_total(request, proveedor):
    logger.debug ('Guarda_total- Proveedor: '+ proveedor)
    archivo = JSON_ROOT + '/' + proveedor + '.json'
    if os.path.isfile(archivo):
        with open(archivo, 'r') as file:
            data = json.load(file)
            #t = threading.Thread(target=BBDD().guardar_hilo, args=(data,proveedor))
            #t.start()

            guardar_hilo.delay(data,proveedor)

            #for peli in data:
            #    BBDD().insertar_peli (peli, proveedor)
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


        peli = data[int(indice)]

        logger.debug(peli)
        BBDD().insertar_peli(peli, proveedor)


    return redirect  ('/')
    #return render("vi_peli/pagina_carga.html",{})

def ficha (request, pk):
    logger.info('Ficha')
    peli = get_object_or_404(Pelicula, pk=pk)
    logger.debug(peli.id)
    enlaces = Lista_Pelis.objects.filter(idFicha__exact=peli.id)
    logger.info (enlaces)
    if len(enlaces) == 0:
        logger.error("No hay enlaces")
        enlaces = None

    return render(request, 'vi_peli/ficha_peli.html', {'peli': peli, 'enlaces': enlaces})


def actualiza_pelis (request):
    lpelis = Lista_Pelis.objects.all()
    return redirect('/')

def act_peli (request, pk):

    print ("entro en act_peli para la pk--> " + str(pk))

    lpelis = Lista_Pelis.objects.get(id=pk)

    logger.debug (lpelis)
    logger.debug (lpelis.idFicha)
    logger.debug (lpelis.torrent)

    BBDD().inserta_ficha(lpelis)
    enlaces = None
    #return render(request, 'vi_peli/lista_pelis.html', {'lpelis': None})
    return render(request, 'vi_peli/ficha_peli.html', {'peli': lpelis, 'enlaces': enlaces})

def limpia_imagenes(request):
    rootDir = MEDIA_ROOT
    logger.debug(rootDir)

    for fullDir, subdirList, fileList in os.walk(rootDir, topdown=False):
        for fila in fileList:
            imagen = '/Imagenes/'+fila
            existe_imagen = Pelicula.objects.filter(imagen__iexact = imagen)
            existe_imagen2 = Lista_Pelis.objects.filter(imagen__iexact=imagen)
            if len (existe_imagen) == 0 and len(existe_imagen2) == 0 and imagen <> '/Imagenes/Logo_Viserpel1.png':
                logger.debug ('Hay que borrar la imagen '+ imagen)
                os.remove(rootDir+'/'+fila)


    return redirect('/')