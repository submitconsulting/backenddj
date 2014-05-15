# _*_ coding: utf-8 _*_
"""
@copyright   Copyright (c) 2014 Submit Consulting
@author      Angel Sullon (@asullom)
@package     mod_ventas

Descripcion: Implementacion de los controladores de la app mod_ventas
"""
from django.shortcuts import render_to_response
from django.template.context import RequestContext

def mod_ventas_dashboard(request):
    
    c = {
        "page_module":("mod_ventas_dashboard"),
        "page_title":("Ventas module dashboard page."),
        }
    return render_to_response("mod_ventas/dashboard.html", c, context_instance=RequestContext(request))
