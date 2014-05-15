# -*- coding: utf-8 -*-
"""
@copyright   Copyright (c) 2013 Submit Consulting
@author      Angel Sullon (@asullom)
@package     sad

Descripcion: Tags para mostrar los menús dinámicos
"""
from django import template
from django.template import resolve_variable, Context
import datetime
from django.template.loader import render_to_string
from django.contrib.sessions.models import Session
from django.conf import settings
from apps.utils.security import DataAccessToken
from apps.space.models import Enterprise, Headquar

from django.template.defaultfilters import stringfilter

from apps.utils.messages import Message
from apps.utils.security import SecurityKey
from apps.sad.menus import Menus

register = template.Library()

@register.simple_tag
def load_menu(request, module):
	"""
	Interfáz del Método para cargar en variables los menús que se mostrará al usuario

	Usage::

		{% load_menu request 'MODULE_KEY' %}

	Definition::

        ('WEB', 'Web informativa'),
        ('VENTAS', 'Ventas'),
        ('BACKEND', 'Backend Manager'),

	Examples::

		{% load_menu request 'BACKEND' %}

	"""
	
	return Menus.load(request, module)

@register.simple_tag
def desktop(request):
	"""
	Interfáz del Método para renderizar el menú de escritorio

	Usage::
		
		{% desktop request %}

	Examples::

		{% desktop request %}

	"""
	
	return Menus.desktop(request)

@register.simple_tag
def desktop_items(request):
	"""
	Interfáz del Método para listar los items en el backend

	Usage::
		
		{% desktop_items request %}

	Examples::

		{% desktop_items request %}

	"""
	
	return Menus.desktop_items(request)


@register.simple_tag
def phone(request):
	"""
	Interfáz del Método para renderizar el menú de dispositivos móviles

	Usage::
		
		{% phone request %}

	Examples::

		{% phone request %}
	"""
	
	return Menus.phone(request)

@register.simple_tag
def side_items(request):
	"""
	Interfáz del Método para listar los items en el sidebar

	Usage::
		
		{% side_items request %}

	Examples::

		{% side_items request %}

	"""
	
	return Menus.side_items(request)

@register.simple_tag
def get_grupos(request, url):
	"""
	Genera el menú de Grupos para imprimirlo en header.html

	Usage::
		
		{% get_grupos request get_url %}

	Examples::

        {% url 'mod_ventas_dashboard' as get_url %}
        {% get_grupos request get_url %}


	"""
	sede = None
	if DataAccessToken.get_headquar_id(request.session):
		try:
			sede = Headquar.objects.get(id=DataAccessToken.get_headquar_id(request.session))
		except:
			Message.error(request, ("Sede no se encuentra en la base de datos."))
		

	value = '' 
	w = ""
	d = DataAccessToken.get_grupo_id_list(request.session)
	if sede:
		w = (u'		<a href="#" class="dropdown-toggle" data-toggle="dropdown" title ="%s">%s > %s %s<b class="caret"></b></a>' % (sede.association.name, sede.enterprise.name, sede.name, value))
	
	o = ''
	if d :
		for i in d:
			print i
			o = o + (u'<li><a href="%s?grupo=%s">%s/%s</a></li>' % (url, i, sede.name, ""))
	if sede:
		o = o + (u'<li><a href="%s?">%s/Todas las areas</a></li>' % (url, sede.name))
	a = (u'<ul class="nav">'
	u'	<li class="dropdown">'
	u'		%s'
	u'		<ul class="dropdown-menu">' % (w))

	c = (u'		</ul>'
	u'	</li>'
	u'</ul>')
	return "%s%s%s" % (a, o, c)

