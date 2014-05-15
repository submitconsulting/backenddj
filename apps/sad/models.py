# _*_ coding: utf-8 _*_
"""
@copyright   Copyright (c) 2014 Submit Consulting
@author      Angel Sullon (@asullom)
@package     sad

Descripcion: Registro de los modelos de la app sad
"""
from django.db import models
from django.contrib.auth.models import User, Group, Permission
from apps.params.models import Person
from apps.space.models import Solution, Association, Enterprise, Headquar

# Usaremos las tablas de django:
# User
# Group (para nosotros Perfil)
# Permission+ContentType (para nosostros Recursos)

class Profile(models.Model):
    """
    Tabla que amplia la informacion de los usuarios del sistema
    """
    last_headquar_id = models.CharField(max_length=50, null=True, blank=True)
    last_module_id = models.CharField(max_length=50, null=True, blank=True)

    user = models.OneToOneField(User)
    
    person = models.OneToOneField(Person)

    class Meta:
        permissions = (
            # ("profile", "Puede hacer TODAS las operaciones del perfil"),
        )

    def __unicode__(self):
        return self.user.username
    '''
    def create_user_profile(sender, instance, created, **kwargs):
        if created :
            Profile.objects.create(user=instance)
        post_save.connect(create_user_profile, sender=User)
    '''
class UserState(models.Model):
    """
    Tabla que registra el historial de los estados de los usuarios
    """
    ON = "ON"
    OFF = "OFF"
    
    USER_STATES = (
        (ON, "Activate"),
        (OFF, "Deactivate"),

    )
    state = models.CharField(max_length=50, choices=USER_STATES, default=ON)
    description = models.TextField(null=True, blank=True)

    user = models.ForeignKey(User)
    
    registered_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        permissions = (
            # ("profile", "Puede hacer TODAS las operaciones del perfil"),
        )

    def __unicode__(self):
        return "%s %s" % (self.user.username, self.state)
    '''
    def create_user_profile(sender, instance, created, **kwargs):
        if created :
            Profile.objects.create(user=instance)
        post_save.connect(create_user_profile, sender=User)
    '''
class Access(models.Model):
    """
    Tabla que registra los accesos de los usuarios al sistema
    """
    INPUT = "INPUT"
    OUTPUT = "OUTPUT"
    
    ACCESS_TYPES = (
        (INPUT, "Input"),
        (OUTPUT, "Output"),

    )
    access_type = models.CharField(max_length=50, choices=ACCESS_TYPES, default=INPUT)
    ip = models.CharField(max_length=50, null=True, blank=True)
    session_key = models.TextField(null=True, blank=True)
    
    user = models.ForeignKey(User)
    registered_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        permissions = (
            ("access", "Puede hacer TODAS las operaciones del access"),
        )

    def __unicode__(self):
        return "%s %s" % (self.user.username, self.access_type)

class Backup(models.Model):
    """
    Tabla que registra los accesos de los usuarios al sistema
    """
    
    file_name = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    size = models.CharField(max_length=50, null=True, blank=True)
   
    user = models.ForeignKey(User)
    registered_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        permissions = (
            ("backup", "Puede hacer TODAS las operaciones de backup"),
        )

    def __unicode__(self):
        return self.file_name
    
class Module(models.Model):
    """
    Modulos del sistema
    """
    PRO = "PRO"
    WEB = "WEB"
    VENTAS = "VENTAS"
    BACKEND = "BACKEND"
    MODULES = (
        (PRO, "Profesional"),
        (WEB, "Web informativa"),
        (VENTAS, "Ventas"),
        (BACKEND, "Backend Manager"),

    )
    module = models.CharField(max_length=50, choices=MODULES, default=BACKEND)
    name = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    icon = models.CharField(max_length=50, null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    registered_at = models.DateTimeField(auto_now_add=True)
    modified_in = models.DateTimeField(auto_now=True)

    solutions = models.ManyToManyField(Solution, verbose_name="solutions", null=True, blank=True)
    groups = models.ManyToManyField(Group, related_name="module_set", verbose_name="groups", null=True, blank=True)  # verbose_name es para Module
    initial_groups = models.ManyToManyField(Group, related_name="initial_groups_module_set", verbose_name="initial_groups", null=True, blank=True)  # related_name cambia module_set x initial_groups_module_set

    class Meta:
        permissions = (
            ("module", "Puede hacer TODAS las operaciones de modulos"),
        )

    def __unicode__(self):
        return "%s %s" % (self.module, self.name)

class Menu(models.Model):
    """
    Menús del sistema. 
    """
    MODULES = Module.MODULES

    module = models.CharField(max_length=50, choices=MODULES, default=Module.BACKEND)
    title = models.CharField(max_length=50)
    url = models.CharField(max_length=150, default="#")
    pos = models.IntegerField(max_length=50, default=1)
    icon = models.CharField(max_length=50, null=True, blank=True, default="")
    is_active = models.BooleanField(default=True)
    description = models.TextField(null=True, blank=True)

    registered_at = models.DateTimeField(auto_now_add=True)
    modified_in = models.DateTimeField(auto_now=True)

    permission = models.ForeignKey(Permission, null=True, blank=True)
    parent = models.ForeignKey("Menu", verbose_name="parent", null=True, blank=True)  # related_name="parent",

    class Meta:
        permissions = (
            ("menu", "Puede hacer TODAS las operaciones de menús"),
        )

    def __unicode__(self):
        return "%s %s" % (self.module, self.title)

class UserProfileEnterprise(models.Model):
    """
    Permisos a nivel de empresa
    """
    # is_admin  = models.BooleanField(default=False)
    registered_at = models.DateTimeField(auto_now_add=True)
    modified_in = models.DateTimeField(auto_now=True)

    user = models.ForeignKey(User)
    group = models.ForeignKey(Group)
    enterprise = models.ForeignKey(Enterprise)

    class Meta:
        permissions = (
            # ("userprofileenterprise", "Puede hacer TODAS las operaciones de userprofileenterprise"),
        )

    def __unicode__(self):
        return "%s %s - %s" % (self.user.username, self.group.name, self.enterprise.name)

class UserProfileHeadquar(models.Model):
    """
    Permisos a nivel de sede
    """
    # is_admin  = models.BooleanField(default=False)
    registered_at = models.DateTimeField(auto_now_add=True)
    modified_in = models.DateTimeField(auto_now=True)

    user = models.ForeignKey(User)
    group = models.ForeignKey(Group)
    headquar = models.ForeignKey(Headquar)

    class Meta:
        permissions = (
            # ("userprofileheadquar", "Puede hacer TODAS las operaciones de userprofileheadquar"),
        )

    def __unicode__(self):
        return "%s %s - %s" % (self.user.username, self.group.name, self.headquar.name)

class UserProfileAssociation(models.Model):
    """
    Permisos a nivel de association
    """
    # is_admin  = models.BooleanField(default=False)
    registered_at = models.DateTimeField(auto_now_add=True)
    modified_in = models.DateTimeField(auto_now=True)

    user = models.ForeignKey(User)
    group = models.ForeignKey(Group)
    association = models.ForeignKey(Association)

    class Meta:
        permissions = (
            # ("userprofileassociation", "Puede hacer TODAS las operaciones de userprofileassociation"),
        )

    def __unicode__(self):
        return "%s %s - %s" % (self.user.username, self.group.name, self.association.name)
