# _*_ coding: utf-8 _*_
"""
@copyright   Copyright (c) 2014 Submit Consulting
@author      Angel Sullon (@asullom)
@package     space

Descripcion: Registro de las urls de la app space
"""
from django.conf.urls import patterns, url

urlpatterns = patterns('apps.space.views',
	# headquar controllers
	url(r'^headquar/index/$', 'headquar_index', name='headquar_index'),
	url(r'^headquar/add/$', 'headquar_add', name='headquar_add'),
	url(r'^headquar/edit/(?P<key>.*)/$', 'headquar_edit', name='headquar_edit'),
	url(r'^headquar/delete/(?P<key>.*)/$', 'headquar_delete', name='headquar_delete'),
	url(r'^headquar/state/(?P<state>[\w\d\-]+)/(?P<key>.*)/$', 'headquar_state', name='headquar_state'),
	url(r'^headquar/change_association/(?P<key>.*)/$', 'headquar_change_association', name='headquar_change_association'),

	# enterprise controllers
	url(r'^enterprise/index/$', 'enterprise_index', name='enterprise_index'),
	url(r'^enterprise/add/$', 'enterprise_add', name='enterprise_add'),
	url(r'^enterprise/edit/(?P<key>.*)/$', 'enterprise_edit', name='enterprise_edit'),
	url(r'^enterprise/delete/(?P<key>.*)/$', 'enterprise_delete', name='enterprise_delete'),
	url(r'^enterprise/state/(?P<state>[\w\d\-]+)/(?P<key>.*)/$', 'enterprise_state', name='enterprise_state'),
	url(r'^enterprise/edit_current/$', 'enterprise_edit_current', name='enterprise_edit_current'),
	url(r'^enterprise/upload/$', 'enterprise_upload', name='enterprise_upload'),
	
	# association controllers
	url(r'^association/edit_current/$', 'association_edit_current', name='association_edit_current'),
	url(r'^association/upload/$', 'association_upload', name='association_upload'),
	
	# solution controllers
	url(r'^solution/index/$', 'solution_index', name='solution_index'),
	url(r'^solution/add/$', 'solution_add', name='solution_add'),
	url(r'^solution/edit/(?P<key>.*)/$', 'solution_edit', name='solution_edit'),
	url(r'^solution/delete/(?P<key>.*)/$', 'solution_delete', name='solution_delete'),
	url(r'^solution/state/(?P<state>[\w\d\-]+)/(?P<key>.*)/$', 'solution_state', name='solution_state'),

) 
