# _*_ coding: utf-8 _*_
"""
@copyright   Copyright (c) 2014 Submit Consulting
@author      Angel Sullon (@asullom)
@package     maestros

Descripcion: Registro de las urls de la app maestros
"""
from django.conf.urls import patterns, url

urlpatterns = patterns('apps.maestros.views',
	url(r'^producto/index/(?P<field>[\w\d\-]+)/(?P<value>.*)/(?P<order>[\w\d\-]+)/$', 'producto_index', name='producto_index'),
	url(r'^producto/index/(?P<field>[\w\d\-]+)/(?P<value>.*)/$', 'producto_index', name='producto_index'),
	url(r'^producto/index/$', 'producto_index', name='producto_index'),
	url(r'^producto/add/$', 'producto_add', name='producto_add'),
	url(r'^producto/edit/(?P<key>.*)/$', 'producto_edit', name='producto_edit'),
	url(r'^producto/delete/(?P<key>.*)/$', 'producto_delete', name='producto_delete'),
	
) 
