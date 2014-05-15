# _*_ coding: utf-8 _*_
"""
@copyright   Copyright (c) 2014 Submit Consulting
@author      Angel Sullon (@asullom)
@package     mod_pro

Descripcion: Registro de las urls de la app mod_pro
"""
from django.conf.urls import patterns, url

urlpatterns = patterns('apps.mod_pro.views',
	url(r'^dashboard/$', 'mod_pro_dashboard', name='mod_pro_dashboard'),
) 
