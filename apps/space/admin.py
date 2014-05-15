# _*_ coding: utf-8 _*_
"""
@copyright   Copyright (c) 2014 Submit Consulting
@author      Angel Sullon (@asullom)
@package     space

Descripcion: Registro de modelos para la administracion con django de la app space
"""
from django.contrib import admin
from apps.space.models import Solution, Enterprise, Association, Headquar


admin.site.register(Solution)
admin.site.register(Enterprise)
admin.site.register(Association)
admin.site.register(Headquar)
