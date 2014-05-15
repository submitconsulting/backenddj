# _*_ coding: utf-8 _*_
"""
@copyright   Copyright (c) 2014 Submit Consulting
@author      Angel Sullon (@asullom)
@package     mod_backend

Descripcion: Implementacion de los controladores de la app mod_backend
"""
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.contrib.sessions.backends.db import SessionStore

def mod_backend_dashboard(request):
    #s = SessionStore()
    #s["last_login"] = "holaaa"
    #s.save()
    c = {
        "page_module":("mod_backend_dashboard"),
        "page_title":("Backend module dashboard page."),
        }
    return render_to_response("mod_backend/dashboard.html", c, context_instance=RequestContext(request))
