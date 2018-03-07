# app_mail/tasks.py
from Viserpel.celery import app
from guardar_datos import BBDD
import logging.config
from Viserpel.settings import LOGGING
logging.config.dictConfig(LOGGING)
#fichero_log = os.path.join(APP_DIR, 'log', 'vi_peli.log')
logger = logging.getLogger(__name__)

@app.task
def guardar_hilo(pelis, proveedor):
    logger.info ("Ejecutando Hilo")
    for peli in pelis:
        logger.info ("Peli -->" + peli["titulo"])
        BBDD().insertar_peli(peli, proveedor)