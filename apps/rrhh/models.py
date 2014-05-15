# _*_ coding: utf-8 _*_
"""
@copyright   Copyright (c) 2014 Submit Consulting
@author      Angel Sullon (@asullom)
@package     rrhh

Descripcion: Registro de los modelos de la app rrhh
"""
from django.db import models
from apps.params.models import Person
from apps.space.models import Headquar


class Employee(models.Model):
    """
    Tabla que contiene los empleados de la empresa, específicamente de la sede
    """
    codigo = models.CharField(max_length=50)
    contrato_vigente = models.BooleanField(default=True)
    
    registered_at = models.DateTimeField(auto_now_add=True)
    modified_in = models.DateTimeField(auto_now=True)
    
    headquar = models.ForeignKey(Headquar)
    person = models.OneToOneField(Person)

    class Meta:
        permissions = (
            ("employee", "Puede hacer TODAS las operaciones de empleados"),
        )

    def __unicode__(self):
        return "%s %s" % (self.codigo, self.contrato_vigente)

