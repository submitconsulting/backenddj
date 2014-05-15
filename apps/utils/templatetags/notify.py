# -*- coding: utf-8 -*-
"""
@copyright   Copyright (c) 2014 Submit Consulting
@author      Angel Sullon (@asullom)
@package     utils

Descripcion: Tag o interfáz para mostrar a los usuarios los mensajes generados por el sistema
"""
from django import template
#from apps.utils.messages import Message
from django.contrib import messages

register = template.Library()

@register.simple_tag
def get_notify(request):
	"""
	Muestra los mensajes de error, advertencias o de información en los templates.
	Estos mensajes son recepcionados con la clase Message.
	p.e: 
		Message.info(request,"message")
	
	Usage::
		
		{% get_notify request %}

	Examples::

		{% get_notify request %}
		
	"""
	d = None
	try:
		d=messages.get_messages(request)
	except KeyError:
		pass
	o = ''
	if d :
		for i in d:
			o = o + i.message
	a = (u'<div id="dw-message" class="dw-message">'
		)

	c = (u'		</div>'
		)

	path = request.path  # get_full_path()
	script = (u'<script type="text/javascript">'
        	u'DwUpdateUrl("%s");'
    		u'</script>'
			u'' % (path))
	if request.is_ajax():
		return "%s%s%s %s" % (a, o, c, script)
	else:
		return "%s%s%s" % (a, o, c)
