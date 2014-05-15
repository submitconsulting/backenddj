# _*_ coding: utf-8 _*_
"""
@copyright   Copyright (c) 2014 Submit Consulting
@author      Angel Sullon (@asullom)
@package     rrhh

Descripcion: Implementacion de los controladores de la app rrhh
"""
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
import json
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from apps.utils.decorators import permission_resource_required
from unicodedata import normalize
from apps.utils.security import Redirect, SecurityKey, DataAccessToken
from apps.rrhh.models import Employee
from django.http import HttpResponse
from django.db.models import Q
from apps.utils.messages import Message
from apps.space.models import Headquar
from django.db import transaction
from apps.params.models import Person

# region employee OK
def employee_json_by_filter(request): 
    filters = ('' if request.REQUEST.get('filter') == None else request.REQUEST.get('filter')).strip()
    # print ('filtrs=%s'%(True if filters else False));
    list_db = Employee.objects.filter(
        Q(codigo__contains=filters) | Q(person__first_name__contains=filters) | Q(person__last_name__contains=filters) | Q(id__isnull=True if filters else False),
        headquar=DataAccessToken.get_headquar_id(request.session),
        ) 
    data = list()
    for d in list_db:
        id_key = SecurityKey.get_key(d.id, "employee_upd")
        data.append({ 'id': id_key, 'codigo': d.codigo, 'descripcion': "%s %s" % (d.person.first_name, d.person.last_name) , 'precio_venta': d.contrato_vigente })
    return HttpResponse(
        json.dumps(data),
            content_type="application/json; charset=uft8"
        )

@login_required
@permission_resource_required(template_denied_name="denied_mod_pro.html")
def employee_index(request, field="codigo", value="None", order="-id"):
    """
    Página principal para trabajar con employees
    """
    try:
        headquar = get_object_or_404(Headquar, id=DataAccessToken.get_headquar_id(request.session))
    except:
        Message.error(request, ("Sede no seleccionado o no se encuentra en la base de datos."))
        return Redirect.to(request, "/home/choice_headquar/")

    field = (field if not request.REQUEST.get("field") else request.REQUEST.get("field")).strip()
    value = (value if not request.REQUEST.get("value") else request.REQUEST.get("value")).strip()
    order = (order if not request.REQUEST.get("order") else request.REQUEST.get("order")).strip()
    
    try:
        value_f = "" if value == "None" else value
        column_contains = u"%s__%s" % (field, "contains")
        employee_list = Employee.objects.filter(headquar=headquar, **{ column_contains: value_f }).order_by(order)
        paginator = Paginator(employee_list, 100)
        try:
            employee_page = paginator.page(request.GET.get("page"))
        except PageNotAnInteger:
            employee_page = paginator.page(1)
        except EmptyPage:
            employee_page = paginator.page(paginator.num_pages)
    except Exception, e:
        Message.error(request, e)
    c = {
        "page_module":("Gestión de employees"),
        "page_title":("Listado de employees."),
        
        "employee_page":employee_page,
        "field":field,
        "value":value.replace("/", "-"),
        "order":order,
        }
    return render_to_response("rrhh/employee/index.html", c, context_instance=RequestContext(request))

