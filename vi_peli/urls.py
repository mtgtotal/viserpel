#coding=utf-8
from django.conf.urls import url

from . import views
from vi_peli.views import ModificarFicha, Prueba

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^carga/$', views.pagina_carga, name='pagina_carga'),
    url(r'^listar_pelis/$', views.listar_pelis, name='listar_pelis'),
    url(r'^carga/guarda_total/(?P<proveedor>.+)$', views.guarda_total, name='guarda_total'),
    url(r'^carga/guarda_pelicula/(?P<proveedor>.+)/(?P<indice>.+)$', views.guarda_pelicula, name='guarda_pelicula'),
    url(r'^ficha/(?P<pk>[0-9]+)/(?P<tabla>[a-zA-Z]+)$', views.ficha, name='ficha'),
    url(r'^busqueda/$', views.busqueda, name='busqueda'),
    url(r'^modificar_ficha/(?P<pk>.+)/$',  ModificarFicha.as_view(), name="modificar_ficha"),
    url(r'^actualiza_pelis/$', views.actualiza_pelis, name='actualiza_pelis'),
    url(r'^limpia_imagenes/$', views.limpia_imagenes, name='limpia_imagenes'),
    url(r'^act_peli/(?P<pk>[0-9]+)/$', views.act_peli, name='act_peli'),
    url(r'^modificarficha/(?P<pk>[0-9]+)/$', views.ficha_edit, name="ficha_edit"),
    url(r'^prueba/$', Prueba.as_view(), name="prueba"),

]