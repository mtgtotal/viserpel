#coding=utf-8
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone


DEFAULT_INDEX_TABLESPACE = "tables"

class Lista_Pelis (models.Model):
    titulo = models.TextField(db_tablespace="indexes")
    titulo_orig = models.TextField(default = titulo, blank=True, null=True)
    enlace = models.TextField(db_tablespace="indexes", unique=True)
    imagen = models.TextField(blank=True, null=True)
    fecha_busqueda = models.DateTimeField(default=timezone.now)
    fecha_publicacion = models.CharField(max_length=15, blank=True, null=True)
    anyo = models.CharField(max_length=4, blank= True, null=True)
    torrent = models.TextField(db_tablespace="indexes", unique=True)
    calidad = models.CharField(max_length=50, blank=True, null=True)
    proveedor = models.CharField(max_length=50, blank=True, null=True)
    sinopsis = models.TextField(blank=True, null=True)
    tamanio =  models.CharField(max_length=15, blank=True, null=True)
    idFicha = models.ForeignKey('vi_peli.Pelicula', db_column='idFicha', null=True, blank=True)
    #idFicha = models.IntegerField(null=True)
    titulo_bes = models.CharField(max_length=200,blank=True, null=True) #Titulo sin espacios ni ningún caracter <> numeros en español
    titulo_ben = models.CharField(max_length=200,blank=True, null=True) # Titulo sin espacios ni ningún caracter <> numeros en original

    def __str__(self):
        return self.titulo

class Pelicula(models.Model):
    idFicha = models.CharField(max_length=50,blank=True, null=True) #Nombre del proveedor (Imbd, Film, tmdb, ...) - Id del proveedor.
    titulo = models.CharField(max_length=200) #Titulo en español
    titulo_orig = models.CharField(max_length=200, blank=True, null=True) #Title
    generos = models.TextField(blank=True, null=True) #Genre
    year = models.IntegerField(blank=True,null=True) #Year
    imagen = models.TextField(blank=True, null=True) #Poster
    #img = models.ImageField (upload_to='Imagenes', verbose_name='Imagen', null=True)
    pais =  models.CharField(max_length=50, blank=True, null=True) #Pais
    escritor =  models.CharField(max_length=200, blank=True, null=True) #Writer
    director = models.CharField(max_length=200, blank=True, null=True) #Director
    actores = models.TextField(blank=True, null=True) #Actors
    duracion = models.CharField(max_length=15, blank=True, null=True) #Runtime
    sinopsis = models.TextField(blank=True, null=True) #Plot
    sinopsis_es = models.TextField(blank=True, null=True)  # Sinopsis
    f_alta = models.DateTimeField(default=timezone.now)
    titulo_bes = models.CharField(max_length=200,blank=True, null=True) #Titulo sin espacios ni ningún caracter <> numeros en español
    titulo_ben = models.CharField(max_length=200,blank=True, null=True) # Titulo sin espacios ni ningún caracter <> numeros en original


    def __str__(self):

        return self.titulo

class MisPelis(models.Model):
    titulo = models.CharField(max_length=200)  # Titulo en español
    titulo_orig = models.CharField(max_length=200, blank=True, null=True)  # Title
    idPeli = models.ForeignKey('vi_peli.Pelicula', related_name='mipeli', null=True, blank=True)
    calidad = models.CharField(max_length=50, blank=True, null=True)
    tipo =  models.CharField(max_length=50, blank=True, null=True)
    directorio = models.TextField()

    def __str__(self):
        return self.titulo

#Distintos Géneros de películas, en desc_generos se incluye una lista con todos los posibles nombres del genero en particular.
class Generos(models.Model):
    id_gen = models.CharField(max_length=20)
    nom_genero = models.CharField(max_length=200)
    desc_generos = models.TextField(max_length=200, blank=True, null=True)


    def __str__(self):
        return self.id_gen

class Calidades(models.Model):
    nombre = models.CharField(max_length=200)
    otros_nombres = models.TextField(blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)
    calidad = models.CharField(max_length=50, blank=True, null=True)
    audio = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.id_gen
# Create your models here.
