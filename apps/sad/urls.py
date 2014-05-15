# _*_ coding: utf-8 _*_
"""
@copyright   Copyright (c) 2014 Submit Consulting
@author      Angel Sullon (@asullom)
@package     sad

Descripcion: Registro de las urls de la app sad
"""
from django.conf.urls import patterns, url

urlpatterns = patterns('apps.sad.views',
	# micontroller/mi_action maintenance
	
	url(r'^system/index/$', 'system_index', name='system_index'),
	
	url(r'^maintenance/index/$', 'maintenance_index', name='maintenance_index'),
	
	url(r'^backup/index/$', 'backup_index', name='backup_index'),
	
	url(r'^log/index/$', 'log_index', name='log_index'),
	url(r'^log/list/(?P<day>.*)/$', 'log_index', name='log_index'),
	
	url(r'^audit/index/$', 'audit_index', name='audit_index'),
	url(r'^audit/list/(?P<day>.*)/$', 'audit_list', name='audit_list'),
	
	url(r'^access/index/(?P<field>[\w\d\-]+)/(?P<value>.*)/(?P<order>[\w\d\-]+)/$', 'access_index', name='access_index'),
	url(r'^access/index/(?P<field>[\w\d\-]+)/(?P<value>.*)/$', 'access_index', name='access_index'),
	url(r'^access/index/$', 'access_index', name='access_index'),
	
	
	url(r'^user/index/(?P<field>[\w\d\-]+)/(?P<value>.*)/(?P<order>[\w\d\-]+)/$', 'user_index', name='user_index'),
	url(r'^user/index/(?P<field>[\w\d\-]+)/(?P<value>.*)/$', 'user_index', name='user_index'),
	url(r'^user/index/$', 'user_index', name='user_index'),
	url(r'^user/add/$', 'user_add', name='user_add'),
	url(r'^user/edit/(?P<key>.*)/$', 'user_edit', name='user_edit'),
	url(r'^user/upload/$', 'user_upload', name='user_upload'),
	url(r'^user/delete/(?P<key>.*)/$', 'user_delete', name='user_delete'),
	url(r'^user/view/(?P<key>.*)/$', 'user_view', name='user_view'),
	url(r'^user/state/(?P<state>[\w\d\-]+)/(?P<key>.*)/$', 'user_state', name='user_state'),
	url(r'^user/person_search/(?P<field>[\w\d\-]+)/(?P<value>.*)/$', 'user_person_search', name='user_person_search'),
    url(r'^user/person_search/$', 'user_person_search', name='user_person_search'),
    url(r'^user/add_from_person/(?P<key>.*)/$', 'user_add_from_person', name='user_add_from_person'),

	url(r'^menu/index/(?P<field>[\w\d\-]+)/(?P<value>.*)/(?P<order>[\w\d\-]+)/$', 'menu_index', name='menu_index'),
	url(r'^menu/index/(?P<field>[\w\d\-]+)/(?P<value>.*)/$', 'menu_index', name='menu_index'),
	url(r'^menu/index/$', 'menu_index', name='menu_index'),
	url(r'^menu/add/$', 'menu_add', name='menu_add'),
	url(r'^menu/edit/(?P<key>.*)/$', 'menu_edit', name='menu_edit'),
	url(r'^menu/delete/(?P<key>.*)/$', 'menu_delete', name='menu_delete'),
	url(r'^menu/state/(?P<state>[\w\d\-]+)/(?P<key>.*)/$', 'menu_state', name='menu_state'),



	url(r'^module/index/$', 'module_index', name='module_index'),
	url(r'^module/add/$', 'module_add', name='module_add'),
	url(r'^module/edit/(?P<key>.*)/$', 'module_edit', name='module_edit'),
	url(r'^module/delete/(?P<key>.*)/$', 'module_delete', name='module_delete'),
	url(r'^module/plans_edit/$', 'module_plans_edit', name='module_plans_edit'),
	url(r'^module/state/(?P<state>[\w\d\-]+)/(?P<key>.*)/$', 'module_state', name='module_state'),

	url(r'^group/index/$', 'group_index', name='group_index'),
	url(r'^group/add/$', 'group_add', name='group_add'),
	url(r'^group/edit/(?P<key>.*)/$', 'group_edit', name='group_edit'),
	url(r'^group/delete/(?P<key>.*)/$', 'group_delete', name='group_delete'),
	url(r'^group/permissions_edit/$', 'group_permissions_edit', name='group_permissions_edit'),  # agregar este recurso manualmente


	url(r'^resource/index/$', 'resource_index', name='resource_index'),
	url(r'^resource/add/$', 'resource_add', name='resource_add'),
	url(r'^resource/edit/(?P<key>.*)/$', 'resource_edit', name='resource_edit'),
	url(r'^resource/delete/(?P<key>.*)/$', 'resource_delete', name='resource_delete'),

) 