@permission_resource_required(template_denied_name="denied_mod_pro.html")
@transaction.atomic
def employee_add(request):
    """
    Agrega Employee
    """
    d = Employee()
    d.photo = "personas/default.png"
    if request.method == "POST":
        try:
            sid = transaction.savepoint()
            d.first_name = request.POST.get("first_name")
            d.last_name = request.POST.get("last_name")
            d.photo = request.POST.get("persona_fotografia")
            d.identity_type = request.POST.get("identity_type")
            d.identity_num = request.POST.get("identity_num")
            identity_type_display = dict((x, y) for x, y in Person.IDENTITY_TYPES)[d.identity_type]

            d.codigo = request.POST.get("codigox")
            d.headquar_id = DataAccessToken.get_headquar_id(request.session)
            
            if normalize("NFKD", u"%s %s" % (d.first_name, d.last_name)).encode("ascii", "ignore").lower() in list(
                normalize("NFKD", u"%s %s" % (col["first_name"], col["last_name"])).encode("ascii", "ignore").lower() for col in Person.objects.values("first_name", "last_name").exclude(id=d.id).filter(identity_type=d.identity_type, identity_num=d.identity_num)
                ):
                raise Exception("La persona <b>%s %s</b> con %s:<b>%s</b> ya existe " % (d.first_name, d.last_name, identity_type_display, d.identity_num))
            if Person.objects.filter(identity_type=d.identity_type, identity_num=d.identity_num).count() > 0:
                raise Exception("La persona con %s:<b>%s</b> ya existe " % (identity_type_display, d.identity_num))
            
            person = Person(first_name=d.first_name, last_name=d.last_name, identity_type=d.identity_type, identity_num=d.identity_num, photo=d.photo)
            person.save()
            d.person = person


            if Employee.objects.filter(codigo=d.codigo).exclude(id=d.id, headquar_id=d.headquar_id).count() > 0:
                raise Exception("El employee <b>%s</b> ya existe " % d.codigo)
            d.save()
            if d.id:
                Message.info(request, ("Employee <b>%(name)s</b> ha sido registrado correctamente.") % {"name":d.codigo}, True)
                request.session['id_personal'] = d.id
                return Redirect.to_action(request, "edit")
                
        except Exception, e:
            transaction.savepoint_rollback(sid)
            Message.error(request, e)
    # categoria_nombre_list=[]
    try:
        print ""
        # categoria_nombre_list = json.dumps(list(col["nombre"]+""  for col in Categoria.objects.values("nombre").filter().order_by("nombre")))
    except Exception, e:
        Message.error(request, e)
    c = {
        "page_module":("Gestión de empleados"),
        "page_title":("Agregar empleado."),
        "d":d,
        "IDENTITY_TYPES":Person.IDENTITY_TYPES,
        }
    return render_to_response("rrhh/employee/add.html", c, context_instance=RequestContext(request))

@permission_resource_required(template_denied_name="denied_mod_pro.html")
def employee_choice(request, key):
    """
    Elige Employee
    """
    id = SecurityKey.is_valid_key(request, key, "employee_upd")
    request.session['id_personal'] = id
    return Redirect.to_action(request, "edit")

