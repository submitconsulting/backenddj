# _*_ coding: utf-8 _*_
"""
@copyright   Copyright (c) 2014 Submit Consulting
@author      Angel Sullon (@asullom)
@package     params

Descripcion: Implementacion de los controladores de la app params
"""
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from apps.utils.messages import Message
from apps.utils.logs import Logger
from django.utils.translation import ugettext as _
from apps.utils.decorators import permission_resource_required
from unicodedata import normalize
from apps.utils.security import Redirect, SecurityKey
from django.db import transaction
from apps.params.models import Locality, LocalityType
import datetime
import locale
import time
from apps.params.models import Person
from apps.params.forms import LocalityAddForm
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.decorators import login_required
locale.setlocale(locale.LC_ALL, "") #print locale.LC_TIME

from django.utils import translation
#import logging
#logger = logging.getLogger("log")

#import csv
#from django.http import HttpResponse
from django.contrib.admin.models import LogEntry, ADDITION
from django.utils.encoding import force_text, force_unicode
from django.contrib import admin
# Locality
@login_required
@permission_resource_required
def locality_index(request, field="name", value="None", order="-id"):
    """
    Lista paginada de locality
    """
    #admin.site.add_action(locality_index)
    
    #Message.error(request, "eeeú3")
        
    #logger.warning("mgeésaaa ")
    #Logger.warning(request, "Mi error oculto")
    
    
    field = (field if not request.REQUEST.get("field") else request.REQUEST.get("field")).strip()
    value = (value if not request.REQUEST.get("value") else request.REQUEST.get("value")).strip()
    order = (order if not request.REQUEST.get("order") else request.REQUEST.get("order")).strip()
    
    print datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
    print time.time()
    print locale.getlocale() #('Spanish_Peru', '1252')
    print locale.getdefaultlocale()#('es_PE', 'cp1252')
    print translation.get_language()# es-pe
    print translation.to_locale(translation.get_language())#es_PE
    print datetime.datetime.now().strftime("%a, %d %b %y")#mié, 16 abr 14
    
    locality_page = None
    try:
        value_f = "" if value == "None" else value  # (true or false) ? value1:value2
        column_contains = u"%s__%s" % (field, "contains")  # SEL-- WHERE name LIKE %an%

        if field == "is_active":
            value_f = "0" if value.lower() == "no" else value
            column_contains = u"%s" % (field) #.filter(is_active=True)
            
        locality_list = Locality.objects.filter(**{ column_contains: value_f }).order_by(order)
        paginator = Paginator(locality_list, 25)  # Show num_rows=25 contacts per page
        try:
            locality_page = paginator.page(request.GET.get("page"))
        except PageNotAnInteger:
            locality_page = paginator.page(1)
        except EmptyPage:
            locality_page = paginator.page(paginator.num_pages)
    except Exception, e:
        Message.error(request, e)
    c = {
        "page_module":_("Locality"),
        "page_title":_("Localities list."),
        
        "locality_page":locality_page,
        "field":field,
        "value":value.replace("/", "-"),
        "order":order,
        }

    return render_to_response("params/locality/index.html", c, context_instance=RequestContext(request))

@permission_resource_required
def locality_report(request, field="name", value="None", order="-id"):
    field = (field if not request.REQUEST.get("field") else request.REQUEST.get("field")).strip()
    value = (value if not request.REQUEST.get("value") else request.REQUEST.get("value")).strip()
    order = (order if not request.REQUEST.get("order") else request.REQUEST.get("order")).strip()
    
    try:
        value = "" if value == "None" else value
        column_contains = u"%s__%s" % (field, "contains")

        locality_list = Locality.objects.filter(**{ column_contains: value }).order_by(order)
    except Exception, e:
        Message.error(request, e)
    c = {
        "page_module":_("Locality"),
        "page_title":_("Localities report."),
        "locality_list":locality_list,
        }
    return render_to_response("params/locality/report.html", c, context_instance=RequestContext(request))

