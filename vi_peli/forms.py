from django import forms
from .models import Pelicula


class PeliForm(forms.ModelForm):
    class Meta:
        model = Pelicula
        fields = ('titulo', 'titulo_orig','id_imbd','generos','year','imagen','img','pais','escritor','director','actores','duracion','sinopsis','sinopsis_es')
