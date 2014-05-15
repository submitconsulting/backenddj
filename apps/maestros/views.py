# _*_ coding: utf-8 _*_
"""
@copyright   Copyright (c) 2014 Submit Consulting
@author      Angel Sullon (@asullom)
@package     maestros

Descripcion: Implementacion de los controladores de la app maestros
"""
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
import json
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from apps.utils.decorators import permission_resource_required
from unicodedata import normalize
from apps.utils.security import Redirect, SecurityKey, DataAccessToken
from django.db.models import Q
from apps.utils.messages import Message
from apps.space.models import Headquar
from django.db import transaction
from apps.params.models import Person
from apps.maestros.models import Producto
from apps.params.models import Categoria

@login_required
@permission_resource_required
def producto_index(request, field="descripcion", value="None", order="-id"):
    """
    Página principal para trabajar con productos
    """
    try:
        headquar = get_object_or_404(Headquar, id=DataAccessToken.get_headquar_id(request.session))
    except:
        Message.error(request, ("Sede no seleccionado o no se encuentra en la base de datos."))
        return Redirect.to(request, "/home/choice_headquar/")

    field = (field if not request.REQUEST.get("field") else request.REQUEST.get("field")).strip()
    value = (value if not request.REQUEST.get("value") else request.REQUEST.get("value")).strip()
    order = (order if not request.REQUEST.get("order") else request.REQUEST.get("order")).strip()

    producto_page = None
    try:
        value_f = "" if value == "None" else value
        column_contains = u"%s__%s" % (field, "contains")
        producto_list = Producto.objects.filter(headquar=headquar).filter(**{ column_contains: value_f }).order_by(order)
        paginator = Paginator(producto_list, 20)
        try:
            producto_page = paginator.page(request.GET.get("page"))
        except PageNotAnInteger:
            producto_page = paginator.page(1)
        except EmptyPage:
            producto_page = paginator.page(paginator.num_pages)
    except Exception, e:
        Message.error(request, e)
    c = {
        "page_module":("Gestión de productos"),
        "page_title":("Listado de productos."),
        
        "producto_page":producto_page,
        "field":field,
        "value":value.replace("/", "-"),
        "order":order,
        }
    return render_to_response("maestros/producto/index.html", c, context_instance=RequestContext(request))

@permission_resource_required
@transaction.atomic
def producto_add(request):
    """
    Agrega Producto
    """
    d = Producto()
    d.descripcion = ""
    d.fecha_venc=""
    if request.method == "POST":
        try:
            sid = transaction.savepoint()
            d.codigo = request.POST.get("codigox")
            d.descripcion = request.POST.get("descripcion")
            d.precio_venta = request.POST.get("precio_venta")
            d.headquar_id = DataAccessToken.get_headquar_id(request.session)
            
            if request.POST.get("fecha_venc"):
                d.fecha_venc = request.POST.get("fecha_venc")
                
            if request.POST.get("categoria_nombre"):
                d.categoria, is_created = Categoria.objects.get_or_create(
                    nombre=request.POST.get("categoria_nombre"),
                    )

            if Producto.objects.filter(codigo=d.codigo).exclude(id=d.id, headquar_id=d.headquar_id).count() > 0:
                raise Exception("El producto <b>%s</b> ya existe " % d.codigo)
            d.save()
            if d.id:
                Message.info(request, ("Producto <b>%(name)s</b> ha sido registrado correctamente.") % {"name":d.codigo}, True)
                return Redirect.to_action(request, "index")
        except Exception, e:
            transaction.savepoint_rollback(sid)
            Message.error(request, e)
    categoria_nombre_list = []
    try:
        categoria_nombre_list = json.dumps(list(col["nombre"] + ""  for col in Categoria.objects.values("nombre").filter().order_by("nombre")))
    except Exception, e:
        Message.error(request, e)
    c = {
        "page_module":("Gestión de productos"),
        "page_title":("Agregar productos."),
        "d":d,
        "categoria_nombre_list":categoria_nombre_list,
        }
    return render_to_response("maestros/producto/add.html", c, context_instance=RequestContext(request))


@transaction.atomic
@permission_resource_required
def producto_edit(request, key):
    """
    Actualiza Producto
    """
    id = SecurityKey.is_valid_key(request, key, "producto_upd")
    if not id:
        return Redirect.to_action(request, "index")
    d = None
    try:
        d = get_object_or_404(Producto, id=id)
        try:
            categoria = Categoria.objects.get(id=d.categoria.id)
            if categoria.id:
                d.categoria_nombre = d.categoria.nombre
        except:
            pass
        
        
    except Exception, e:
        Message.error(request, ("Usuario no se encuentra en la base de datos. %s" % e))
        return Redirect.to_action(request, "index")

    if request.method == "POST":
        try:
            sid = transaction.savepoint()  # https://docs.djangoproject.com/en/1.6/topics/db/transactions/#topics-db-transactions-savepoints
            d.codigo = request.POST.get("codigox")
            d.descripcion = request.POST.get("descripcion")
            d.precio_venta = request.POST.get("precio_venta")
            if request.POST.get("fecha_venc"):
                d.fecha_venc = request.POST.get("fecha_venc")
                
            if request.POST.get("categoria_nombre"):
                
                d.categoria, is_created = Categoria.objects.get_or_create(
                    nombre=request.POST.get("categoria_nombre"),
                    )
                
            if Producto.objects.filter(codigo=d.codigo).exclude(id=d.id, headquar_id=d.headquar_id).count() > 0:
                raise Exception("El producto <b>%s</b> ya existe " % d.codigo)
            d.save()
            # raise Exception( "El producto <b>%s</b> ya existe " % d.codigo )
            if d.id:
                Message.info(request, ("Producto <b>%(name)s</b> ha sido actualizado correctamente.") % {"name":d.codigo}, True)
                return Redirect.to_action(request, "index")

        except Exception, e:
            transaction.savepoint_rollback(sid)
            Message.error(request, e)
    categoria_nombre_list = []
    try:
        categoria_nombre_list = json.dumps(list(col["nombre"] + ""  for col in Categoria.objects.values("nombre").filter().order_by("nombre")))
        print "PV=%s" % d.precio_venta
    except Exception, e:
        Message.error(request, e)
    c = {
        "page_module":("Gestión de productos"),
        "page_title":("Actualizar producto."),
        "d":d,
        "categoria_nombre_list":categoria_nombre_list,
        }
    return render_to_response("maestros/producto/edit.html", c, context_instance=RequestContext(request))

@permission_resource_required
@transaction.atomic  # no es necesario pk no tiene transaction
def producto_delete(request, key):
    """
    Elimina producto
    """
    id = SecurityKey.is_valid_key(request, key, "producto_del")
    if not id:
        return Redirect.to_action(request, "index")
    try:
        d = get_object_or_404(Producto, id=id)
    except:
        Message.error(request, ("Producto no se encuentra en la base de datos."))
        return Redirect.to_action(request, "index")
    try:
        # sid = transaction.savepoint()
        d.delete()
        if not d.id:
            Message.info(request, ("Producto <b>%(codigo)s</b> ha sido eliminado correctamente.") % {"codigo":d.codigo}, True)
            return Redirect.to_action(request, "index")
    except Exception, e:
        # transaction.savepoint_rollback(sid)
        Message.error(request, e)
        return Redirect.to_action(request, "index")
# endregion producto
