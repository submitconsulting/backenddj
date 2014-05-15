# _*_ coding: utf-8 _*_
"""
@copyright   Copyright (c) 2014 Submit Consulting
@author      Angel Sullon (@asullom)
@package     space

Descripcion: Implementacion de los controladores de la app space
"""
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from django.db.models import Avg, Max, Min, Count
from unicodedata import normalize
from apps.utils.decorators import permission_resource_required
from apps.utils.security import SecurityKey, DataAccessToken, Redirect
from apps.utils.messages import Message
from apps.space.models import Solution, Association, Enterprise, Headquar
from apps.params.models import Locality
from apps.utils.upload import Upload

# region headquar OK
@permission_resource_required
def headquar_index(request):
    """
    Página principal para trabajar con sedes
    """
    try:
        enterprise = get_object_or_404(Enterprise, id=DataAccessToken.get_enterprise_id(request.session))
    except:
        Message.error(request, ("Empresa no seleccionada o no se encuentra en la base de datos."))
        return Redirect.to(request, "/home/choice_headquar/")
    try:
        headquar_list = Headquar.objects.filter(enterprise_id=DataAccessToken.get_enterprise_id(request.session)).order_by("-id")
    except Exception, e:
        Message.error(request, e)
    c = {
        "page_module":("Cuenta"),
        "page_title":("Listado de sedes de la empresa."),
        "headquar_list":headquar_list,
        }
    return render_to_response("space/headquar/index.html", c, context_instance=RequestContext(request))

@permission_resource_required
@transaction.atomic
def headquar_add(request):
    """
    Agrega sede
    """
    d = Headquar()
    d.phone = ""
    d.address = ""
    if request.method == "POST":
        try:
            sid = transaction.savepoint()
            d.name = request.POST.get("name")
            d.phone = request.POST.get("phone")
            d.address = request.POST.get("address")
            d.is_main = False
            d.locality_name = request.POST.get("locality_name")
            if request.POST.get("locality_name"):
                d.locality, is_locality_created = Locality.objects.get_or_create(
                    name=request.POST.get("locality_name"),  # name__iexact
                    )
            d.association_id = DataAccessToken.get_association_id(request.session)
            d.enterprise_id = DataAccessToken.get_enterprise_id(request.session)

            if normalize("NFKD", u"%s" % d.name).encode("ascii", "ignore").lower() in list(
                normalize("NFKD", u"%s" % col["name"]).encode("ascii", "ignore").lower() for col in Headquar.objects.values("name").exclude(id=d.id).filter(enterprise_id=d.enterprise_id)
                ):
                raise Exception("La sede <b>%s</b> ya existe " % (d.name))
            d.save()
            if d.id:
                Message.info(request, ("Sede <b>%(name)s</b> ha sido registrado correctamente.") % {"name":d.name})
                return Redirect.to_action(request, "index")
        except Exception, e:
            transaction.savepoint_rollback(sid)
            Message.error(request, e)
    try:
        locality_name_list = json.dumps(list(col["name"] + ""  for col in Locality.objects.values("name").filter().order_by("name")))
    except Exception, e:
        Message.error(request, e)
    c = {
        "page_module":("Cuenta"),
        "page_title":("Agregar sede."),
        "d":d,
        "locality_name_list":locality_name_list,
        }
    return render_to_response("space/headquar/add.html", c, context_instance=RequestContext(request))

