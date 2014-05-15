# -*- coding: utf-8 -*-
"""
@copyright   Copyright (c) 2013 Submit Consulting
@author      Angel Sullon (@asullom)
@package     utils

Descripcion: Clases para controlar la seguridad de la información en la nube

"""
from apps.utils.messages import Message
import datetime
import random

import hashlib

from array import *
from django.shortcuts import redirect
#import sys
#reload(sys)
#sys.setdefaultencoding('utf-8')
from django.contrib.auth.models import User, Group, Permission 
from django.db.models import Q
from django.http import HttpResponse

class DataAccessToken:
	"""
		Clase que permite almacenar y recuperar los permisos a datos de las empresas solicitados por los usuarios.
	"""
	@staticmethod
	def set_association_id(request, association_id):
		request.session['association_id'] = association_id

	@staticmethod
	def get_association_id(session):
		return session.get('association_id', False)
	
	@staticmethod
	def set_enterprise_id(request, enterprise_id):
		request.session['enterprise_id'] = enterprise_id

	@staticmethod
	def get_enterprise_id(session):
		return session.get('enterprise_id', False)

	@staticmethod
	def set_headquar_id(request, headquar_id):
		request.session['headquar_id'] = headquar_id

	@staticmethod
	def get_headquar_id(session):
		return session.get('headquar_id', False)

	@staticmethod
	def set_grupo_id_list(request	, grupo_id_list):
		request.session['grupo_id_list'] = grupo_id_list

	@staticmethod
	def get_grupo_id_list(session):
		return session.get('grupo_id_list', False)

class SecurityKey:
	"""
		Clase que permite crear llave de seguridad en las url.
	"""
	TEXT_KEY = 'lyHyRajh987r.P~CFCcJ[AvFKdz|86'

	# Método para generar las llaves de seguridad
	@staticmethod
	def get_key(id, action_name):
		""" 
		Genera una llave de seguridad válida durante todo el día %Y-%m-%d

		Entrada::

			id=1
			action_name="user_upd"

		Salida::

			1.dfad09debee34f8e85fccc5adaa2dadb
	    """
		key = "%s%s" % (SecurityKey.TEXT_KEY, datetime.datetime.now().strftime('%Y-%m-%d'))

		m = hashlib.md5("%s%s%s" % (id, key, action_name))
		key = m.hexdigest()
		
		return u"%s.%s" % (id, key)

	# Método para verificar si la llave es válida
	@staticmethod
	def is_valid_key(request, key_value, action_name):
		""" 
		Genera una llave de seguridad válida durante todo el día %Y-%m-%d

		Entrada::

			key_value=1.dfad09debee34f8e85fccc5adaa2dadb
			action_name="user_upd"

		Salida::

			1
	    """
		key = key_value.split('.')
		_id = key[0]
		valid_key = SecurityKey.get_key(_id, action_name)
		valid = (True if valid_key == key_value else False)
		if not valid:
			# raise Exception(("Acceso denegado. La llave de seguridad es incorrecta."))
			Message.error(request, ('Acceso denegado. La llave de seguridad es incorrecta.'))
			return False
		# print 'key_value(%s) = valid_key(%s)' % (key_value, valid_key)
		# Message.info(request,('key_value(%s) = valid_key(%s)' % (key_value, valid_key)))
		return _id

class Redirect:
	"""
	Clase que permite re-dirigir a un controller, cuaya solicitud se haya realizado con ajax o no

	Antes::

		if request.is_ajax():
			request.path="/params/locality/index/" #/app/controller_path/action/$params
			return locality_index(request)
		else:
			return redirect("/params/locality/index/")
		

	Ahora solo use (Example)::

		return Redirect.to(request, "/sad/user/index/")
		return Redirect.to_action(request, "index")
	"""

	@staticmethod
	def to(request, route, params=None):
		"""
		route_list[0] = app
		route_list[1] = controller
		route_list[2] = action
		"""
		route = route.strip("/")
		route_list = route.split("/")

		app_name = route_list[0]
		controller_name = ""
		action_name = ""
		if len(route_list) > 1:
			controller_name = route_list[1]
		else:
			raise Exception(("Route no tiene controller"))
		if len(route_list) > 2:
			action_name = route_list[2]

		app = ("apps.%s.views") % app_name

		path = "/%s/%s/" % (app_name, controller_name)
		func = "%s" % (controller_name)
		if action_name:
			path = "/%s/%s/%s/" % (app_name, controller_name, action_name)
			func = "%s_%s" % (controller_name, action_name)

		if request.is_ajax():
			mod = __import__(app, fromlist=[func])
			methodToCall = getattr(mod, func)
			# Message.error(request, "ajax %s"%path)
			request.path = path  # /app/controller_path/action/$params
			return methodToCall(request)
		else:
			# Message.error(request, "noajax %s"%path)
			return redirect(path)

	@staticmethod
	def to_action(request, action_name, params=None):
		"""
		route_list[0] = app
		route_list[1] = controller
		route_list[2] = action
		"""
		route = request.path
		route = route.strip("/")
		route_list = route.split("/")

		app_name = route_list[0]
		controller_name = ""
		# action_name=""
		if len(route_list) > 1:
			controller_name = route_list[1]
		else:
			raise Exception(("Route no tiene controller"))
		# if len(route_list) > 2:
		# 	action_name = route_list[2]

		app = ("apps.%s.views") % app_name

		path = "/%s/%s/" % (app_name, controller_name)
		func = "%s" % (controller_name)
		if action_name:
			path = "/%s/%s/%s/" % (app_name, controller_name, action_name)
			func = "%s_%s" % (controller_name, action_name)
		# Message.error(request, "path= %s"%path)
		# Message.error(request, "func= %s"%func)
		if request.is_ajax():
			mod = __import__(app, fromlist=[func])
			methodToCall = getattr(mod, func)
			# Message.error(request, "ajax %s"%path)
			request.path = path  # /app/controller_path/action/$params
			return methodToCall(request)
		else:
			# Message.error(request, "noajax %s"%path)
			return redirect(path)

