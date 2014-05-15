# _*_ coding: utf-8 _*_
"""
@copyright   Copyright (c) 2014 Submit Consulting
@author      Angel Sullon (@asullom)
@package     account

Descripcion: Registro de las urls de la app account
"""
from django.conf.urls import patterns, url

urlpatterns = patterns('apps.accounts.views',
	url(r'^add_enterprise/$', 'add_enterprise', name='add_enterprise'),
	url(r'^signup/$', 'signup_sys', name='signup_sys'),
	url(r'^login/$', 'login_sys', name='login_sys'),
	url(r'^load_access/(?P<headquar_id>.*)/(?P<module_id>.*)/$', 'load_access', name='load_access'),
	url(r'^logout/$', 'logout_sys', name='logout_sys'),
	url(r'^profile/edit/$', 'user_profile_edit', name='user_profile_edit'), # se creará como recurso virtual
	
	url(r'^choice_headquar/(?P<field>[\w\d\-]+)/(?P<value>.*)/$', 'choice_headquar', name='choice_headquar'),
	url(r'^choice_headquar/$', 'choice_headquar', name='choice_headquar'),
) 
