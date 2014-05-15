# _*_ coding: utf-8 _*_
"""
@copyright   Copyright (c) 2014 Submit Consulting
@author      Angel Sullon (@asullom)
@package     space

Descripcion: Registro de los modelos de la app space
"""
from django.db import models
from apps.params.models import Locality
from django.utils.translation import ugettext as _

class Solution(models.Model):
    """
    Tabla que contiene las soluciones o planes o servicios del sistema
    """
    name = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    registered_at = models.DateTimeField(auto_now_add=True)
    modified_in = models.DateTimeField(auto_now=True)
    
    class Meta:
        permissions = (
            ("solution", "Puede hacer TODAS las operaciones de soluciones"),
        )

    def __unicode__(self):
        return self.name

class Association(models.Model):
    """
    Tabla que contiene las asociaciones suscritas a un plan
    """
    GOVERMENT = "GOVERMENT"
    PRIVATE = "PRIVATE"
    MIXED = "MIXED"
    OTHERS = "OTHERS"
    TYPES = (
        (GOVERMENT, _("Government")),
        (PRIVATE, _("Private")),
        (MIXED, _("Mixed")),
        (OTHERS, _("Others"))
    )
    name = models.CharField(max_length=50)
    logo = models.ImageField(upload_to="asociaciones", verbose_name="Logo", default="asociaciones/default.png")
    type_a = models.CharField(max_length=10, choices=TYPES, default=PRIVATE)
    is_active = models.BooleanField(default=True)

    registered_at = models.DateTimeField(auto_now_add=True)
    modified_in = models.DateTimeField(auto_now=True)

    solution = models.ForeignKey(Solution, null=True, blank=True)

    class Meta:
        permissions = (
            ("association", "Puede hacer TODAS las operaciones de asociaciones"),
        )

    def __unicode__(self):
        return self.name

class Enterprise(models.Model):
    """
    Tabla que contiene las empresas suscritas a un plan
    """
    GOVERMENT = "GOVERMENT"
    PRIVATE = "PRIVATE"
    MIXED = "MIXED"
    OTHERS = "OTHERS"
    TYPES = (
        (GOVERMENT, _("Government")),
        (PRIVATE, _("Private")),
        (MIXED, _("Mixed")),
        (OTHERS, _("Others"))
    )
    name = models.CharField(max_length=50)
    logo = models.ImageField(upload_to="empresas", verbose_name="Logo", default="empresas/default.png")
    tax_id = models.CharField(max_length=50)
    type_e = models.CharField(max_length=10, choices=TYPES, default=PRIVATE)
    is_active = models.BooleanField(default=True)

    registered_at = models.DateTimeField(auto_now_add=True)
    modified_in = models.DateTimeField(auto_now=True)

    solution = models.ForeignKey(Solution, null=True, blank=True)

    class Meta:
        permissions = (
            ("enterprise", "Puede hacer TODAS las operaciones de empresas"),
        )

    def __unicode__(self):
        return self.name

class Headquar(models.Model):
    """
    Tabla que contiene las sedes de las empresas, asociadas a una Asociación
    Un Headquar o sede o sucursal, es la unidad principal del sistema
    Los accesos del sistema serán entregados a un Headquarters
    """
    name = models.CharField(max_length=50)

    phone = models.CharField(max_length=50, null=True, blank=True)

    address = models.TextField(null=True, blank=True)
    is_main = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)

    registered_at = models.DateTimeField(auto_now_add=True)
    modified_in = models.DateTimeField(auto_now=True)

    locality = models.ForeignKey(Locality, null=True, blank=True)
    association = models.ForeignKey(Association, null=True, blank=True)
    enterprise = models.ForeignKey(Enterprise)

    class Meta:
        permissions = (
            ("headquar", "Puede hacer TODAS las operaciones de sedes"),
        )

    def __unicode__(self):
        return "%s %s-%s (%s-%s)" % (self.name, self.enterprise.name, self.enterprise.solution.name, self.association.name, self.association.solution.name)
