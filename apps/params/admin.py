# _*_ coding: utf-8 _*_
"""
@copyright   Copyright (c) 2014 Submit Consulting
@author      Angel Sullon (@asullom)
@package     params

Descripcion: Registro de modelos para la administracion con django de la app params
"""
from django.contrib import admin
from apps.params.models import LocalityType, Locality, Person

# Register your models here.

admin.site.register(LocalityType)
admin.site.register(Locality)
admin.site.register(Person)
