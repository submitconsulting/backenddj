# _*_ coding: utf-8 _*_
"""
@copyright   Copyright (c) 2014 Submit Consulting
@author      Angel Sullon (@asullom)
@package     home

Descripcion: Registro de las urls de la app home
"""
from django.conf.urls import patterns, url

urlpatterns = patterns('apps.home.views',
	url(r'^$', 'index', name='index'),
	url(r'^index/$', 'index', name='index'),
	


) 
