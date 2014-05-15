# _*_ coding: utf-8 _*_
"""
@copyright   Copyright (c) 2014 Submit Consulting
@author      Angel Sullon (@asullom)
@package     mod_backend

Descripcion: Registro de las urls de la app mod_backend
"""
from django.conf.urls import patterns, url

urlpatterns = patterns('apps.mod_backend.views',
	url(r'^dashboard/$', 'mod_backend_dashboard', name='mod_backend_dashboard'),
) 
