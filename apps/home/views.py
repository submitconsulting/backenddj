# _*_ coding: utf-8 _*_
"""
@copyright   Copyright (c) 2014 Submit Consulting
@author      Angel Sullon (@asullom)
@package     home

Descripcion: Implementacion de los controladores de la app home o inicio del sistema
"""
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
def index(request):
    """
    Muestra la página inical del sistema, ie http://localhost:8000/ = http://localhost:8000/home/
    """
    
    c = {
        "page_module":("Home"),
        "page_title":("BackendDJ Home Page."),
        }
    return render_to_response("home/index.html", c, context_instance=RequestContext(request))


# endregion home OK