@permission_resource_required(template_denied_name="denied_mod_backend.html")
def locality_add(request):
    d = Locality()
    d.msnm = 0
    d.date_create =""
    if request.method == "POST":
        try:
            # Aquí asignar los datos
            d.name = request.POST.get("name")
            d.msnm = request.POST.get("msnm")
            d.date_create = None
            if request.POST.get("date_create"):
                d.date_create = request.POST.get("date_create")
            if request.POST.get("locality_type_id"):
                d.locality_type = LocalityType.objects.get(id=request.POST.get("locality_type_id"))

            if normalize("NFKD", u"%s" % d.name).encode("ascii", "ignore").lower() in list(
                normalize("NFKD", u"%s" % col["name"]).encode("ascii", "ignore").lower() for col in Locality.objects.values("name").exclude(id=d.id)  # puede .filter()
                ):
                raise Exception(_("Locality <b>%(name)s</b> name's already in use.") % {"name":d.name})  # El nombre x para localidad ya existe.
            # salvar registro
            d.save()
            if d.id:
                Message.info(request, ("Localidad <b>%(name)s</b> ha sido registrado correctamente.") % {"name":d.name}, True)
                # return Redirect.to(request, "/params/locality/index/")#usar to(...) cuando la acción está implementada en otra app, ver sad.views.user_index
                return Redirect.to_action(request, "index")  # usar to_action(...) cuando la acción está implementada en este archivo
        except Exception, e:
            Message.error(request, e)
    try:
        locality_type_list = LocalityType.objects.all().order_by("name")
    except Exception, e:
        Message.error(request, e)
    c = {
        "page_module":_("Locality"),
        "page_title":_("New locality."),
        "d":d,
        "locality_type_list":locality_type_list,
        }
    return render_to_response("params/locality/add.html", c, context_instance=RequestContext(request))

def locality_add_form(request):
    form = LocalityAddForm()
    if request.method == "POST":
        form = LocalityAddForm(request.POST)
        if form.is_valid():
            #name = form.cleaned_data['name']
            #location = form.cleaned_data['location']
            #locality_type = form.cleaned_data['locality_type'].id
            #p = Locality()
            #p.name = name
            #p.location = location
            #p.locality_type_id = locality_type
            #p.save()
            form.save()
            return Redirect.to_action(request, "index")   
    c = {
        "page_module":_("Locality"),
        "page_title":_("New locality."),
        "form":form,
        #"locality_type_list":locality_type_list,
        }
    return render_to_response('params/locality/add_form.html', c ,context_instance = RequestContext(request))


@transaction.atomic
@permission_resource_required
def locality_edit(request, key):
    id = SecurityKey.is_valid_key(request, key, "locality_upd")
    if not id:
        return Redirect.to_action(request, "index")
    d = None
    try:
        d = get_object_or_404(Locality, id=id)  # Locality.objects.get(id=id)
    except:  # Locality.DoesNotExist
        Message.error(request, _("Locality not found in the database."))
        return Redirect.to_action(request, "index")

    if request.method == "POST":
        try:
            sid = transaction.savepoint()  # begin transaction, no amerita el decorador @transaction.atomic pero dejadlo para las nuevas version 

            # Aquí asignar los datos
            d.name = request.POST.get("name")
            d.msnm = request.POST.get("msnm")
            if request.POST.get("date_create"):
                d.date_create = request.POST.get("date_create")
            d.is_active = True

            # para probar transaction 
            # locality_type=LocalityType()
            # locality_type.name="Rural5"
            # if LocalityType.objects.filter(name = locality_type.name).count() > 0:
            #     raise Exception(_("LocalityType <b>%(name)s</b> name's already in use.") % {"name":locality_type.name}) #trhow new Exception("msg")
            # locality_type.save()
            # d.locality_type=locality_type

            if normalize("NFKD", u"%s" % d.name).encode("ascii", "ignore").lower() in list(
                normalize("NFKD", u"%s" % col["name"]).encode("ascii", "ignore").lower() for col in Locality.objects.values("name").exclude(id=d.id)  # puede .filter()
                ):
                raise Exception(_("Locality <b>%(name)s</b> name's already in use.") % {"name":d.name})  # trhow new Exception("msg")
            # salvar registro
            d.save()
            # para probar transaction
            # raise Exception("Error para no salvar. Si funciona")
            if d.id:
                # transaction.savepoint_commit(sid) se colocaría solo al final, pero no amerita pk ya está decorado con @transaction.atomic
                Message.info(request, ("Localidad <b>%(name)s</b> ha sido actualizado correctamente.") % {"name":d.name}, True)
                return Redirect.to_action(request, "index")
        except Exception, e:
            transaction.savepoint_rollback(sid)  # para reversar en caso de error en alguna de las tablas
            Message.error(request, e)
    try:
        locality_type_list = LocalityType.objects.all().order_by("name")
    except Exception, e:
        Message.error(request, e)
    c = {
        "page_module":_("Locality"),
        "page_title":_("Update locality."),
        "d":d,
        "locality_type_list":locality_type_list,
        }
    return render_to_response("params/locality/edit.html", c, context_instance=RequestContext(request))

