from django.template.loader import render_to_string
from pure_pagination.paginator import Page, Paginator

from django import template

register = template.Library()

class Page(Page):
    def renderv(self):
        print ("Entro en RENDERV")
        return render_to_string('vi_peli/paginacion2.html', {
            'current_page': self,
            'page_obj': self,  # Issue 9 https://github.com/jamespacileo/django-pure-pagination/issues/9
            # Use same naming conventions as Django
        })