# -*- coding: utf-8 -*-
"""
@copyright   Copyright (c) 2014 Submit Consulting
@author      Angel Sullon (@asullom)
@package     utils

Descripcion: Decorador para validar los permisos de los usuarios

"""
from functools import wraps
from django.utils.decorators import available_attrs
from django.http import HttpResponse
from django.shortcuts import render_to_response
from apps.utils.messages import Message
from django.template.context import RequestContext
from django.core.exceptions import PermissionDenied

def is_admin(view_func):
    '''
    Verifica si es admin o no
    Usage::

        from apps.sad.decorators import is_admin

        @is_admin 
        def function_name(request):

    Example::

        @is_admin
        def locality_index(request, field="name", value="None", order="-id"):
            return render_to_response("params/locality/index.html", c, context_instance = RequestContext(request))
    '''
    def _wrapped_view_func(request, *args, **kwargs):
        if not request.user.is_superuser:
            return HttpResponse("<h3>Necesitas privilegios de aministrador para realizar esta acción</h3>")
        return view_func(request, *args, **kwargs) 
        
    return _wrapped_view_func

def permission_resource_required(function=None, template_denied_name="denied_mod_backend.html"):
    """
    Verifica si el usuario tiene permiso para acceder al recurso actual (request.path)

    Usage::

        from apps.sad.decorators import permission_resource_required

        @permission_resource_required
        def function_name(request):

        @permission_resource_required(template_denied_name="denied_mod_ventas.html")
        def function_name(request):

    Example::

        @permission_resource_required
        def user_index(request, field="username", value="None", order="-id"):
            ...
            render_to_response("sad/user/index.html", c, context_instance = RequestContext(request))
    """
    actual_decorator = permission_resource_required_decorator(
        template_denied_name=template_denied_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

def permission_resource_required_decorator(template_denied_name="denied_mod_backend.html"):
    """
    Implementa el docorador permission_resource_required
    """
    def decorator(view_func):
        @wraps(view_func, assigned=available_attrs(view_func))
        def _wrapped_view(request, *args, **kwargs) :
            if not request.user.id:
                Message.warning(request, ("Tu no estás autenticado"))
                raise PermissionDenied #403.html
                #return render_to_response("403.html", {'': ''}, context_instance=RequestContext(request))
            permiso = ""
            recurso = "/"
            response = HttpResponse()
            response.write('<script type="text/javascript">')
            response.write('alert("Hola")')
            response.write('</script>')
            try:
                path = request.path.strip("/")  # request.get_full_path().strip("/") #"/apps/controller/action/" to "apps/controller/action"
                
            except Exception, e:
                raise Exception("%s. Asigne adecuadamente el parámetro template_denied_name " % e)
            
            path_list = path.split('/')
            permiso = "%s." % (path_list[0])
            recurso = "/%s/" % (path_list[0])
            if not isinstance(permiso, (list, tuple)):
                perms = (permiso,)
            else:
                perms = permiso

            if not request.user.has_perms(perms) and len(path_list) > 1:
                permiso = "%s.%s" % (path_list[0], path_list[1])
                recurso = "/%s/%s/" % (path_list[0], path_list[1])
                
            if not isinstance(permiso, (list, tuple)):
                perms = (permiso,)
            else:
                perms = permiso
            if not request.user.has_perms(perms) and len(path_list) > 2:
                permiso = "%s.%s_%s" % (path_list[0], path_list[1], path_list[2])
                recurso = "/%s/%s/%s/" % (path_list[0], path_list[1], path_list[2])
 
            if not isinstance(permiso, (list, tuple)):
	            perms = (permiso,)
            else:
	            perms = permiso
            if request.user.has_perms(perms):
	            return view_func(request, *args, **kwargs)
            else:
                Message.warning(request, ("Tu no posees permisos para acceder a <b>%(route)s</b>") % {'route':recurso})
                #raise PermissionDenied
                return render_to_response(template_denied_name, {'': ''}, context_instance=RequestContext(request))
        return _wrapped_view
    return decorator