@permission_resource_required
def locality_delete(request, key):
    id = SecurityKey.is_valid_key(request, key, "locality_del")
    if not id:
        return Redirect.to_action(request, "index")
    try:
        d = get_object_or_404(Locality, id=id)  # Locality.objects.get(id=id)
    except:  # Locality.DoesNotExist
        Message.error(request, _("Locality not found in the database."))
        return Redirect.to_action(request, "index")
    try:
        # rastreando dependencias
        if d.headquart_set.count() > 0:
            raise Exception(("Localidad <b>%(name)s</b> está asignado en headquart.") % {"name":d.name})
        
        d.delete()
        if not d.id:
            Message.info(request, ("Localidad <b>%(name)s</b> ha sido eliminado correctamente.") % {"name":d.name}, True)
            return Redirect.to_action(request, "index")
    except Exception, e:
        Message.error(request, e)
        return Redirect.to_action(request, "index")

@permission_resource_required
def locality_state(request, state, key):
    """
    Inactiva y reactiva el estado de la Localidad
    """
    id = SecurityKey.is_valid_key(request, key, "locality_%s" % state)
    if not id:
        return Redirect.to_action(request, "index")
    try:
        d = get_object_or_404(Locality, id=id)
    except:
        Message.error(request, ("Localidad no se encuentra en la base de datos."))
        return Redirect.to_action(request, "index")
    try:
        if state == "inactivar" and d.is_active == False:
            Message.error(request, ("Localidad ya se encuentra inactivo."))
        else:
            if state == "reactivar" and d.is_active == True:
                Message.error(request, ("Localidad ya se encuentra activo."))
            else:
                d.is_active = (True if state == "reactivar" else False)
                d.save()
                if d.id:
                    if d.is_active:
                        Message.info(request, ("Localidad <b>%(name)s</b> ha sido reactivado correctamente.") % {"name":d.name}, True)
                    else:
                        Message.info(request, ("Localidad <b>%(name)s</b> ha sido inactivado correctamente.") % {"name":d.name}, True)
                    return Redirect.to_action(request, "index")
    except Exception, e:
        Message.error(request, e)
        return Redirect.to_action(request, "index")
# Fin Locality

'''
def person_search(request, field="first_name", value="None"):
    """
    Muestra el listado de Person 
    """
    field = (field if not request.REQUEST.get("field") else request.REQUEST.get("field")).strip()
    value = (value if not request.REQUEST.get("value") else request.REQUEST.get("value")).strip()

    value_f = "None" if value == "None" else value
    column_contains = u"%s__%s" % (field, "contains")

    person_list = Person.objects.filter(**{ column_contains: value_f }).order_by("last_name", "first_name") #.distinct()  # Trae todo
    
    c = {
        "page_module":("Personas"),
        "page_title":("Listado de personas registrados en el sistema."),
        "person_list": person_list,

        "field":field,
        "value":value.replace("/", "-"),
        }
    return render_to_response("params/person/search.html", c, context_instance=RequestContext(request))
'''