@permission_resource_required(template_denied_name="denied_mod_pro.html")
@transaction.atomic
def employee_edit(request):
    """
    Actualiza Employee
    """
    # id=SecurityKey.is_valid_key(request, key, "employee_upd")
    id = request.session['id_personal']
    if not id:
        return Redirect.to_action(request, "index")
    d = None
    try:
        d = get_object_or_404(Employee, id=id)
        try:
            person = Person.objects.get(employee=d.id)
            if person.id:
                d.first_name = d.person.first_name
                d.last_name = d.person.last_name
                d.photo = d.person.photo
                d.identity_type = d.person.identity_type
                d.identity_num = d.person.identity_num
        except:
            pass
        
    except Exception, e:
        Message.error(request, ("Employee no se encuentra en la base de datos. %s" % e))
        return Redirect.to_action(request, "index")

    if request.method == "POST":
        try:
            sid = transaction.savepoint()
            d.codigo = request.POST.get("codigox")

            if Employee.objects.filter(codigo=d.codigo).exclude(id=d.id).count() > 0:
                raise Exception("El employee <b>%s</b> ya existe " % d.codigo)
            d.save()
            try:
                person = Person.objects.get(employee=d)
            except:
                person = Person(employee=d)
                person.save()
                pass
            d.first_name = request.POST.get("first_name")
            d.last_name = request.POST.get("last_name")
            d.identity_type = request.POST.get("identity_type")
            d.identity_num = request.POST.get("identity_num")
            identity_type_display = dict((x, y) for x, y in Person.IDENTITY_TYPES)[d.identity_type]
                        
            if normalize("NFKD", u"%s %s" % (d.first_name, d.last_name)).encode("ascii", "ignore").lower() in list(
                normalize("NFKD", u"%s %s" % (col["first_name"], col["last_name"])).encode("ascii", "ignore").lower() for col in Person.objects.values("first_name", "last_name").exclude(id=person.id).filter(identity_type=d.identity_type, identity_num=d.identity_num)
                ):
                raise Exception("La persona <b>%s %s</b> con %s:<b>%s</b> ya existe " % (d.first_name, d.last_name, identity_type_display, d.identity_num))
            
            if Person.objects.exclude(id=person.id).filter(identity_type=d.identity_type, identity_num=d.identity_num).count() > 0:
                raise Exception("La persona con %s:<b>%s</b> ya existe " % (identity_type_display, d.identity_num))
            
            person.first_name = request.POST.get("first_name")
            person.last_name = request.POST.get("last_name")
            person.identity_type = request.POST.get("identity_type")
            person.identity_num = request.POST.get("identity_num")

            person.photo = request.POST.get("persona_fotografia")
            person.save()
            d.photo = person.photo
            if d.id:
                Message.info(request, ("Employee <b>%(name)s</b> ha sido actualizado correctamente.") % {"name":d.codigo}, True)
                # return Redirect.to_action(request, "index")

        except Exception, e:
            transaction.savepoint_rollback(sid)
            Message.error(request, e)

    c = {
        "page_module":("Gestión de employees"),
        "page_title":("Actualizar employee."),
        "d":d,
        "IDENTITY_TYPES":Person.IDENTITY_TYPES,
        }
    return render_to_response("rrhh/employee/edit.html", c, context_instance=RequestContext(request))

@permission_resource_required(template_denied_name="denied_mod_pro.html")
@transaction.atomic
def employee_delete(request, key):
    """
    Elimina employee
    """
    id = SecurityKey.is_valid_key(request, key, "employee_del")
    if not id:
        return Redirect.to_action(request, "index")
    try:
        d = get_object_or_404(Employee, id=id)
    except:
        Message.error(request, ("Employee no se encuentra en la base de datos."))
        return Redirect.to_action(request, "index")
    try:
        d.delete()
        if not d.id:
            Message.info(request, ("Employee <b>%(codigo)s</b> ha sido eliminado correctamente.") % {"codigo":d.codigo}, True)
            return Redirect.to_action(request, "index")
    except Exception, e:
        Message.error(request, e)
        return Redirect.to_action(request, "index")


@permission_resource_required
def employee_person_search(request, field="first_name", value="None"):
    """
    Muestra el listado de Person 
    """
    field = (field if not request.REQUEST.get("field") else request.REQUEST.get("field")).strip()
    value = (value if not request.REQUEST.get("value") else request.REQUEST.get("value")).strip()

    value_f = "None" if value == "None" else value
    column_contains = u"%s__%s" % (field, "contains")
    headquar=DataAccessToken.get_headquar_id(request.session)
    employee_list= Employee.objects.values("id").filter(headquar=headquar)
    person_list = Person.objects.exclude(employee__in=employee_list).filter(**{ column_contains: value_f }).order_by("last_name", "first_name") #.distinct()  # Trae todo
    
    c = {
        "page_module":("Personas"),
        "page_title":("Resultado de personas que no son empleados para esta sede."),
        "person_list": person_list,

        "field":field,
        "value":value.replace("/", "-"),
        }
    return render_to_response("rrhh/employee/person_search.html", c, context_instance=RequestContext(request))