@permission_resource_required
@transaction.atomic
def headquar_edit(request, key):
    """
    Actualiza sede
    """
    id = SecurityKey.is_valid_key(request, key, "headquar_upd")
    if not id:
        return Redirect.to_action(request, "index")
    d = None
    try:
        d = get_object_or_404(Headquar, id=id)
        if d.locality:
            d.locality_name = d.locality.name
    except:
        Message.error(request, ("Sede no se encuentra en la base de datos."))
        return Redirect.to_action(request, "index")

    if request.method == "POST":
        try:
            sid = transaction.savepoint()
            d.name = request.POST.get("name")
            d.phone = request.POST.get("phone")
            d.address = request.POST.get("address")
            d.locality_name = request.POST.get("locality_name").strip()
            if request.POST.get("locality_name").strip():
                d.locality, is_locality_created = Locality.objects.get_or_create(
                    name=request.POST.get("locality_name").strip(),  # name__iexact
                    )
            if normalize("NFKD", u"%s" % d.name).encode("ascii", "ignore").lower() in list(
                normalize("NFKD", u"%s" % col["name"]).encode("ascii", "ignore").lower() for col in Headquar.objects.values("name").exclude(id=d.id).filter(enterprise_id=d.enterprise_id)
                ):
                raise Exception("La sede <b>%s</b> ya existe " % (d.name))

            # salvar registro
            d.save()
            if d.id:
                Message.info(request, ("Sede <b>%(name)s</b> ha sido actualizado correctamente.") % {"name":d.name})
                return Redirect.to_action(request, "index")

        except Exception, e:
            transaction.savepoint_rollback(sid)
            Message.error(request, e)
    try:
        locality_name_list = json.dumps(list(" " + col["name"] + ""  for col in Locality.objects.values("name").filter().order_by("name")))
        # locality_name_list = json.dumps(list(x[1]) for x in Association.TYPES) )
    except Exception, e:
        Message.error(request, e)
    c = {
        "page_module":("Cuenta"),
        "page_title":("Actualizar sede."),
        "d":d,
        "locality_name_list":locality_name_list,
        }
    return render_to_response("space/headquar/edit.html", c, context_instance=RequestContext(request))

@permission_resource_required
def headquar_change_association(request, key):
    """
    Cambia de asociación a la sede
    """
    id = SecurityKey.is_valid_key(request, key, "headquar_cha")
    if not id:
        return Redirect.to_action(request, "index")
    d = None

    try:
        d = get_object_or_404(Headquar, id=id)
        if d.association:
            d.association_name = d.association.name
    except:
        Message.error(request, ("Sede no se encuentra en la base de datos."))
        return Redirect.to_action(request, "index")

    if request.method == "POST":
        try:
            # d.association_id = DataAccessToken.get_association_id(request.session)
            d.association_name = request.POST.get("association_name")
            try:
                d.association = Association.objects.get(name=d.association_name)
            except:
                raise Exception("La asociación <b>%s</b> no existe, vuelva a intentar " % (request.POST.get("association_name")))
            # salvar registro
            d.save()
            if d.id:
                Message.info(request, ("Sede <b>%(name)s</b> ha sido cambiado de asociación correctamente.") % {"name":d.name})
                return Redirect.to_action(request, "index")

        except Exception, e:
            
            Message.error(request, e)
    try:
        association_name_list = json.dumps(list(col["name"] + ""  for col in Association.objects.values("name").filter(is_active=True).order_by("name")))

    except Exception, e:
        Message.error(request, e)
    c = {
        "page_module":("Cuenta"),
        "page_title":("Cambiar de asociación a la sede."),
        "d":d,
        "association_name_list":association_name_list,
        }
    return render_to_response("space/headquar/change_association.html", c, context_instance=RequestContext(request))

@permission_resource_required
def headquar_state(request, state, key):
    """
    Inactiva y reactiva el estado de la sede
    """
    id = SecurityKey.is_valid_key(request, key, "headquar_%s" % state)
    if not id:
        return Redirect.to_action(request, "index")
    try:
        d = get_object_or_404(Headquar, id=id)
    except:
        Message.error(request, ("Sede no se encuentra en la base de datos."))
        return Redirect.to_action(request, "index")
    try:
        if state == "inactivar" and d.is_active == False:
            Message.error(request, ("Sede ya se encuentra inactivo."))
        else:
            if state == "reactivar" and d.is_active == True:
                Message.error(request, ("Sede ya se encuentra activo."))
            else:
                d.is_active = (True if state == "reactivar" else False)
                d.save()
                if d.id:
                    if d.is_active:
                        Message.info(request, ("Sede <b>%(name)s</b> ha sido reactivado correctamente.") % {"name":d.name}, True)
                    else:
                        Message.info(request, ("Sede <b>%(name)s</b> ha sido inactivado correctamente.") % {"name":d.name}, True)
                    return Redirect.to_action(request, "index")
    except Exception, e:
        Message.error(request, e)
        return Redirect.to_action(request, "index")

