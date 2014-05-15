# _*_ coding: utf-8 _*_
"""
@copyright   Copyright (c) 2014 Submit Consulting
@author      Angel Sullon (@asullom)
@package     rrhh

Descripcion: Registro de las urls de la app rrhh
"""
from django.conf.urls import patterns, url

urlpatterns = patterns('apps.rrhh.views',
	
	url(r'^employee/index/(?P<field>[\w\d\-]+)/(?P<value>.*)/(?P<order>[\w\d\-]+)/$', 'employee_index', name='employee_index'),
	url(r'^employee/index/(?P<field>[\w\d\-]+)/(?P<value>.*)/$', 'employee_index', name='employee_index'),
	url(r'^employee/index/$', 'employee_index', name='employee_index'),
	url(r'^employee/add/$', 'employee_add', name='employee_add'),
	url(r'^employee/choice/(?P<key>.*)/$', 'employee_choice', name='employee_choice'),
	url(r'^employee/edit/$', 'employee_edit', name='employee_edit'),
	url(r'^employee/delete/(?P<key>.*)/$', 'employee_delete', name='employee_delete'),
	url(r'^employee_json_by_filter/$', 'employee_json_by_filter', name="employee_json_by_filter"),
	url(r'^employee/person_search/(?P<field>[\w\d\-]+)/(?P<value>.*)/$', 'employee_person_search', name='employee_person_search'),
	url(r'^employee/person_search/$', 'employee_person_search', name='employee_person_search'),
    url(r'^employee/add_from_person/(?P<key>.*)/$', 'employee_add_from_person', name='employee_add_from_person'),
    
	url(r'^employee/add_all/$', 'employee_add_all', name='employee_add_all'),
	

) 
