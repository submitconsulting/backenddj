# _*_ coding: utf-8 _*_
"""
@copyright   Copyright (c) 2014 Submit Consulting
@author      Angel Sullon (@asullom)
@package     utils

Descripcion: Registra en archivos .txt los sucesos ocultos del sistema
"""
from django.db import models

import logging, logging.handlers
import datetime
from django.utils.html import escape
from django.template.defaultfilters import removetags


from locale import setlocale, LC_ALL, LC_TIME
#from apps.helpers.util import EncodingFormatter
import sys
reload(sys)
sys.setdefaultencoding('utf-8') # esto es reemplazado por force_text
from django.utils.encoding import force_text
# setlocale(LC_TIME, '') #no se puede para mié tildes, no usar aqui
# print sys.getdefaultencoding()
# create logger
logger = logging.getLogger('logs')
logger.setLevel(logging.DEBUG)
# logger.setLevel(logging.INFO)

# create file handler and set level to debug
import os
from django.conf import settings
filedebug = 'temp/logs/log%s.txt' % (datetime.datetime.now().strftime("%Y-%m-%d"))
LOG_FILE = os.path.join(settings.BASE_DIR, filedebug)
fh = logging.FileHandler(LOG_FILE)  # , "a", encoding = "UTF-8" 
#fh.setLevel(logging.DEBUG)
# fh.setLevel(logging.INFO)

# create console handler and set level to debug
#ch = logging.StreamHandler()
#ch.setLevel(logging.DEBUG)
# ch.setLevel(logging.INFO)

# create formatter
formatter = logging.Formatter('[%(asctime)s][%(levelname)s] [%(name)s] %(message)s')
#formatter = logging.Formatter('%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s')
# formatter = logging.Formatter('[%(asctime)s.%(msecs)d][%(levelname)s] [%(name)s] %(message)s', datefmt='%m/%d/%Y %H:%M:%S')
# formatter = logging.Formatter('[%(asctime)s.%(msecs)d][%(levelname)s] [%(name)s] %(message)s', datefmt='%a, %d %b %y %H:%M:%S')
# formatter = EncodingFormatter('[%(asctime)s][%(levelname)s] [%(name)s] %(message)s', datefmt='%a, %d %b %y %H:%M:%S', encoding='utf-8') #, datefmt='%a, %d %b %y %H:%M:%S'
# add formatter to fh and ch
fh.setFormatter(formatter)
#ch.setFormatter(formatter)

# add fh and ch to logger
logger.addHandler(fh)
#logger.addHandler(ch)


class Logger:
    """
    Clase para la gestión de rastreo oculto del sistema

    Usage::

        from apps.utils.messages import Message
        Logger.info(request,"message")

    """
    
    @staticmethod
    def set_msg(request, name, msg):
        """
        Método interno, que deacuerdo al tipo de mensaje recibido en name, guarda en 
        logger.info() #por ejemplo.
        
        """
        
        
        # m = __import__ ('logger')
        
        methodToCall = getattr(logger, name)  # logger.debug donde name=debug p.e.
        methodToCall(("[%s][%s][%s] %s ") % (request.get_full_path(), request.user, request.META['REMOTE_ADDR'], removetags(msg, 'b')))  # logger.debug(msg) #(str(u'%s'%msg)).encode('utf-8')

    @staticmethod
    def debug(request, msg):
        # logger.debug("%s - %s"%(request.user, msg))
        Logger.set_msg(request, "debug", msg)

    @staticmethod
    def info(request, msg, audit=False):

        # logger.info("%s - %s"%(request.user, msg))
        Logger.set_msg(request, "info", msg)

    @staticmethod
    def warning(request, msg, audit=True):
        # logger.warning("%s - %s"%(request.user, msg))
        Logger.set_msg(request, "warning", msg)

    @staticmethod
    def error(request, msg, audit=True):
        # logger.error("%s - %s"%(request.user, msg))
        Logger.set_msg(request, "error", msg)
        

    @staticmethod
    def critical(request, msg, audit=True):
        # logger.critical("%s - %s"%(request.user, msg))
        Logger.set_msg(request, "critical", msg)