@permission_resource_required
def headquar_delete(request, key):
    """
    Elimina sede
    """
    id = SecurityKey.is_valid_key(request, key, "headquar_del")
    if not id:
        return Redirect.to_action(request, "index")
    try:
        d = get_object_or_404(Headquar, id=id)
    except:
        Message.error(request, ("Sede no se encuentra en la base de datos."))
        return Redirect.to_action(request, "index")
    try:
        if d.enterprise.headquar_set.count() == 1:
            raise Exception(("Empresa <b>%(name)s</b> no puede quedar sin ninguna sede.") % {"name":d.enterprise.name})
        if d.userprofileheadquar_set.count() > 0:
            raise Exception(("Sede <b>%(name)s de %(empresa)s</b> tiene usuarios y grupos asignados.") % {"name":d.name, "empresa":d.enterprise.name})
        
        # agregue aquí sus otras relgas de negocio
        d.delete()
        if not d.id:
            Message.info(request, ("Sede <b>%(name)s de %(empresa)s</b> ha sido eliminado correctamente.") % {"name":d.name, "empresa":d.enterprise.name}, True)
            return Redirect.to_action(request, "index")
    except Exception, e:
        Message.error(request, e)
        return Redirect.to_action(request, "index")
# endregion headquar

# region enterprise OK
@permission_resource_required
def enterprise_index(request):
    """
    Página principal para trabajar con empresas
    """
    try:
        d = get_object_or_404(Association, id=DataAccessToken.get_association_id(request.session))
    except:
        Message.error(request, ("Asociación no seleccionada o no se encuentra en la base de datos."))
        return Redirect.to(request, "/home/choice_headquar/")
    enterprise_list = None
    try:
        subq = "SELECT COUNT(*) as count_sedes FROM space_headquar WHERE space_headquar.enterprise_id = space_enterprise.id"  # mejor usar {{ d.headquar_set.all.count }} y listo, trate de no usar {{ d.num_sedes_all }}
        # enterprise_list = Enterprise.objects.filter(headquar__association_id=DataAccessToken.get_association_id(request.session)).annotate(num_sedes=Count("headquar")).order_by("-id").distinct().extra(select={"num_sedes_all": subq})
        enterprise_list = Enterprise.objects.filter(headquar__association_id=DataAccessToken.get_association_id(request.session)).annotate(num_sedes=Count("headquar")).order_by("-id").distinct()
        # enterprise_list2= Enterprise.objects.filter(headquar__enterprise_id=DataAccessToken.get_enterprise_id(request.session)).annotate(num_sedes_all=Count("headquar")).distinct()
        # enterprise_list =enterprise_list1.add(num_sedes_all="e")
        # enterprise_list = chain(enterprise_list1, enterprise_list2)
        # enterprise_list= [s.id for s in sets.Set(enterprise_list1).intersection(sets.Set(enterprise_list2))]
        # enterprise_list=enterprise_list.distinct()
    except Exception, e:
        Message.error(request, e)
    c = {
        "page_module":("Cuenta"),
        "page_title":("Listado de empresas con sedes vinculadas a la asociación."),
        "enterprise_list":enterprise_list,
        }
    return render_to_response("space/enterprise/index.html", c, context_instance=RequestContext(request))

@csrf_exempt
def enterprise_upload(request):
    """
    Sube logo
    """
    data = {}
    try:
        filename = Upload.save_file(request.FILES["logo"], "empresas/")
        data ["name"] = "%s" % filename
    except Exception, e:
        Message.error(request, e)
    return HttpResponse(json.dumps(data))

