# -*- coding: utf-8 -*-
"""
@copyright   Copyright (c) 2013 Submit Consulting
@author      Angel Sullon (@asullom)
@package     utils

Descripcion: Filtros se seguridad de la información

"""
from django import template
#from django.contrib.sessions.models import Session
#from django.conf import settings
#from django.template.defaultfilters import stringfilter
from apps.utils.security import SecurityKey

register = template.Library()

# @stringfilter

@register.filter
def key(uid, action_name):
	"""
	Muestra la llave de seguridad generada por la clase SecurityKey

	Usage::

		{% url 'controller_name' id_value|key:'action_name' %}

	Example::

		{% url 'locality_edit' d.id|key:'locality_upd' %}

	"""
	
	return SecurityKey.get_key(uid, action_name)

