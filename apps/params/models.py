# _*_ coding: utf-8 _*_
"""
@copyright   Copyright (c) 2014 Submit Consulting
@author      Angel Sullon (@asullom)
@package     params

Descripcion: Registro de los modelos de la app params
"""
from django.db import models
from django.contrib.auth.models import User

class LocalityType(models.Model):
    """
    Tabla params_localitytype para tipos de localidades. 
    P.e: Departamento, Provincia, Distrito, etc.
    """
    name = models.CharField(max_length=50)

    class Meta:
        permissions = (
            ("localitytype", "Puede hacer TODAS las oper. de tipos d localidades"),
        )

    def __unicode__(self):
        return self.name

class Locality(models.Model):
    """
    Tabla params_locality que contiene localidades o ciudades
    """
    name = models.CharField(max_length=50)
    location = models.TextField(null=True, blank=True)
    utm = models.CharField(max_length=50, null=True, blank=True)
    msnm = models.FloatField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    date_create = models.DateTimeField(null=True, blank=True)
    registered_at = models.DateTimeField(auto_now_add=True)
    modified_in = models.DateTimeField(auto_now=True)
    locality_type = models.ForeignKey(LocalityType, null=True, blank=True)

    class Meta:
        permissions = (
            ("locality", "Puede hacer TODAS las operaciones de localidades"),
            ("locality_index", "Puede ver el index de localidades"),
            ("locality_add", "Puede agregar localidad"),
            ("locality_edit", "Puede actualizar localidades"),
            ("locality_delete", "Puede eliminar localidades"),
            ("locality_report", "Puede reportar localidades"),
            ("locality_state", "Puede inactivar y reactivar localidades"),
        )

    def __unicode__(self):
        return "%s %s" % (self.name, self.location)
    
    @staticmethod
    def calculatex(a):
        return a

class Person(models.Model):
    """
    Tabla params_Person contiene la información básica de los empleados, clientes, etc.
    esto es con la finalidad de no repetir información en cada tabla
    """
    DEFAULT = "DNI"
    CE = "CE"
    PART_NAC = "PART_NAC"
    OTHERS = "OTHERS"
    IDENTITY_TYPES = (
        (DEFAULT, "D.N.I."),
        (CE, "C.E."),
        (PART_NAC, "P.NAC."),
        (OTHERS, "Otro")
    )
    identity_type = models.CharField(max_length=10, choices=IDENTITY_TYPES, default=DEFAULT)
    identity_num = models.CharField(max_length=20, null=True, blank=True)
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    photo = models.ImageField(upload_to="personas", verbose_name="Foto", default="personas/default.png") # req. PIL
    
    registered_at = models.DateTimeField(auto_now_add=True)
    modified_in = models.DateTimeField(auto_now=True)

    class Meta:
        permissions = (
            ("person", "Puede hacer TODAS las operaciones de personas"),
        )

    def __unicode__(self):
        return self.first_name

class Ticket(models.Model):
    """
    Tabla que registra los accesos de los usuarios al sistema
    """
    texto = models.CharField(max_length=150, null=True, blank=True)
    fila = models.IntegerField(default=1)
   
    user = models.ForeignKey(User)
    
    class Meta:
        permissions = (
            ("ticket", "Puede hacer TODAS las operaciones de ticket"),
        )

    def __unicode__(self):
        return "%s %s" % (self.user.username, self.texto)
    
# mis params tables para el proyecto SHOMWARE
class Categoria(models.Model):
    """
    Tabla params_Categoria para las categorías de los productos del proyecto SHOMWARE
    """
    nombre = models.CharField(max_length=50)

    class Meta:
        permissions = (
            ("categoria", "Puede hacer TODAS las operaciones de categorias"),
        )

    def __unicode__(self):
        return self.nombre
"""
G:\dev\apps\backenddj>python manage.py syncdb
Creating tables ...
Creating table params_categoria
Creating table maestros_producto
The following content types are stale and need to be deleted:

    sad | resource
    sad | user
    sad | group

Any objects related to these content types by a foreign key will also
be deleted. Are you sure you want to delete these content types?
If you"re unsure, answer "no".

    Type "yes" to continue, or "no" to cancel: no
Installing custom SQL ...
Installing indexes ...
Installed 0 object(s) from 0 fixture(s)

G:\dev\apps\backenddj>

y se agregarán las nuevas tablas con sus permissions previamente definidos
luego ejecute 
delete from auth_permission where codename like 'add_%'or  codename like 'change_%' or codename like 'delete_%'
"""