@permission_resource_required
@transaction.atomic
def enterprise_add(request):
    """
    Agrega empresa dentro de una asociación, para ello deberá agregarse con una sede Principal
    """
    d = Enterprise()
    d.sede = "Principal"
    if request.method == "POST":
        try:
            sid = transaction.savepoint()
            d.name = request.POST.get("name")
            d.tax_id = request.POST.get("tax_id")
            d.type_e = request.POST.get("type_e")
            d.solution_id = request.POST.get("solution_id")
            # solution=Solution.objects.get(id=d.solution_id) #no es necesario
            if normalize("NFKD", u"%s" % d.name).encode("ascii", "ignore").lower() in list(
                normalize("NFKD", u"%s" % col["name"]).encode("ascii", "ignore").lower() for col in Enterprise.objects.values("name").exclude(id=d.id)
                ):
                raise Exception(("Empresa <b>%(name)s</b> ya existe.") % {"name":d.name})

            if Enterprise.objects.exclude(id=d.id).filter(tax_id=d.tax_id).count() > 0:
                raise Exception("La empresa con RUC <b>%s</b> ya existe " % (d.tax_id))

            d.save()

            headquar = Headquar()
            headquar.name = request.POST.get("sede")
            headquar.association_id = DataAccessToken.get_association_id(request.session)
            headquar.enterprise = d

            if normalize("NFKD", u"%s" % headquar.name).encode("ascii", "ignore").lower() in list(
                normalize("NFKD", u"%s" % col["name"]).encode("ascii", "ignore").lower() for col in Headquar.objects.values("name").exclude(id=headquar.id).filter(enterprise_id=headquar.enterprise_id)
                ):
                raise Exception("La sede <b>%s</b> ya existe " % (headquar.name))

            headquar.save()

            if d.id:
                Message.info(request, ("Empresa <b>%(name)s</b> ha sido registrado correctamente.") % {"name":d.name})
                return Redirect.to_action(request, "index")
        except Exception, e:
            transaction.savepoint_rollback(sid)
            Message.error(request, e)
    try:
        solution_list = Solution.objects.filter(is_active=True).order_by("id")
    except Exception, e:
        Message.error(request, e)
    c = {
        "page_module":("Cuenta"),
        "page_title":("Agregar empresa dentro de la asociación."),
        "d":d,
        "TYPES":Enterprise.TYPES,
        "solution_list":solution_list,
        }
    return render_to_response("space/enterprise/add.html", c, context_instance=RequestContext(request))

@permission_resource_required
@transaction.atomic
def enterprise_edit(request, key):
    """
    Actualiza empresa
    """
    id = SecurityKey.is_valid_key(request, key, "enterprise_upd")
    if not id:
        return Redirect.to_action(request, "index")
    d = None

    try:
        d = get_object_or_404(Enterprise, id=id)
    except:
        Message.error(request, ("Empresa no se encuentra en la base de datos."))
        return Redirect.to_action(request, "index")

    if request.method == "POST":
        try:
            sid = transaction.savepoint()
            d.name = request.POST.get("name")
            d.tax_id = request.POST.get("tax_id")
            d.type_e = request.POST.get("type_e")
            d.solution_id = request.POST.get("solution_id")
            # solution=Solution.objects.get(id=d.solution_id) #no es necesario

            if normalize("NFKD", u"%s" % d.name).encode("ascii", "ignore").lower() in list(
                normalize("NFKD", u"%s" % col["name"]).encode("ascii", "ignore").lower() for col in Enterprise.objects.values("name").exclude(id=d.id)
                ):
                raise Exception(("Empresa <b>%(name)s</b> ya existe.") % {"name":d.name})

            if Enterprise.objects.exclude(id=d.id).filter(tax_id=d.tax_id).count() > 0:
                raise Exception("La empresa con RUC <b>%s</b> ya existe " % (d.tax_id))

            # salvar registro
            d.save()
            if d.id:
                Message.info(request, ("Empresa <b>%(name)s</b> ha sido actualizado correctamente.") % {"name":d.name})
                return Redirect.to_action(request, "index")

        except Exception, e:
            transaction.savepoint_rollback(sid)
            Message.error(request, e)
    try:
        solution_list = Solution.objects.filter(is_active=True).order_by("id")
    except Exception, e:
        Message.error(request, e)
    c = {
        "page_module":("Cuenta"),
        "page_title":("Actualizar sede."),
        "d":d,
        "TYPES":Enterprise.TYPES,
        "solution_list":solution_list,
        }
    return render_to_response("space/enterprise/edit.html", c, context_instance=RequestContext(request))

