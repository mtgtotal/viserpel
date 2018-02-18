#coding=utf-8
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^carga/$', views.pagina_carga, name='pagina_carga'),
    url(r'^carga/guarda_total/(?P<proveedor>.+)$', views.guarda_total, name='guarda_total'),
    url(r'^carga/guarda_pelicula/(?P<proveedor>.+)/(?P<indice>.+)$', views.guarda_pelicula, name='guarda_pelicula'),
    url(r'^ficha/(?P<pk>[0-9]+)/$', views.ficha, name='ficha'),
    url(r'^busqueda/$', views.busqueda, name='busqueda'),



]