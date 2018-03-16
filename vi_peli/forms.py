#coding=utf-8
from django import forms
from .models import Pelicula, Lista_Pelis


class PeliForm(forms.ModelForm):
    class Meta:
        model = Lista_Pelis
        fields = ('titulo', 'titulo_orig','anyo','calidad','proveedor',)



class FichaForm(forms.ModelForm):
    class Meta:
        model = Pelicula
        fields = ['titulo', 'titulo_orig', 'year', 'director', 'actores', 'sinopsis_es', 'sinopsis', 'escritor', 'pais', 'idFicha', 'imagen']

        labels = { 'titulo': u'Título',
                   'titulo_orig': u'Titulo original',
                   'year': u'Año',
                   'director':u'Director',
                   'actores':u'Actores',
                   'sinopsis_es': u'Sinopsis (Es)',
                   'sinopsis':u'Sinopsis',
                   'escritor':u'Escritor',
                   'pais': u'País',
                   'idFicha': u'ID Api',
                   'imagen': u'Ruta imagen'}

        widgets = {'actores': forms.TextInput(),
                   'imagen': forms.TextInput()
                   }

    def __init__(self, *args, **kwargs):
        super(FichaForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                    'class': 'form-control'
            })





"""
     fields = [
            'tipo_cliente',
            'nombre',
            'numero_documento',
            'direccion',
            'barrio',
            'telefono',
            'email',
            'ciudad',
            'nombre_contacto1',
            'telefono_contacto1',
            'nombre_contacto2',
            'telefono_contacto2',
            'nombre_contacto3',
            'telefono_contacto3',
        ]

        labels = {
            'tipo_cliente':'Tipo de Cliente',
            'nombre':'Nombre completo o razón social',
            'numero_documento':'Numero de identificación',
            'direccion':'Dirección',
            'barrio':'Barrio',
            'telefono':'Teléfono',
            'email':'Em@il',
            'ciudad':'Ciudad',
            'nombre_contacto1':'Nombre de Contacto',
            'telefono_contacto1':'Teléfono',
            'nombre_contacto2':'Nombre de Contacto 2',
            'telefono_contacto2':'Teléfono',
            'nombre_contacto3':'Nombre de Contacto 3',
            'telefono_contacto3':'Teléfono',
        }

        widgets = {
            'tipo_cliente':forms.Select(),
            'nombre':forms.TextInput(),
            'numero_documento':forms.TextInput(),
            'direccion':forms.TextInput(),
            'barrio':forms.TextInput(),
            'telefono':forms.TextInput(),
            'email':forms.TextInput(),
            'ciudad':forms.Select(),
            'nombre_contacto1':forms.TextInput(),
            'telefono_contacto1':forms.TextInput(),
            'nombre_contacto2':forms.TextInput(attrs={'required': False}),
            'telefono_contacto2':forms.TextInput(attrs={'required': False}),
            'nombre_contacto3':forms.TextInput(attrs={'required': False}),
            'telefono_contacto3':forms.TextInput(attrs={'required': False}),
        }
"""