@permission_resource_required
@transaction.atomic
def enterprise_edit_current(request):
    """
    Actualiza datos de la empresa a la que ingresó el usuario
    """
    d = Enterprise()
    try:
        d = get_object_or_404(Enterprise, id=DataAccessToken.get_enterprise_id(request.session))
    except:
        Message.error(request, ("Empresa no seleccionada o no se encuentra en la base de datos."))
        return Redirect.to(request, "/home/choice_headquar/")

    if request.method == "POST":
        try:
            sid = transaction.savepoint()
            d.name = request.POST.get("name")
            d.tax_id = request.POST.get("tax_id")
            d.type_e = request.POST.get("type_e")
            d.solution_id = request.POST.get("solution_id")
            d.logo = request.POST.get("empresa_logo")
            # solution=Solution.objects.get(id=d.solution_id) #no es necesario
            if normalize("NFKD", u"%s" % d.name).encode("ascii", "ignore").lower() in list(
                normalize("NFKD", u"%s" % col["name"]).encode("ascii", "ignore").lower() for col in Enterprise.objects.values("name").exclude(id=d.id)
                ):
                raise Exception(("Empresa <b>%(name)s</b> ya existe.") % {"name":d.name})

            if Enterprise.objects.exclude(id=d.id).filter(tax_id=d.tax_id).count() > 0:
                raise Exception("La empresa con RUC <b>%s</b> ya existe " % (d.tax_id))

            # salvar registro
            d.save()
            if d.id:
                Message.info(request, ("Empresa <b>%(name)s</b> ha sido actualizado correctamente.") % {"name":d.name})

        except Exception, e:
            transaction.savepoint_rollback(sid)
            Message.error(request, e)
    try:
        solution_list = Solution.objects.filter(is_active=True).order_by("id")
    except Exception, e:
        Message.error(request, e)
    c = {
        "page_module":("Cuenta"),
        "page_title":("Información de la empresa."),
        "d":d,
        "TYPES":Enterprise.TYPES,
        "solution_list":solution_list,
        }
    return render_to_response("space/enterprise/edit_current.html", c, context_instance=RequestContext(request))

@permission_resource_required
def enterprise_state(request, state, key):
    """
    Inactiva y reactiva el estado de la sede
    """
    id = SecurityKey.is_valid_key(request, key, "enterprise_%s" % state)
    if not id:
        return Redirect.to_action(request, "index")
    try:
        d = get_object_or_404(Enterprise, id=id)
    except:
        Message.error(request, ("Empresa no se encuentra en la base de datos."))
        return Redirect.to_action(request, "index")
    try:
        if state == "inactivar" and d.is_active == False:
            Message.error(request, ("Empresa ya se encuentra inactivo."))
        else:
            if state == "reactivar" and d.is_active == True:
                Message.error(request, ("Empresa ya se encuentra activo."))
            else:
                d.is_active = (True if state == "reactivar" else False)
                d.save()
                if d.id:
                    if d.is_active:
                        Message.info(request, ("Empresa <b>%(name)s</b> ha sido reactivado correctamente.") % {"name":d.name}, True)
                    else:
                        Message.info(request, ("Empresa <b>%(name)s</b> ha sido inactivado correctamente.") % {"name":d.name}, True)
                    return Redirect.to_action(request, "index")
    except Exception, e:
        Message.error(request, e)
        return Redirect.to_action(request, "index")

