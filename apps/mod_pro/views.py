# _*_ coding: utf-8 _*_
"""
@copyright   Copyright (c) 2014 Submit Consulting
@author      Angel Sullon (@asullom)
@package     mod_pro

Descripcion: Implementacion de los controladores de la app mod_pro
"""
from django.shortcuts import render_to_response
from django.template.context import RequestContext

def mod_pro_dashboard(request):
    
    c = {
        "page_module":("mod_pro_dashboard"),
        "page_title":("PRO module dashboard page."),
        }
    return render_to_response("mod_pro/dashboard.html", c, context_instance=RequestContext(request))
