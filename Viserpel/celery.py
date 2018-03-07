
from __future__ import absolute_import

import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vi_peli.settings')  # Nota 1

from django.conf import settings  # Nota 2

app = Celery('CeleryApp')  # Nota 3

app.config_from_object('django.conf:settings')  # Nota 4
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)  # Nota 5

app.conf.update(BROKER_URL='django://',)

"""
from __future__ import absolute_import, unicode_literals
import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')

app = Celery('Viserpel_celery')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
"""