@permission_resource_required
@transaction.atomic
def enterprise_delete(request, key):
    """
    Elimina empresa con todas sus sedes
    """
    id = SecurityKey.is_valid_key(request, key, "enterprise_del")
    if not id:
        return Redirect.to_action(request, "index")
    try:
        d = get_object_or_404(Enterprise, id=id)
    except:
        Message.error(request, ("Empresa no se encuentra en la base de datos."))
        return Redirect.to_action(request, "index")
    try:
        sid = transaction.savepoint()
        association = Association.objects.get(id=DataAccessToken.get_association_id(request.session))
        if Enterprise.objects.filter(headquar__association_id=DataAccessToken.get_association_id(request.session)).count() == 1:
            raise Exception(("Asociación <b>%(name)s</b> no puede quedar sin ninguna sede asociada.") % {"name":association.name})        
        if d.userprofileenterprise_set.count() > 0:
            raise Exception(("Empresa <b>%(name)s</b> tiene usuarios y grupos asignados.") % {"name":d.name})
        # agregue aquí sus otras relgas de negocio
        d.delete()
        if not d.id:
            Message.info(request, ("Empresa <b>%(name)s</b> ha sido eliminado correctamente.") % {"name":d.name}, True)
            return Redirect.to_action(request, "index")
    except Exception, e:
        transaction.savepoint_rollback(sid)
        Message.error(request, e)
        return Redirect.to_action(request, "index")
# endregion enterprise

# region association OK
@csrf_exempt
def association_upload(request):
    """
    Sube logo
    """
    data = {}
    try:
        filename = Upload.save_file(request.FILES["logo"], "asociaciones/")
        data ["name"] = "%s" % filename
    except Exception, e:
        Message.error(request, e)
    return HttpResponse(json.dumps(data))

@transaction.atomic
@permission_resource_required
def association_edit_current(request):
    """
    Actualiza datos de la asociación a la que ingresó el usuario
    """
    d = Association()
    try:
        d = get_object_or_404(Association, id=DataAccessToken.get_association_id(request.session))
    except:
        Message.error(request, ("Asociación no seleccionada o no se encuentra en la base de datos."))
        return Redirect.to(request, "/home/choice_headquar/")

    if request.method == "POST":
        try:
            sid = transaction.savepoint()
            d.name = request.POST.get("name")
            d.type_a = request.POST.get("type_a")
            d.solution_id = request.POST.get("solution_id")
            # solution=Solution.objects.get(id=d.solution_id) #no es necesario
            d.logo = request.POST.get("asociacion_logo")
            if normalize("NFKD", u"%s" % d.name).encode("ascii", "ignore").lower() in list(
                normalize("NFKD", u"%s" % col["name"]).encode("ascii", "ignore").lower() for col in Association.objects.values("name").exclude(id=d.id)
                ):
                raise Exception(("Asociación <b>%(name)s</b> ya existe.") % {"name":d.name})

            # salvar registro
            d.save()
            raise Exception(("Asociación <b>%(name)s</b> ya existe.") % {"name":d.name})
            if d.id:
                Message.info(request, ("Asociación <b>%(name)s</b> ha sido actualizado correctamente.") % {"name":d.name})

        except Exception, e:
            transaction.savepoint_rollback(sid)
            Message.error(request, e)
    try:
        solution_list = Solution.objects.filter(is_active=True).order_by("id")
    except Exception, e:
        Message.error(request, e)
    c = {
        "page_module":("Cuenta"),
        "page_title":("Información de la asociación."),
        "d":d,
        "TYPES":Association.TYPES,
        "solution_list":solution_list,
        }
    return render_to_response("space/association/edit_current.html", c, context_instance=RequestContext(request))
# endregion association

# region solution OK
@permission_resource_required
def solution_index(request):
    """
    Página principal para trabajar con soluciones
    """
    try:
        solution_list = Solution.objects.all().order_by("-id")
    except Exception, e:
        Message.error(request, e)
    c = {
        "page_module":("Gestión de soluciones"),
        "page_title":("Listado de soluciones del sistema."),
        "solution_list":solution_list,
        }
    return render_to_response("space/solution/index.html", c, context_instance=RequestContext(request))

