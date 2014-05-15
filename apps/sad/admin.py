# _*_ coding: utf-8 _*_
"""
@copyright   Copyright (c) 2014 Submit Consulting
@author      Angel Sullon (@asullom)
@package     sad

Descripcion: Registro de modelos para la administracion con django de la app sad
"""
from django.contrib import admin
from apps.sad.models import Module, Menu, UserProfileEnterprise, UserProfileHeadquar,\
    UserProfileAssociation
from apps.sad.models import Profile

admin.site.register(Module)
admin.site.register(Menu)
admin.site.register(UserProfileEnterprise)
admin.site.register(UserProfileHeadquar)
admin.site.register(UserProfileAssociation)

# Define an inline admin descriptor for UserProfile model
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
# which acts a bit like a singleton
class UserProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'profile'

# Define a new User admin
class UserAdmin(UserAdmin):
    inlines = (UserProfileInline,)

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

