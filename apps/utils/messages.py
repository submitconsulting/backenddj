# _*_ coding: utf-8 _*_
"""
@copyright   Copyright (c) 2014 Submit Consulting
@author      Angel Sullon (@asullom)
@package     utils

Descripcion: Registra en archivos .txt, según el tipo de mensaje, las acciones de los usuarios
"""
from django.db import models

import logging, logging.handlers
import datetime
from django.utils.html import escape
from django.template.defaultfilters import removetags
import string


from locale import setlocale, LC_ALL, LC_TIME
#from apps.helpers.util import EncodingFormatter
import sys
reload(sys)
sys.setdefaultencoding('utf-8') # esto es reemplazado por force_text
from django.utils.encoding import force_text
# setlocale(LC_TIME, '') #no se puede para mié tildes, no usar aqui
# print sys.getdefaultencoding()
# create logger
logger = logging.getLogger('sistema')
logger.setLevel(logging.DEBUG)
# logger.setLevel(logging.INFO)

# create file handler and set level to debug
import os
from django.conf import settings
filedebug = 'temp/logs/audit%s.txt' % (datetime.datetime.now().strftime("%Y-%m-%d"))
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

from django.contrib import messages

class Message:
    """
    Clase para la gestión de mensajería instantánea del sistema

    Usage::

        from apps.utils.messages import Message
        Message.info(request,"message")

    """
    
    @staticmethod
    def set_msg(request, name, msg, audit=False):
        """
        Método interno, que asigna el mensaje en la variable messages de django
        y, deacuerdo al tipo de mensaje recibido en name, guarda en 
        logger.info() #por ejemplo.
        
        Level Constant    Value
DEBUG    10
INFO    20
SUCCESS    25
WARNING    30
ERROR    40

messages.debug(request, '%s SQL statements were executed.' % count) # no imprime
messages.info(request, 'Three credits remain in your account.')
messages.success(request, 'Profile details updated.')
messages.warning(request, 'Your account expires in three days.')
messages.error(request, 'Document deleted.')
        """
        messagesToCall = getattr(messages, "info")
        messagesToCall(request, (u''
            u'<div class="alert alert-block alert-%s"><button type="button" class="close" data-dismiss="alert">×</button>%s</div>'
            u'' % (name, force_text(msg)))
            )
        
        # m = __import__ ('logger')
        if audit:
            methodToCall = getattr(logger, name)  # logger.debug donde name=debug p.e.
            methodToCall(("[%s][%s][%s] %s ") % (request.get_full_path(), request.user, request.META['REMOTE_ADDR'], removetags(msg, 'b')))  # logger.debug(msg) #(str(u'%s'%msg)).encode('utf-8')

    @staticmethod
    def debug(request, msg, audit=True):
        # logger.debug("%s - %s"%(request.user, msg))
        Message.set_msg(request, "debug", msg, audit)

    @staticmethod
    def info(request, msg, audit=False):

        # logger.info("%s - %s"%(request.user, msg))
        Message.set_msg(request, "info", msg, audit)

    @staticmethod
    def warning(request, msg, audit=True):
        # logger.warning("%s - %s"%(request.user, msg))
        Message.set_msg(request, "warning", msg, audit)

    @staticmethod
    def error(request, msg, audit=True):
        # logger.error("%s - %s"%(request.user, msg))
        Message.set_msg(request, "error", msg, audit)
        

    @staticmethod
    def critical(request, msg, audit=True):
        # logger.critical("%s - %s"%(request.user, msg))
        Message.set_msg(request, "critical", msg, audit)

