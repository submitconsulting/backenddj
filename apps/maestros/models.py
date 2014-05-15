# _*_ coding: utf-8 _*_
"""
@copyright   Copyright (c) 2014 Submit Consulting
@author      Angel Sullon (@asullom)
@package     maestros

Descripcion: Registro de los modelos de la app maestros
"""
from django.db import models
from apps.params.models import Categoria
from apps.space.models import Headquar

class Producto(models.Model):
    """
    Tabla que contiene los productos que ofrece la empresa
    """
    codigo = models.CharField(max_length=50)
    descripcion = models.TextField(null=True, blank=True)
    precio_venta = models.FloatField (default=0)
    esta_activo = models.BooleanField(default=True)
    fecha_venc= models.DateTimeField(null=True, blank=True)
    
    registered_at = models.DateTimeField(auto_now_add=True)
    modified_in = models.DateTimeField(auto_now=True)

    categoria = models.ForeignKey(Categoria, null=True, blank=True)
    headquar = models.ForeignKey(Headquar)

    class Meta:
        permissions = (
            ("producto", "Puede hacer TODAS las operaciones de productos"),
            ("producto_index", "Puede ver el index de productos"),
            ("producto_add", "Puede agregar producto"),
            ("producto_edit", "Puede actualizar productos"),
            ("producto_delete", "Puede eliminar productos"),
            ("producto_report", "Puede reportar productos"),
            ("producto_state", "Puede inactivar y reactivar productos"),
            # Pa agregar más permissions solo vuelva a hacer >python manage.py syncdb y no tiene que borrar la db
            # ("producto_list", "xPuede listar productos"),
            # ("producto_json", "xPuede listar productos en formato JSON"),
            ("producto_edit_precio", "Puede actualizar precio venta de productos"),
        )

    def __unicode__(self):
        return self.descripcion
