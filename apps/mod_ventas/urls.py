# _*_ coding: utf-8 _*_
"""
@copyright   Copyright (c) 2014 Submit Consulting
@author      Angel Sullon (@asullom)
@package     mod_ventas

Descripcion: Registro de las urls de la app mod_ventas
"""
from django.conf.urls import patterns, url

urlpatterns = patterns('apps.mod_ventas.views',
	url(r'^dashboard/$', 'mod_ventas_dashboard', name='mod_ventas_dashboard'),

) 