@permission_resource_required
def solution_add(request):
    """
    Agrega solución
    """
    d = Solution()
    d.description = ""
    if request.method == "POST":
        try:
            d.name = request.POST.get("name")
            d.description = request.POST.get("description")
            if Solution.objects.exclude(id=d.id).filter(name=d.name).count() > 0:
                raise Exception(("Solución <b>%(name)s</b> ya existe.") % {"name":d.name})
            d.save()
            if d.id:
                Message.info(request, ("Solución <b>%(name)s</b> ha sido registrado correctamente.") % {"name":d.name})
                return Redirect.to_action(request, "index")
        except Exception, e:
            Message.error(request, e)
    c = {
        "page_module":("Gestión de soluciones"),
        "page_title":("Agregar solución."),
        "d":d,
        }
    return render_to_response("space/solution/add.html", c, context_instance=RequestContext(request))

@permission_resource_required
def solution_edit(request, key):
    """
    Actualiza solución
    """
    id = SecurityKey.is_valid_key(request, key, "solution_upd")
    if not id:
        return Redirect.to_action(request, "index")
    d = None

    try:
        d = get_object_or_404(Solution, id=id)
    except:
        Message.error(request, ("Solución no se encuentra en la base de datos."))
        return Redirect.to_action(request, "index")

    if request.method == "POST":
        try:
            d.name = request.POST.get("name")
            d.description = request.POST.get("description")
            if Solution.objects.exclude(id=d.id).filter(name=d.name).count() > 0:
                raise Exception(("Solución <b>%(name)s</b> ya existe.") % {"name":d.name})

            # salvar registro
            d.save()
            if d.id:
                Message.info(request, ("Solución <b>%(name)s</b> ha sido actualizado correctamente.") % {"name":d.name})
                return Redirect.to_action(request, "index")

        except Exception, e:
            Message.error(request, e)
    c = {
        "page_module":("Gestión de soluciones"),
        "page_title":("Actualizar solución."),
        "d":d,
        }
    return render_to_response("space/solution/edit.html", c, context_instance=RequestContext(request))

@permission_resource_required
def solution_state(request, state, key):
    """
    Inactiva y reactiva el estado del la solución/plan
    """
    id = SecurityKey.is_valid_key(request, key, "solution_%s" % state)
    if not id:
        return Redirect.to_action(request, "index")
    try:
        d = get_object_or_404(Solution, id=id)
    except:
        Message.error(request, ("Solución no se encuentra en la base de datos."))
        return Redirect.to_action(request, "index")
    try:
        if state == "inactivar" and d.is_active == False:
            Message.error(request, ("La solución ya se encuentra inactivo."))
        else:
            if state == "reactivar" and d.is_active == True:
                Message.error(request, ("La solución ya se encuentra activo."))
            else:
                d.is_active = (True if state == "reactivar" else False)
                d.save()
                if d.id:
                    if d.is_active:
                        Message.info(request, ("Solución <b>%(name)s</b> ha sido reactivado correctamente.") % {"name":d.name}, True)
                    else:
                        Message.info(request, ("Solución <b>%(name)s</b> ha sido inactivado correctamente.") % {"name":d.name}, True)
                    return Redirect.to_action(request, "index")
    except Exception, e:
        Message.error(request, e)
        return Redirect.to_action(request, "index")

@permission_resource_required
def solution_delete(request, key):
    """
    Elimina solución
    """
    id = SecurityKey.is_valid_key(request, key, "solution_del")
    if not id:
        return Redirect.to_action(request, "index")
    try:
        d = get_object_or_404(Solution, id=id)
    except:
        Message.error(request, ("Solución no se encuentra en la base de datos."))
        return Redirect.to_action(request, "index")
    try:
        # rastreando dependencias
        if d.module_set.count() > 0:
            raise Exception(("Solución <b>%(name)s</b> tiene módulos asignados.") % {"name":d.name})
        if d.association_set.count() > 0:
            raise Exception(("Solución <b>%(name)s</b> está asignado en asociaciones.") % {"name":d.name})
        if d.enterprise_set.count() > 0:
            raise Exception(("Solución <b>%(name)s</b> está asignado en empresas.") % {"name":d.name})
        d.delete()
        if not d.id:
            Message.info(request, ("Solución <b>%(name)s</b> ha sido eliminado correctamente.") % {"name":d.name}, True)
            return Redirect.to_action(request, "index")
    except Exception, e:
        Message.error(request, e)
        return Redirect.to_action(request, "index")
# endregion solution