@permission_resource_required
@transaction.atomic
def employee_add_from_person(request, key):
    """
    Agrega employee desde person
    """
    id = SecurityKey.is_valid_key(request, key, "employee_add_from_person")
    if not id:
        return Redirect.to_action(request, "index")
    
    d = None
    try:
        d = get_object_or_404(Person, id=id)
    except Exception, e:
        Message.error(request, ("Person no se encuentra en la base de datos. %s" % e))
        return Redirect.to_action(request, "index")
    
    if request.method == "POST":
        try:
            sid = transaction.savepoint()
            headquar = Headquar.objects.get(id=DataAccessToken.get_headquar_id(request.session))
            
            d.first_name = request.POST.get("first_name")
            d.last_name = request.POST.get("last_name")
            d.photo = request.POST.get("persona_fotografia")
            d.identity_type = request.POST.get("identity_type")
            d.identity_num = request.POST.get("identity_num")
            identity_type_display = dict((x, y) for x, y in Person.IDENTITY_TYPES)[d.identity_type]
            
            d.codigo = request.POST.get("codigox")
            #d.headquar_id = DataAccessToken.get_headquar_id(request.session)
            employee = Employee()
            if Employee.objects.exclude(id=d.id,headquar=headquar).filter(codigo=d.codigo).count() > 0:
                raise Exception("El employee <b>%s</b> ya existe " % d.codigo)
            employee = Employee(codigo=d.codigo, person=d, headquar=headquar)
            employee.save()
            person = d
            if normalize("NFKD", u"%s %s" % (d.first_name, d.last_name)).encode("ascii", "ignore").lower() in list(
                normalize("NFKD", u"%s %s" % (col["first_name"], col["last_name"])).encode("ascii", "ignore").lower() for col in Person.objects.values("first_name", "last_name").exclude(id=person.id).filter(identity_type=d.identity_type, identity_num=d.identity_num)
                ):
                raise Exception("La persona <b>%s %s</b> con %s:<b>%s</b> ya existe " % (d.first_name, d.last_name, identity_type_display, d.identity_num))
            if Person.objects.exclude(id=person.id).filter(identity_type=d.identity_type, identity_num=d.identity_num).count() > 0:
                raise Exception("La persona con %s:<b>%s</b> ya existe " % (identity_type_display, d.identity_num))
            
            
            person.first_name = request.POST.get("first_name")
            person.last_name = request.POST.get("last_name")
            person.identity_type = request.POST.get("identity_type")
            person.identity_num = request.POST.get("identity_num")
            person.photo = request.POST.get("persona_fotografia")
            person.save()
            d.photo = person.photo
            
            d = employee
    
            if d.id:
                Message.info(request, ("Empleado <b>%(name)s</b> ha sido agregado desde persona correctamente.") % {"name":d.codigo}, True)
                request.session['id_personal'] = d.id
                #request.path = "/rrhh/employee/edit/"
                return Redirect.to_action(request, "edit")
        except Exception, e:
            transaction.savepoint_rollback(sid)
            Message.error(request, e)
    
    c = {
        "page_module":("Gestión de empleados"),
        "page_title":("Agregar empleado de person ."),
        "d":d,
        "IDENTITY_TYPES":Person.IDENTITY_TYPES,
        }
    return render_to_response("rrhh/employee/add_from_person.html", c, context_instance=RequestContext(request))



@permission_resource_required(template_denied_name="denied_mod_pro.html")
@transaction.atomic
def employee_add_all(request):
    """
    Agrega Employees
    """
    d = Employee()
    n = 1000
    i = 101
    k = i
    while i <= n:
        print i
        d = Employee()
        d.codigo = "00%s" % i
        d.headquar_id = DataAccessToken.get_headquar_id(request.session)
        person = Person(first_name="NOMB%s" % i, last_name="APELL%s" % i, identity_num="00%s0" % i)
        person.save()
        d.person = person
        d.save()
        i = i + 1
    return HttpResponse("%s registros insertados " % (n - k+1))
# endregion employee
