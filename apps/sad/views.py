# _*_ coding: utf-8 _*_
"""
@copyright   Copyright (c) 2014 Submit Consulting
@author      Angel Sullon (@asullom)
@package     sad

Descripcion: Implementacion de los controladores de la app sad
"""
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template.context import RequestContext
import json
# from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse

# from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.contrib.auth.decorators import login_required
from django.db import transaction

from unicodedata import normalize
from apps.utils.messages import Message
from apps.utils.logs import Logger
from apps.params.models import Person
from django.contrib.auth.models import User, Group, Permission 
from django.contrib.contenttypes.models import ContentType
from apps.space.models import Headquar
from apps.sad.models import Profile, Module, Menu, UserProfileAssociation, UserProfileEnterprise, UserProfileHeadquar
from apps.space.models import Solution
from django.db.models import Q
from apps.utils.upload import Upload
from apps.utils.decorators import permission_resource_required
from apps.utils.security import SecurityKey, DataAccessToken, Redirect
import datetime
from django.utils import timezone

import os
from django.conf import settings
from django.utils.encoding import force_text, force_unicode
import codecs
from apps.sad.models import Access

# region system OK.
@permission_resource_required
def system_index(request):
    """
    Lista paginada de system
    """
    
    backup_page = None
    
    c = {
        "page_module":("system"),
        "page_title":("system. TODO:: Deberá actualizar las variables de configuración del proyecto : settings.py ...Esperamos tu ayuda"),
        "day":'America/Lima',
        
        }

    return render_to_response("sad/system/index.html", c, context_instance=RequestContext(request))

# endregion system

# region maintenance OK.
@permission_resource_required
def maintenance_index(request):
    """
    Lista paginada de maintenance
    """
    
    backup_page = None
    
    c = {
        "page_module":("maintenance"),
        "page_title":("maintenance list. TODO:: Deberá permitir OPTIMIZAR, defragmentar, vaciar cache y reparar cada una de las tablas ...Esperamos tu ayuda"),
        
        "backup_page":backup_page,
        }

    return render_to_response("sad/maintenance/index.html", c, context_instance=RequestContext(request))

# endregion maintenance

# region backup OK.
@permission_resource_required
def backup_index(request):
    """
    Lista paginada de backup
    """
    
    backup_page = None
    
    c = {
        "page_module":("backup"),
        "page_title":("backup list. TODO:: Deberá permitir crear el busckup de la base de datos actual, restaurar y descargar ...Esperamos tu ayuda"),
        
        "backup_page":backup_page,
        }

    return render_to_response("sad/backup/index.html", c, context_instance=RequestContext(request))

# endregion backup

# region log OK.
@permission_resource_required
def log_index(request):
    """
    Página principal de log
    """
    day=datetime.datetime.now().strftime("%Y-%m-%d")
    if request.method == "POST":
        try:
            # Aquí asignar los datos
            day = request.POST.get("day")
            if request.POST.get("day"):
                
                #return Redirect.to_action(request, "list")
                if request.is_ajax():
                    request.path = "/sad/log/list/%s/" % (day)  # /app/controller_path/action/$params
                    return log_list(request, day)
                else:                        
                    return redirect("/sad/log/list/%s/" % (day))
        except Exception, e:
            Message.error(request, e)
    c = {
        "page_module":("Logs del sistema"),
        "page_title":("Sucesos."),
        "day":day,
        }
    return render_to_response("sad/log/index.html", c, context_instance=RequestContext(request))

@permission_resource_required
def log_list(request, day):
    """
    Listado de log del dia day
    """
    
    filedebug = 'temp/logs/log%s.txt' % (day)
    LOG_FILE = os.path.join(settings.BASE_DIR, filedebug)
    
    audit_page = None
    try:
        list = []
        audit=None
        try:
            audit = open( LOG_FILE, 'r' )
        except (OSError, IOError) as e:
            Message.error(request, "%s no se encuentra" % filedebug)
            pass
        if audit:
            try:
                audit=codecs.EncodedFile(audit,"utf-8")
                for row in reversed(audit.readlines()):
                    #print row
                    data = row.strip('\xef\xbb\xbf').split(']')
                    type=data[1].strip('[')
                    type_d=""
                    
                    if type is 'ERROR' or type is 'ALERT':
                        type_d ='<span class="label label-important">%s</span>' % type
                    elif type == 'WARNING' or type == 'CRITICAL' or type == 'EMERGENCE':
                        type_d ='<span class="label label-warning">%s</span>' % type
                    elif type == 'NOTICE' or type == 'INFO':
                        type_d ='<span class="label label-info">%s</span>' % type
                    else:
                        type_d ='<span class="label">%s</span>' % type
                                    
                    list.append({
                        "date": data[0].strip('['),
                        "type": type_d,
                        "mod": data[2].strip('['),
                        "route": data[3].strip('['),
                        "user": data[4].strip('['),
                        "ip": data[5].strip('['),
                        "desc": data[6].strip('['),
                        })
            except :
                Message.error(request, force_text("<b>%(name)s</b> posiblemente fué modificado manualmente") % {"name":audit.name})
                list = []
                auditx = open( LOG_FILE, 'r' )
                auditx=codecs.EncodedFile(auditx,"utf-8",'latin-1')
                #raise Exception("El usuario manipulo el archivo " )
                #audit = codecs.open(LOG_FILE, 'r', encoding = 'utf-8') 
                #print audit.readlines() .strip('\xef\xbb\xbf')
                for rowx in reversed(auditx.readlines()):
                    #print rowx
                    datax = rowx.strip('\xef\xbb\xbf').split(']')
                    type=datax[1].strip('[')
                    type_d=""
                    
                    if type is 'ERROR' or type is 'ALERT':
                        type_d ='<span class="label label-important">%s</span>' % type
                    elif type == 'WARNING' or type == 'CRITICAL' or type == 'EMERGENCE':
                        type_d ='<span class="label label-warning">%s</span>' % type
                    elif type == 'NOTICE' or type == 'INFO':
                        type_d ='<span class="label label-info">%s</span>' % type
                    else:
                        type_d ='<span class="label">%s</span>' % type
                                    
                    list.append({
                        "date": datax[0].strip('['),
                        "type": type_d,
                        "mod": datax[2].strip('['),
                        "route": datax[3].strip('['),
                        "user": datax[4].strip('['),
                        "ip": datax[5].strip('['),
                        "desc": datax[6].strip('['),
                        })
                Message.error(request, force_text("<b>%(name)s</b> fué recuperado") % {"name":audit.name})
                       
        if audit:    
            audit.close()
        
        paginator = Paginator(list, 25)  # Show num_rows=25 contacts per page
        try:
            audit_page = paginator.page(request.GET.get("page"))
        except PageNotAnInteger:
            audit_page = paginator.page(1)
        except EmptyPage:
            audit_page = paginator.page(paginator.num_pages)
    except Exception, e:
        Message.error(request, e)
    c = {
        "page_module":("Logs del sistema"),
        "page_title":force_text("Sucesos del día %(day)s. ") % {"day":day},
        "audit_page": audit_page,
        "day":day.replace("/", "-"),
        }
    return render_to_response("sad/log/list.html", c, context_instance=RequestContext(request))


# endregion log


# region auditoria OK.
@permission_resource_required
def audit_index(request):
    """
    Página principal para audit
    """
    day=datetime.datetime.now().strftime("%Y-%m-%d")
    if request.method == "POST":
        try:
            # Aquí asignar los datos
            day = request.POST.get("day")
            if request.POST.get("day"):
                
                #return Redirect.to_action(request, "list")
                if request.is_ajax():
                    request.path = "/sad/audit/list/%s/" % (day)  # /app/controller_path/action/$params
                    return audit_list(request, day)
                else:                        
                    return redirect("/sad/audit/list/%s/" % (day))
        except Exception, e:
            Message.error(request, e)
    c = {
        "page_module":("Listado de acciones de los usuarios"),
        "page_title":("Auditoría y seguimientos."),
        "day":day,
        }
    return render_to_response("sad/audit/index.html", c, context_instance=RequestContext(request))

@permission_resource_required
def audit_list(request, day):
    """
    Página principal para audit
    """
    
    filedebug = 'temp/logs/audit%s.txt' % (day)
    LOG_FILE = os.path.join(settings.BASE_DIR, filedebug)
    
    audit_page = None
    try:
        list = []
        audit=None
        try:
            audit = open( LOG_FILE, 'r' )
        except (OSError, IOError) as e:
            Message.error(request, "%s no se encuentra" % filedebug)
            pass
        if audit:
            try:
                audit=codecs.EncodedFile(audit,"utf-8")
                for row in reversed(audit.readlines()):
                    #print row
                    data = row.strip('\xef\xbb\xbf').split(']')
                    type=data[1].strip('[')
                    type_d=""
                    
                    if type is 'ERROR' or type is 'ALERT':
                        type_d ='<span class="label label-important">%s</span>' % type
                    elif type == 'WARNING' or type == 'CRITICAL' or type == 'EMERGENCE':
                        type_d ='<span class="label label-warning">%s</span>' % type
                    elif type == 'NOTICE' or type == 'INFO':
                        type_d ='<span class="label label-info">%s</span>' % type
                    else:
                        type_d ='<span class="label">%s</span>' % type
                                    
                    list.append({
                        "date": data[0].strip('['),
                        "type": type_d,
                        "mod": data[2].strip('['),
                        "route": data[3].strip('['),
                        "user": data[4].strip('['),
                        "ip": data[5].strip('['),
                        "desc": data[6].strip('['),
                        })
            except :
                Message.error(request, force_text("<b>%(name)s</b> posiblemente fué modificado manualmente") % {"name":audit.name})
                list = []
                auditx = open( LOG_FILE, 'r' )
                auditx=codecs.EncodedFile(auditx,"utf-8",'latin-1')
                #raise Exception("El usuario manipulo el archivo " )
                #audit = codecs.open(LOG_FILE, 'r', encoding = 'utf-8') 
                #print audit.readlines() .strip('\xef\xbb\xbf')
                for rowx in reversed(auditx.readlines()):
                    #print rowx
                    datax = rowx.strip('\xef\xbb\xbf').split(']')
                    type=datax[1].strip('[')
                    type_d=""
                    
                    if type is 'ERROR' or type is 'ALERT':
                        type_d ='<span class="label label-important">%s</span>' % type
                    elif type == 'WARNING' or type == 'CRITICAL' or type == 'EMERGENCE':
                        type_d ='<span class="label label-warning">%s</span>' % type
                    elif type == 'NOTICE' or type == 'INFO':
                        type_d ='<span class="label label-info">%s</span>' % type
                    else:
                        type_d ='<span class="label">%s</span>' % type
                                    
                    list.append({
                        "date": datax[0].strip('['),
                        "type": type_d,
                        "mod": datax[2].strip('['),
                        "route": datax[3].strip('['),
                        "user": datax[4].strip('['),
                        "ip": datax[5].strip('['),
                        "desc": datax[6].strip('['),
                        })
                Message.error(request, force_text("<b>%(name)s</b> fué recuperado") % {"name":audit.name})
                       
        if audit:    
            audit.close()
        
        paginator = Paginator(list, 25)  # Show num_rows=25 contacts per page
        try:
            audit_page = paginator.page(request.GET.get("page"))
        except PageNotAnInteger:
            audit_page = paginator.page(1)
        except EmptyPage:
            audit_page = paginator.page(paginator.num_pages)
    except Exception, e:
        Message.error(request, e)
    c = {
        "page_module":("Auditorías del sistema"),
        "page_title":force_text("Auditoría y seguimientos del día %(day)s. ") % {"day":day},
        "audit_page": audit_page,
        "day":day.replace("/", "-"),
        }
    return render_to_response("sad/audit/list.html", c, context_instance=RequestContext(request))


# endregion auditoria



#region Accesos ok

@permission_resource_required
def access_index(request, field="user__profile__person__first_name", value="None", order="-id"):
    """
    Lista paginada de Access
    """
        
    field = (field if not request.REQUEST.get("field") else request.REQUEST.get("field")).strip()
    value = (value if not request.REQUEST.get("value") else request.REQUEST.get("value")).strip()
    order = (order if not request.REQUEST.get("order") else request.REQUEST.get("order")).strip()
    #print request.session['_auth_user_id']
        
    access_page = None
    try:
        value_f = "" if value == "None" else value  # (true or false) ? value1:value2
        column_contains = u"%s__%s" % (field, "contains")  # SEL-- WHERE name LIKE %an%

        if field == "is_active":
            value_f = "0" if value.lower() == "no" else value
            column_contains = u"%s" % (field) #.filter(is_active=True)
            
        access_list = Access.objects.filter(**{ column_contains: value_f }).order_by(order)
        paginator = Paginator(access_list, 25)  # Show num_rows=25 contacts per page
        try:
            access_page = paginator.page(request.GET.get("page"))
        except PageNotAnInteger:
            access_page = paginator.page(1)
        except EmptyPage:
            access_page = paginator.page(paginator.num_pages)
    except Exception, e:
        Message.error(request, e)
    c = {
        "page_module":("Access"),
        "page_title":("Access list."),
        
        "access_page":access_page,
        "field":field,
        "value":value.replace("/", "-"),
        "order":order,
        }

    return render_to_response("sad/access/index.html", c, context_instance=RequestContext(request))
#endregion accesos
# region user OK.

@login_required(login_url="/accounts/login/")
@permission_resource_required
def user_index(request, field="username", value="None", order="-id"):
    """
    Página principal para trabajar con usuarios
    """
    try:
        d = get_object_or_404(Headquar, id=DataAccessToken.get_headquar_id(request.session))
    except:
        Message.error(request, ("Sede no seleccionado o no se encuentra en la base de datos."))
        return Redirect.to(request, "/home/choice_headquar/")
    field = (field if not request.REQUEST.get("field") else request.REQUEST.get("field")).strip()
    value = (value if not request.REQUEST.get("value") else request.REQUEST.get("value")).strip()
    order = (order if not request.REQUEST.get("order") else request.REQUEST.get("order")).strip()
    try:
        value_f = "" if value == "None" else value
        column_contains = u"%s__%s" % (field, "contains")
        user_list = User.objects.filter(**{ column_contains: value_f }).order_by("pos").order_by(order)
        paginator = Paginator(user_list, 125)
        try:
            user_page = paginator.page(request.GET.get("page"))
        except PageNotAnInteger:
            user_page = paginator.page(1)
        except EmptyPage:
            user_page = paginator.page(paginator.num_pages)
    except Exception, e:
        Message.error(request, e)
    c = {
        "page_module":("Gestión de usuarios"),
        "page_title":("Listado de usuarios del sistema."),
        "user_page":user_page,
        "field":field,
        "value":value.replace("/", "-"),
        "order":order,
        }
    return render_to_response("sad/user/index.html", c, context_instance=RequestContext(request))

def user_upload(request):
    """
    Sube fotografia
    """
    data = {}
    try:
        filename = Upload.save_file(request.FILES["fotografia"], "personas/")
        data ["name"] = "%s" % filename
    except Exception, e:
        Message.error(request, e)
    return HttpResponse(json.dumps(data))
    
@permission_resource_required
@transaction.atomic
def user_add(request):
    """
    Agrega usuario
    """
    d = User()
    d.photo = "personas/default.png"
    if request.method == "POST":
        try:
            sid = transaction.savepoint()
            headquar = Headquar.objects.get(id=DataAccessToken.get_headquar_id(request.session))

            d.username = request.POST.get("login")
            d.email = request.POST.get("email")
            
            d.first_name = request.POST.get("first_name")
            d.last_name = request.POST.get("last_name")
            d.photo = request.POST.get("persona_fotografia")
            d.identity_type = request.POST.get("identity_type")
            d.identity_num = request.POST.get("identity_num")
            identity_type_display = dict((x, y) for x, y in Person.IDENTITY_TYPES)[d.identity_type]

            
            if User.objects.filter(username=d.username).count() > 0:
                raise Exception("El usuario <b>%s</b> ya existe " % d.username)
            if User.objects.filter(email=d.email).count() > 0:
                raise Exception("El email <b>%s</b> ya existe " % d.email)
            user = User.objects.create_user(username=d.username, email=d.email, password=request.POST.get("password"))

            if normalize("NFKD", u"%s %s" % (d.first_name, d.last_name)).encode("ascii", "ignore").lower() in list(
                normalize("NFKD", u"%s %s" % (col["first_name"], col["last_name"])).encode("ascii", "ignore").lower() for col in Person.objects.values("first_name", "last_name").filter(identity_type=d.identity_type, identity_num=d.identity_num)
                ):
                raise Exception("La persona <b>%s %s</b> con %s:<b>%s</b> ya existe " % (d.first_name, d.last_name, identity_type_display, d.identity_num))
            if Person.objects.filter(identity_type=d.identity_type, identity_num=d.identity_num).count() > 0:
                raise Exception("La persona con %s:<b>%s</b> ya existe " % (identity_type_display, d.identity_num))
            person = Person(first_name=d.first_name, last_name=d.last_name, identity_type=d.identity_type, identity_num=d.identity_num, photo=d.photo)
            person.save()

            profile = Profile(user=user)
            profile.person = person
            profile.save()

            d = user

            # agregando en UserProfileHeadquar
            groups_sede = request.POST.getlist("groups_sede")
            groups_sede = list(set(groups_sede))
            for value in groups_sede:
                group = Group.objects.get(id=value)
                # d.groups.add(group)
                user_profile_headquar = UserProfileHeadquar()
                user_profile_headquar.user = d
                user_profile_headquar.headquar = headquar
                user_profile_headquar.group = group
                user_profile_headquar.save()

            # agregando en UserProfileEnterprise
            groups_enterprise = request.POST.getlist("groups_enterprise")
            groups_enterprise = list(set(groups_enterprise))
            for value in groups_enterprise:
                group = Group.objects.get(id=value)
                # d.groups.add(group)
                user_profile_enterprise = UserProfileEnterprise()
                user_profile_enterprise.user = d
                user_profile_enterprise.enterprise = headquar.enterprise
                user_profile_enterprise.group = group
                user_profile_enterprise.save()

            # agregando en UserProfileAssociation
            groups_association = request.POST.getlist("groups_association")
            groups_association = list(set(groups_association))
            for value in groups_association:
                group = Group.objects.get(id=value)
                # d.groups.add(group)
                user_profile_association = UserProfileAssociation()
                user_profile_association.user = d
                user_profile_association.association = headquar.association
                user_profile_association.group = group
                user_profile_association.save()

            # agregando en user_groups
            group_dist_list = list(set(groups_sede + groups_enterprise + groups_association))
            for value in group_dist_list:
                group = Group.objects.get(id=value)
                d.groups.add(group)

            if d.id:
                Message.info(request, ("Usuario <b>%(name)s</b> ha sido registrado correctamente.") % {"name":d.username}, True)
                return Redirect.to_action(request, "index")
        except Exception, e:
            transaction.savepoint_rollback(sid)
            Message.error(request, e)
    try:
        headquar = Headquar.objects.get(id=DataAccessToken.get_headquar_id(request.session))

        solution_enterprise = Solution.objects.get(id=headquar.enterprise.solution.id)
        solution_association = Solution.objects.get(id=headquar.association.solution.id)
        module_list = Module.objects.filter(Q(solutions=solution_enterprise) | Q(solutions=solution_association), is_active=True).distinct()
        group_perm_list = Group.objects.filter(module_set__in=module_list).order_by("-id").distinct()  # trae los objetos relacionados sad.Module
        # print group_perm_list
        # print "====================="
        # pero hay que adornarlo de la forma Module>Group/perfil
        group_list_by_module = []
        group_list_by_module_unique_temp = []  # solo para verificar que el Group no se repita si este está en dos o más módulos
        for module in module_list:
            for group in Group.objects.filter(module_set=module).distinct():
                if len(group_list_by_module) == 0:
                    group_list_by_module.append({
                    "group": group,
                    "module": module,
                    })
                    group_list_by_module_unique_temp.append(group)
                else:
                    if group not in group_list_by_module_unique_temp:
                        group_list_by_module.append({
                        "group": group,
                        "module": module,
                        })
                        group_list_by_module_unique_temp.append(group)
        # print group_list_by_module_unique_temp
    except Exception, e:
        Message.error(request, e)
    c = {
        "page_module":("Gestión de usuarios"),
        "page_title":("Agregar usuario."),
        "d":d,
        "group_perm_list":group_list_by_module,
        "IDENTITY_TYPES":Person.IDENTITY_TYPES,
        }
    return render_to_response("sad/user/add.html", c, context_instance=RequestContext(request))

@permission_resource_required
@transaction.atomic
def user_edit(request, key):
    """
    Actualiza user
    """
    id = SecurityKey.is_valid_key(request, key, "user_upd")
    if not id:
        return Redirect.to_action(request, "index")
    d = None
    try:
        d = get_object_or_404(User, id=id)
        try:
            profile = Profile.objects.get(user=d.id)
            if profile.id:
                d.first_name = d.profile.person.first_name
                d.last_name = d.profile.person.last_name
                d.photo = d.profile.person.photo
                d.identity_type = d.profile.person.identity_type
                d.identity_num = d.profile.person.identity_num
        except:
            pass
        headquar = Headquar.objects.get(id=DataAccessToken.get_headquar_id(request.session))

        # los permisos del usuario según su espacio        
        group_id_list_by_user_and_headquar = list(col["id"] for col in Group.objects.values("id").filter(userprofileheadquar__headquar__id=headquar.id, userprofileheadquar__user__id=d.id).distinct())
        group_id_list_by_user_and_enterprise = list(col["id"] for col in Group.objects.values("id").filter(userprofileenterprise__enterprise__id=headquar.enterprise.id, userprofileenterprise__user__id=d.id).distinct())
        group_id_list_by_user_and_association = list(col["id"] for col in Group.objects.values("id").filter(userprofileassociation__association__id=headquar.association.id, userprofileassociation__user__id=d.id).distinct())

    except Exception, e:
        Message.error(request, ("Usuario no se encuentra en la base de datos. %s" % e))
        return Redirect.to_action(request, "index")

    if request.method == "POST":
        try:
            sid = transaction.savepoint()
            d.username = request.POST.get("login")
            
            if User.objects.exclude(id=d.id).filter(username=d.username).count() > 0:
                raise Exception("El usuario <b>%s</b> ya existe " % d.username)

            if request.POST.get("email"):
                d.email = request.POST.get("email")
                if User.objects.exclude(id=d.id).filter(email=d.email).count() > 0:
                    raise Exception("El email <b>%s</b> ya existe " % d.email)
            if request.POST.get("password"):
                d.set_password(request.POST.get("password"))
            d.save()

            try:
                person = Person.objects.get(profile=d.profile)
            except:
                person = Person()
                person.save()
                pass

            try:
                profile = Profile.objects.get(user=d)
            except:
                profile = Profile(user=d)
                profile.person = person
                profile.save()
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

            # Elimino los antiguos privilegios
            group_id_list_by_user_and_hea = list(set(group_id_list_by_user_and_headquar + group_id_list_by_user_and_enterprise + group_id_list_by_user_and_association))
            
            for group_id in group_id_list_by_user_and_headquar:
                group = Group.objects.get(id=group_id)
                user_profile_headquar = UserProfileHeadquar.objects.get(user_id=d.id, group_id=group_id, headquar_id=headquar.id)
                user_profile_headquar.delete()

            for group_id in group_id_list_by_user_and_enterprise:
                group = Group.objects.get(id=group_id)
                user_profile_enterprise = UserProfileEnterprise.objects.get(user_id=d.id, group_id=group_id, enterprise_id=headquar.enterprise.id)
                user_profile_enterprise.delete()

            for group_id in group_id_list_by_user_and_association:
                group = Group.objects.get(id=group_id)
                user_profile_association = UserProfileAssociation.objects.get(user_id=d.id, group_id=group_id, association_id=headquar.association.id)
                user_profile_association.delete()

            for group_id in  group_id_list_by_user_and_hea:
                group = Group.objects.get(id=group_id)
                d.groups.remove(group)

            # agregando en UserProfileHeadquar
            groups_sede = request.POST.getlist("groups_sede")
            groups_sede = list(set(groups_sede))
            for value in groups_sede:
                group = Group.objects.get(id=value)
                # d.groups.add(group)
                user_profile_headquar = UserProfileHeadquar()
                user_profile_headquar.user = d
                user_profile_headquar.headquar = headquar
                user_profile_headquar.group = group
                user_profile_headquar.save()

            # agregando en UserProfileEnterprise
            groups_enterprise = request.POST.getlist("groups_enterprise")
            groups_enterprise = list(set(groups_enterprise))
            for value in groups_enterprise:
                group = Group.objects.get(id=value)
                # d.groups.add(group)
                user_profile_enterprise = UserProfileEnterprise()
                user_profile_enterprise.user = d
                user_profile_enterprise.enterprise = headquar.enterprise
                user_profile_enterprise.group = group
                user_profile_enterprise.save()

            # agregando en UserProfileAssociation
            groups_association = request.POST.getlist("groups_association")
            groups_association = list(set(groups_association))
            for value in groups_association:
                group = Group.objects.get(id=value)
                # d.groups.add(group)
                user_profile_association = UserProfileAssociation()
                user_profile_association.user = d
                user_profile_association.association = headquar.association
                user_profile_association.group = group
                user_profile_association.save()

            # agregando en user_groups
            group_dist_list = list(set(groups_sede + groups_enterprise + groups_association))
            for value in group_dist_list:
                group = Group.objects.get(id=value)
                d.groups.add(group)

            if d.id:
                Message.info(request, ("Usuario <b>%(name)s</b> ha sido actualizado correctamente.") % {"name":d.username}, True)
                return Redirect.to_action(request, "index")

        except Exception, e:
            transaction.savepoint_rollback(sid)
            Message.error(request, e)
    try:
        solution_enterprise = Solution.objects.get(id=headquar.enterprise.solution.id)
        solution_association = Solution.objects.get(id=headquar.association.solution.id)
        module_list = Module.objects.filter(Q(solutions=solution_enterprise) | Q(solutions=solution_association), is_active=True).distinct()
        group_perm_list = Group.objects.filter(module_set__in=module_list).order_by("-id").distinct()  # trae los objetos relacionados a sad.Module
        # print group_perm_list
        # print "=====================x"
        # pero hay que adornarlo de la forma Module>Group
        group_list_by_module = []
        group_list_by_module_unique_temp = []  # solo para verificar que el Group no se repita si este está en dos o más módulos
        for module in module_list:
            for group in Group.objects.filter(module_set=module).distinct():
                if len(group_list_by_module) == 0:
                    group_list_by_module.append({
                    "group": group,
                    "module": module,
                    })
                    group_list_by_module_unique_temp.append(group)
                else:
                    if group not in group_list_by_module_unique_temp:
                        group_list_by_module.append({
                        "group": group,
                        "module": module,
                        })
                        group_list_by_module_unique_temp.append(group)
        # print group_list_by_module_unique_temp
    except Exception, e:
        Message.error(request, e)
    c = {
        "page_module":("Gestión de usuarios"),
        "page_title":("Actualizar usuario."),
        "d":d,
        "group_perm_list":group_list_by_module,
        "group_id_list_by_user_and_headquar":group_id_list_by_user_and_headquar,
        "group_id_list_by_user_and_enterprise":group_id_list_by_user_and_enterprise,
        "group_id_list_by_user_and_association":group_id_list_by_user_and_association,
        "IDENTITY_TYPES":Person.IDENTITY_TYPES,
        }
    return render_to_response("sad/user/edit.html", c, context_instance=RequestContext(request))

def user_view(request, key):
    """
    Visualiza información del usuario
    """
    id = SecurityKey.is_valid_key(request, key, "user_viw")
    if not id:
        return Redirect.to_action(request, "index")
    d = None
    try:
        d = get_object_or_404(User, id=id)
        try:
            profile = Profile.objects.get(user=d.id)
            if profile.id:
                d.first_name = d.profile.person.first_name
                d.last_name = d.profile.person.last_name
                d.photo = d.profile.person.photo
                d.identity_type = d.profile.person.identity_type
                d.identity_num = d.profile.person.identity_num
        except:
            pass
    except Exception, e:
        Message.error(request, ("Usuario no se encuentra en la base de datos. %s" % e))
        return Redirect.to_action(request, "index")

    try:
        headquar = Headquar.objects.get(id=DataAccessToken.get_headquar_id(request.session))
        headquar_list_by_user_profile_headquar = Headquar.objects.filter(id__in=UserProfileHeadquar.objects.values("headquar_id").filter(user=d).distinct())

        user_profile_headquar_list = UserProfileHeadquar.objects.filter(user=d).order_by("headquar")
        user_profile_enterprise_list = UserProfileEnterprise.objects.filter(user=d).order_by("enterprise")
        user_profile_association_list = UserProfileAssociation.objects.filter(user=d).order_by("association")

        solution_enterprise = Solution.objects.get(id=headquar.enterprise.solution.id)
        solution_association = Solution.objects.get(id=headquar.association.solution.id)
        module_list = Module.objects.filter(Q(solutions=solution_enterprise) | Q(solutions=solution_association)).distinct()
        group_perm_list = Group.objects.filter(module_set__in=module_list).order_by("-id").distinct()  # trae los objetos relacionados sad.Module
        # print group_perm_list
        # print "=====================x"
        # pero hay que adornarlo de la forma Module>Group/perfil
        group_list_by_module = []
        group_list_by_module_unique_temp = []  # solo para verificar que el Group no se repita si este está en dos o más módulos
        for module in module_list:
            for group in Group.objects.filter(module_set=module).distinct():
                if len(group_list_by_module) == 0:
                    group_list_by_module.append({
                    "group": group,
                    "module": module,
                    })
                    group_list_by_module_unique_temp.append(group)
                else:
                    if group not in group_list_by_module_unique_temp:
                        group_list_by_module.append({
                        "group": group,
                        "module": module,
                        })
                        group_list_by_module_unique_temp.append(group)
        # print group_list_by_module_unique_temp
    except Exception, e:
        Message.error(request, e)
    c = {
        "page_module":("Gestión de usuarios"),
        "page_title":("Información del usuario."),
        "d":d,
        "user_profile_headquar_list":user_profile_headquar_list,
        "user_profile_enterprise_list":user_profile_enterprise_list,
        "user_profile_association_list":user_profile_association_list,
        "IDENTITY_TYPES":Person.IDENTITY_TYPES,
        }
    return render_to_response("sad/user/view.html", c, context_instance=RequestContext(request))

@permission_resource_required
def user_state(request, state, key):
    """
    Inactiva y reactiva el estado del usuario
    """
    id = SecurityKey.is_valid_key(request, key, "user_%s" % state)
    if not id:
        return Redirect.to_action(request, "index")
    try:
        d = get_object_or_404(User, id=id)
    except:
        Message.error(request, ("Usuario no se encuentra en la base de datos."))
        return Redirect.to_action(request, "index")

    if d.username == "admin":
        Message.warning(request, ("Lo sentimos, pero este usuario no se puede inactivar."))
        return Redirect.to_action(request, "index")

    try:
        if state == "inactivar" and d.is_active == False:
            Message.error(request, ("El usuario ya se encuentra inactivo."))
        else:
            if state == "reactivar" and d.is_active == True:
                Message.error(request, ("El usuario ya se encuentra activo."))
            else:
                d.is_active = (True if state == "reactivar" else False)
                d.save()
                if d.id:
                    if d.is_active:
                        Message.info(request, ("Usuario <b>%(username)s</b> ha sido reactivado correctamente.") % {"username":d.username}, True)
                    else:
                        Message.info(request, ("Usuario <b>%(username)s</b> ha sido inactivado correctamente.") % {"username":d.username}, True)
                    return Redirect.to_action(request, "index")
    except Exception, e:
        Message.error(request, e)
        return Redirect.to_action(request, "index")

@permission_resource_required
@transaction.atomic
def user_delete(request, key):
    """
    Elimina usuario
    """
    id = SecurityKey.is_valid_key(request, key, "user_del")
    if not id:
        return Redirect.to_action(request, "index")
    try:
        d = get_object_or_404(User, id=id)
    except:
        Message.error(request, ("Usuario no se encuentra en la base de datos."))
        return Redirect.to_action(request, "index")
    if d.username == "admin":
        Message.warning(request, ("Lo sentimos, pero este usuario no se puede eliminar."))
        return Redirect.to_action(request, "index")
    try:
        # rastreando dependencias
        if d.groups.count() > 0:
            raise Exception(("Usuario <b>%(name)s</b> tiene permisos asignados.") % {"name":d.username})

        if d.userprofileheadquar_set.count() > 0:
            raise Exception(("Usuario <b>%(name)s</b> tiene permisos asignados en userprofileheadquar.") % {"name":d.username})
        if d.userprofileenterprise_set.count() > 0:
            raise Exception(("Usuario <b>%(name)s</b> tiene permisos asignados en userprofileenterprise.") % {"name":d.username})
        if d.userprofileassociation_set.count() > 0:
            raise Exception(("Usuario <b>%(name)s</b> tiene permisos asignados en userprofileassociation.") % {"name":d.username})
        
        d.delete()
        if not d.id:
            Message.info(request, ("Usuario <b>%(username)s</b> ha sido eliminado correctamente.") % {"username":d.username}, True)
            return Redirect.to_action(request, "index")
    except Exception, e:
        Message.error(request, e)
        return Redirect.to_action(request, "index")

@permission_resource_required
def user_person_search(request, field="first_name", value="None"):
    """
    Muestra el listado de Person 
    """
    field = (field if not request.REQUEST.get("field") else request.REQUEST.get("field")).strip()
    value = (value if not request.REQUEST.get("value") else request.REQUEST.get("value")).strip()

    value_f = "None" if value == "None" else value
    column_contains = u"%s__%s" % (field, "contains")
    
    profile_list = Profile.objects.filter()
    person_list = Person.objects.exclude(profile__in=profile_list).filter(**{ column_contains: value_f }).order_by("last_name", "first_name") #.distinct()  # Trae todo
    
    c = {
        "page_module":("Personas"),
        "page_title":("Resultado de personas que no tienen perfil o acceso al sistema."),
        "person_list": person_list,

        "field":field,
        "value":value.replace("/", "-"),
        }
    return render_to_response("sad/user/person_search.html", c, context_instance=RequestContext(request))

@permission_resource_required
@transaction.atomic
def user_add_from_person(request, key):
    """
    Agrega usuario desde person
    """
    id = SecurityKey.is_valid_key(request, key, "user_add_from_person")
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

            d.username = request.POST.get("login")
            d.email = request.POST.get("email")
            
            d.first_name = request.POST.get("first_name")
            d.last_name = request.POST.get("last_name")
            d.photo = request.POST.get("persona_fotografia")
            d.identity_type = request.POST.get("identity_type")
            d.identity_num = request.POST.get("identity_num")
            identity_type_display = dict((x, y) for x, y in Person.IDENTITY_TYPES)[d.identity_type]

            
            if User.objects.filter(username=d.username).count() > 0:
                raise Exception("El usuario <b>%s</b> ya existe " % d.username)
            if User.objects.filter(email=d.email).count() > 0:
                raise Exception("El email <b>%s</b> ya existe " % d.email)
            user = User.objects.create_user(username=d.username, email=d.email, password=request.POST.get("password"))
                        
            
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
            

            profile = Profile(user=user)
            profile.person = person
            profile.save()

            d = user

            # agregando en UserProfileHeadquar
            groups_sede = request.POST.getlist("groups_sede")
            groups_sede = list(set(groups_sede))
            for value in groups_sede:
                group = Group.objects.get(id=value)
                # d.groups.add(group)
                user_profile_headquar = UserProfileHeadquar()
                user_profile_headquar.user = d
                user_profile_headquar.headquar = headquar
                user_profile_headquar.group = group
                user_profile_headquar.save()

            # agregando en UserProfileEnterprise
            groups_enterprise = request.POST.getlist("groups_enterprise")
            groups_enterprise = list(set(groups_enterprise))
            for value in groups_enterprise:
                group = Group.objects.get(id=value)
                # d.groups.add(group)
                user_profile_enterprise = UserProfileEnterprise()
                user_profile_enterprise.user = d
                user_profile_enterprise.enterprise = headquar.enterprise
                user_profile_enterprise.group = group
                user_profile_enterprise.save()

            # agregando en UserProfileAssociation
            groups_association = request.POST.getlist("groups_association")
            groups_association = list(set(groups_association))
            for value in groups_association:
                group = Group.objects.get(id=value)
                # d.groups.add(group)
                user_profile_association = UserProfileAssociation()
                user_profile_association.user = d
                user_profile_association.association = headquar.association
                user_profile_association.group = group
                user_profile_association.save()

            # agregando en user_groups
            group_dist_list = list(set(groups_sede + groups_enterprise + groups_association))
            for value in group_dist_list:
                group = Group.objects.get(id=value)
                d.groups.add(group)

            if d.id:
                Message.info(request, ("Usuario <b>%(name)s</b> ha sido agregado desde persona correctamente.") % {"name":d.username}, True)
                return Redirect.to_action(request, "index")
        except Exception, e:
            transaction.savepoint_rollback(sid)
            Message.error(request, e)
    try:
        headquar = Headquar.objects.get(id=DataAccessToken.get_headquar_id(request.session))

        solution_enterprise = Solution.objects.get(id=headquar.enterprise.solution.id)
        solution_association = Solution.objects.get(id=headquar.association.solution.id)
        module_list = Module.objects.filter(Q(solutions=solution_enterprise) | Q(solutions=solution_association), is_active=True).distinct()
        group_perm_list = Group.objects.filter(module_set__in=module_list).order_by("-id").distinct()  # trae los objetos relacionados sad.Module
        # print group_perm_list
        # print "====================="
        # pero hay que adornarlo de la forma Module>Group/perfil
        group_list_by_module = []
        group_list_by_module_unique_temp = []  # solo para verificar que el Group no se repita si este está en dos o más módulos
        for module in module_list:
            for group in Group.objects.filter(module_set=module).distinct():
                if len(group_list_by_module) == 0:
                    group_list_by_module.append({
                    "group": group,
                    "module": module,
                    })
                    group_list_by_module_unique_temp.append(group)
                else:
                    if group not in group_list_by_module_unique_temp:
                        group_list_by_module.append({
                        "group": group,
                        "module": module,
                        })
                        group_list_by_module_unique_temp.append(group)
        # print group_list_by_module_unique_temp
    except Exception, e:
        Message.error(request, e)
    c = {
        "page_module":("Gestión de usuarios"),
        "page_title":("Agregar usuario de person ."),
        "d":d,
        "group_perm_list":group_list_by_module,
        "IDENTITY_TYPES":Person.IDENTITY_TYPES,
        }
    return render_to_response("sad/user/add_from_person.html", c, context_instance=RequestContext(request))


# endregion user





# region menu OK
# @csrf_exempt
@login_required#(login_url="/accounts/login/")
@permission_resource_required
def menu_index(request, field="title", value="None", order="pos"):
    """
    Página principal para trabajar con menús dinámicos
    """
    field = (field if not request.REQUEST.get("field") else request.REQUEST.get("field")).strip()
    value = (value if not request.REQUEST.get("value") else request.REQUEST.get("value")).strip()
    order = (order if not request.REQUEST.get("order") else request.REQUEST.get("order")).strip()

    menu_page = None
    try:
        value_f = "" if value == "None" else value
        column_contains = u"%s__%s" % (field, "contains")
        menu_list = Menu.objects.filter(**{ column_contains: value_f }).order_by("module", order)
        paginator = Paginator(menu_list, 125)
        try:
            menu_page = paginator.page(request.GET.get("page"))
        except PageNotAnInteger:
            menu_page = paginator.page(1)
        except EmptyPage:
            menu_page = paginator.page(paginator.num_pages)
    except Exception, e:
        Message.error(request, e)
    c = {
        "page_module":("Gestión de menús"),
        "page_title":("Listado de menús del sistema."),
        
        "menu_page":menu_page,
        # "MODULES":dict((x, y) for x, y in Module.MODULES),
        "field":field,
        "value":value.replace("/", "-"),
        "order":order,
        }
    return render_to_response("sad/menu/index.html", c, context_instance=RequestContext(request))

@permission_resource_required
def menu_add(request):
    d = Menu()
    if request.method == "POST":
        try:
            # Aquí asignar los datos
            d.title = request.POST.get("title")
            d.url = ("#" if not request.REQUEST.get("url") else request.REQUEST.get("url")).strip()
            d.icon = request.POST.get("icon")
            d.pos = request.POST.get("pos")
            d.module = request.POST.get("module")
            if request.POST.get("permission_id"):
                d.permission_id = Permission.objects.get(id=request.POST.get("permission_id")).id

            if request.POST.get("parent_id"):
                d.parent_id = Menu.objects.get(id=request.POST.get("parent_id")).id

            # if Menu.objects.exclude(id = d.id).filter(title = d.title).count() > 0:
            #     raise Exception( ("Menu <b>%(name)s</b> ya existe.") % {"name":d.title} )

            # salvar registro
            d.save()
            if d.id:
                Message.info(request, ("Menu <b>%(name)s</b> ha sido registrado correctamente.") % {"name":d.title}, True)
                return Redirect.to_action(request, "index")
        except Exception, e:
            Message.error(request, e)
    try:
        parent_list = Menu.objects.filter(parent_id=None, is_active=True)
        permission_list = Permission.objects.all()

    except Exception, e:
        Message.error(request, e)
    c = {
        "page_module":("Gestión de menús"),
        "page_title":("Agregar menú."),
        "d":d,
        "MODULES":Menu.MODULES,
        "parent_list":parent_list,
        "permission_list":permission_list,
        }
    return render_to_response("sad/menu/add.html", c, context_instance=RequestContext(request))

@permission_resource_required
def menu_edit(request, key):
    """
    Actualiza menú
    """
    id = SecurityKey.is_valid_key(request, key, "menu_upd")
    if not id:
        return Redirect.to_action(request, "index")
    d = None
    try:
        d = get_object_or_404(Menu, id=id)
    except:
        Message.error(request, ("Menu no se encuentra en la base de datos."))
        return Redirect.to_action(request, "index")
    if d.id <= 90:
        Message.warning(request, ("Lo sentimos, pero este menú no se puede editar."))
        return Redirect.to_action(request, "index")
    if request.method == "POST":
        try:
            d.title = request.POST.get("title")
            d.url = ("#" if not request.REQUEST.get("url") else request.REQUEST.get("url")).strip()
            d.icon = request.POST.get("icon")
            d.pos = request.POST.get("pos")
            d.module = request.POST.get("module")
            if d.permission:
                d.permission = None
            if request.POST.get("permission_id"):
                d.permission_id = Permission.objects.get(id=request.POST.get("permission_id")).id

            if d.parent:
                d.parent = None
            if request.POST.get("parent_id"):
                d.parent_id = Menu.objects.get(id=request.POST.get("parent_id")).id

            # if Menu.objects.exclude(id = d.id).filter(title = d.title).count() > 0:
            #     raise Exception( ("Menu <b>%(name)s</b> ya existe.") % {"name":d.title} )

            # salvar registro
            d.save()
            if d.id:
                Message.info(request, ("Menu <b>%(name)s</b> ha sido actualizado correctamente.") % {"name":d.title})
                return Redirect.to_action(request, "index")

        except Exception, e:
            Message.error(request, e)
    try:
        parent_list = Menu.objects.filter(parent_id=None, is_active=True)
        permission_list = Permission.objects.all()

    except Exception, e:
        Message.error(request, e)
    c = {
        "page_module":("Gestión de menús"),
        "page_title":("Actualizar menú."),
        "d":d,
        "MODULES":Menu.MODULES,
        "parent_list":parent_list,
        "permission_list":permission_list,
        }
    return render_to_response("sad/menu/edit.html", c, context_instance=RequestContext(request))

@permission_resource_required
def menu_state(request, state, key):
    """
    Inactiva y reactiva el estado del menú
    """
    id = SecurityKey.is_valid_key(request, key, "menu_%s" % state)
    if not id:
        return Redirect.to_action(request, "index")
    try:
        d = get_object_or_404(Menu, id=id)
    except:
        Message.error(request, ("Menú no se encuentra en la base de datos."))
        return Redirect.to_action(request, "index")
    try:
        if state == "inactivar" and d.is_active == False:
            Message.error(request, ("El menú ya se encuentra inactivo."))
        else:
            if state == "reactivar" and d.is_active == True:
                Message.error(request, ("El menú ya se encuentra activo."))
            else:
                d.is_active = (True if state == "reactivar" else False)
                d.save()
                if d.id:
                    if d.is_active:
                        Message.info(request, ("Menú <b>%(name)s</b> ha sido reactivado correctamente.") % {"name":d.title}, True)
                    else:
                        Message.info(request, ("Menú <b>%(name)s</b> ha sido inactivado correctamente.") % {"name":d.title}, True)
                    return Redirect.to_action(request, "index")
    except Exception, e:
        Message.error(request, e)
        return Redirect.to_action(request, "index")

@permission_resource_required
def menu_delete(request, key):
    """
    Elimina menú
    """
    id = SecurityKey.is_valid_key(request, key, "menu_del")
    if not id:
        return Redirect.to_action(request, "index")
    try:
        d = get_object_or_404(Menu, id=id)
    except:
        Message.error(request, ("Menú no se encuentra en la base de datos."))
        return Redirect.to_action(request, "index")
    if d.id <= 90:
        Message.warning(request, ("Lo sentimos, pero este menú no se puede eliminar."))
        return Redirect.to_action(request, "index")
    try:
        d.delete()
        if not d.id:
            Message.info(request, ("Menú <b>%(name)s</b> ha sido eliminado correctamente.") % {"name":d.title}, True)
            return Redirect.to_action(request, "index")
    except Exception, e:
        Message.error(request, e)
        return Redirect.to_action(request, "index")
    # endregion Menu
# endregion menu



# region module OK
@permission_resource_required
def module_index(request):
    """
    Página principal para trabajar con módulos del sistema (CRUD a la tabla sad_module)
    """
    try:
        module_list = Module.objects.all().order_by("module", "-id")
    except Exception, e:
        Message.error(request, e)
    c = {
        "page_module":("Gestión de módulos"),
        "page_title":("Listado de módulos del sistema."),
        "module_list":module_list,
        # "MODULES":dict((x, y) for x, y in Module.MODULES),
        "html":"<b>paragraph</b>",
        }
    return render_to_response("sad/module/index.html", c, context_instance=RequestContext(request))

@permission_resource_required
@transaction.atomic
def module_add(request):
    """
    Agrega módulo
    """
    d = Module()
    d.description = ""
    if request.method == "POST":
        try:
            sid = transaction.savepoint()
            d.module = request.POST.get("module")
            d.name = request.POST.get("name")
            d.description = request.POST.get("description")
            if Module.objects.exclude(id=d.id).filter(name=d.name).count() > 0:
                raise Exception(("Modulo <b>%(name)s</b> ya existe.") % {"name":d.name})
            d.save()

            groups = request.POST.getlist("groups")
            for value in groups:
                group = Group.objects.get(id=value)
                d.groups.add(group)
            
            initial_groups = request.POST.getlist("initial_groups")
            for value in initial_groups:
                group = Group.objects.get(id=value)
                d.initial_groups.add(group)

            if d.id:
                Message.info(request, ("Modulo <b>%(name)s</b> ha sido registrado correctamente.") % {"name":d.name})
                return Redirect.to_action(request, "index")
        except Exception, e:
            transaction.savepoint_rollback(sid)
            Message.error(request, e)
    try:
        group_list = Group.objects.all().order_by("name")
    except Exception, e:
        Message.error(request, e)
    c = {
        "page_module":("Gestión de módulos"),
        "page_title":("Agregar módulo."),
        "d":d,
        "group_list":group_list,
        "MODULES":Module.MODULES,
        }
    return render_to_response("sad/module/add.html", c, context_instance=RequestContext(request))

@permission_resource_required
@transaction.atomic
def module_edit(request, key):
    """
    Actualiza módulo
    """
    id = SecurityKey.is_valid_key(request, key, "module_upd")
    if not id:
        return Redirect.to_action(request, "index")
    d = None
    try:
        d = get_object_or_404(Module, id=id)
    except:
        Message.error(request, ("Módulo no se encuentra en la base de datos."))
        return Redirect.to_action(request, "index")

    if request.method == "POST":
        try:
            sid = transaction.savepoint()
            d.module = request.POST.get("module")
            d.name = request.POST.get("name")
            d.description = request.POST.get("description")
            if Module.objects.exclude(id=d.id).filter(name=d.name).count() > 0:
                raise Exception(("Modulo <b>%(name)s</b> ya existe.") % {"name":d.name})
            d.save()

            old_grupos_id_list_r = request.POST.get("old_grupos_id_list")
            if old_grupos_id_list_r:
                old_grupos_id_list_r = old_grupos_id_list_r.split(",")

            # Elimino los antiguos privilegios
            for value in  old_grupos_id_list_r:
                group = Group.objects.get(id=value)
                d.groups.remove(group)

            groups = request.POST.getlist("groups")
            for value in groups:
                group = Group.objects.get(id=value)
                d.groups.add(group)
            
            old_initial_groups_id_list_r = request.POST.get("old_initial_groups_id_list")
            if old_initial_groups_id_list_r:
                old_initial_groups_id_list_r = old_initial_groups_id_list_r.split(",")

            # Elimino los antiguos privilegios
            for value in  old_initial_groups_id_list_r:
                group = Group.objects.get(id=value)
                d.initial_groups.remove(group)

            initial_groups = request.POST.getlist("initial_groups")
            for value in initial_groups:
                group = Group.objects.get(id=value)
                d.initial_groups.add(group)

            if d.id:
                Message.info(request, ("Modulo <b>%(name)s</b> ha sido actualizado correctamente.") % {"name":d.name})
                return Redirect.to_action(request, "index")

        except Exception, e:
            transaction.savepoint_rollback(sid)
            Message.error(request, e)
    try:
        group_list = Group.objects.all().order_by("-id")
        old_grupos_id_list = list({i.id: i for i in d.groups.all()})
        old_initial_groups_id_list = list({i.id: i for i in d.initial_groups.all()})
    except Exception, e:
        Message.error(request, e)
    c = {
        "page_module":("Gestión de módulos"),
        "page_title":("Actualizar módulo."),
        "d":d,
        "group_list":group_list,
        "MODULES":Module.MODULES,
        "old_grupos_id_list":old_grupos_id_list,
        "old_initial_groups_id_list":old_initial_groups_id_list,
        }
    return render_to_response("sad/module/edit.html", c, context_instance=RequestContext(request))

@permission_resource_required
def module_state(request, state, key):
    """
    Inactiva y reactiva el estado del módulo
    """
    id = SecurityKey.is_valid_key(request, key, "module_%s" % state)
    if not id:
        return Redirect.to_action(request, "index")
    try:
        d = get_object_or_404(Module, id=id)
    except:
        Message.error(request, ("Módulo no se encuentra en la base de datos."))
        return Redirect.to_action(request, "index")
    try:
        if state == "inactivar" and d.is_active == False:
            Message.error(request, ("Módulo ya se encuentra inactivo."))
        else:
            if state == "reactivar" and d.is_active == True:
                Message.error(request, ("Módulo ya se encuentra activo."))
            else:
                d.is_active = (True if state == "reactivar" else False)
                d.save()
                if d.id:
                    if d.is_active:
                        Message.info(request, ("Módulo <b>%(name)s</b> ha sido reactivado correctamente.") % {"name":d.name}, True)
                    else:
                        Message.info(request, ("Módulo <b>%(name)s</b> ha sido inactivado correctamente.") % {"name":d.name}, True)
                    return Redirect.to_action(request, "index")
    except Exception, e:
        Message.error(request, e)
        return Redirect.to_action(request, "index")

@permission_resource_required
def module_delete(request, key):
    """
    Elimina módulo y sus dependencias
    """
    id = SecurityKey.is_valid_key(request, key, "module_del")
    if not id:
        return Redirect.to_action(request, "index")
    try:
        d = get_object_or_404(Module, id=id)
    except:
        Message.error(request, ("Módulo no se encuentra en la base de datos."))
        return Redirect.to_action(request, "index")
    try:
        # rastreando dependencias
        if d.solutions.count() > 0:
            raise Exception(("Módulo <b>%(name)s</b> está asignado en planes.") % {"name":d.name})

        d.delete()  # las dependencias grupos e initial_groups se eliminan automáticamente
        if not d.id:
            Message.info(request, ("Módulo <b>%(name)s</b> ha sido eliminado correctamente.") % {"name":d.name}, True)
            return Redirect.to_action(request, "index")
    except Exception, e:
        Message.error(request, e)
        return Redirect.to_action(request, "index")

@permission_resource_required
@transaction.atomic
def module_plans_edit(request):
    if request.method == "POST":
        try:
            sid = transaction.savepoint()
            privilegios_r = request.POST.getlist("privilegios")
            old_privilegios_r = request.POST.get("old_privilegios")
            if old_privilegios_r:
                old_privilegios_r = old_privilegios_r.split(",")

            # Elimino los antiguos privilegios
            for value in  old_privilegios_r:
                data = value.split("-")  # el formato es 1-4 = solution_id-module_id
                module = Module.objects.get(id=data[1])
                solution = Solution.objects.get(id=data[0])
                module.solutions.remove(solution)
            
            for value in  privilegios_r:
                data = value.split("-")  # el formato es 1-4 = solution_id-module_id
                module = Module.objects.get(id=data[1])
                solution = Solution.objects.get(id=data[0])
                module.solutions.add(solution)

            Message.info(request, ("Los planes se han actualizados correctamente!"))
        except Exception, e:
            transaction.savepoint_rollback(sid)
            Message.error(request, e)
    try:
        module_list = Module.objects.filter(is_active=True).order_by("module")
        solution_list = Solution.objects.filter(is_active=True).order_by("-id")

        # listar los privilegios y compararlos con los module y solution
        privilegios = []
        for m in module_list:
            for s in m.solutions.all() :
                privilegios.append("%s-%s" % (s.id, m.id))  # el formato es 1-4 = solution_id-module_id

        # for i in privilegios:
        #     print u"%s" % (i)
    except Exception, e:
        Message.error(request, e)
    c = {
        "page_module":("Gestión de planes"),
        "page_title":("Configuración de planes del sistema."),
        "module_list":module_list,
        "module_list_len":len(module_list),
        "solution_list":solution_list,
        "solution_list_len":len(solution_list),
        "privilegios":privilegios,
        }
    return render_to_response("sad/module/plans_edit.html", c, context_instance=RequestContext(request))
# endregion module







# region group OK
@permission_resource_required
def group_index(request):
    """
    Página principal para trabajar con perfiles o grupo de usuarios (CRUD a la tabla Group de django.contrib.auth.models)
    """
    try:
        group_list = Group.objects.all().order_by("-id")
    except Exception, e:
        Message.error(request, e)
    c = {
        "page_module":("Gestión de perfiles"),
        "page_title":("Listado de perfiles de usuario. (django.contrib.auth.models.Group)"),
        "group_list":group_list,
        }
    return render_to_response("sad/group/index.html", c, context_instance=RequestContext(request))

@permission_resource_required
def group_add(request):
    """
    Agrega perfil o grupo de usuarios en django.contrib.auth.models.Group
    """
    d = Group()

    if request.method == "POST":
        try:
            d.name = request.POST.get("name")
            if Group.objects.exclude(id=d.id).filter(name=d.name).count() > 0:
                raise Exception(("Perfil <b>%(name)s</b> ya existe.") % {"name":d.name})
            d.save()
            if d.id:
                Message.info(request, ("Perfil <b>%(name)s</b> ha sido registrado correctamente.") % {"name":d.name})
                return Redirect.to_action(request, "index")
        except Exception, e:
            Message.error(request, e)
    c = {
        "page_module":("Gestión de perfiles"),
        "page_title":("Agregar perfil (en django.contrib.auth.models.Group)."),
        "d":d,
        }
    return render_to_response("sad/group/add.html", c, context_instance=RequestContext(request))

@permission_resource_required
def group_edit(request, key):
    """
    Actualiza perfil o grupo de usuarios en django.contrib.auth.models.Group
    """
    id = SecurityKey.is_valid_key(request, key, "group_upd")
    if not id:
        return Redirect.to_action(request, "index")
    d = None
    try:
        d = get_object_or_404(Group, id=id)
    except:
        Message.error(request, ("Perfil no se encuentra en la base de datos."))
        return Redirect.to_action(request, "index")

    if request.method == "POST":
        try:
            d.name = request.POST.get("name")
            if Group.objects.exclude(id=d.id).filter(name=d.name).count() > 0:
                raise Exception(("Perfil <b>%(name)s</b> ya existe.") % {"name":d.name})
            d.save()
            if d.id:
                Message.info(request, ("Perfil <b>%(name)s</b> ha sido actualizado correctamente.") % {"name":d.name})
                return Redirect.to_action(request, "index")
        except Exception, e:
            Message.error(request, e)
    c = {
        "page_module":("Gestión de perfiles"),
        "page_title":("Actualizar perfil."),
        "d":d,
        }
    return render_to_response("sad/group/edit.html", c, context_instance=RequestContext(request))

@permission_resource_required
def group_delete(request, key):
    """
    Elimina perfil o grupo de usuarios de django.contrib.auth.models.Group
    """
    id = SecurityKey.is_valid_key(request, key, "group_del")
    if not id:
        return Redirect.to_action(request, "index")
    try:
        d = get_object_or_404(Group, id=id)
    except:
        Message.error(request, ("Perfil no se encuentra en la base de datos."))
        return Redirect.to_action(request, "index")
    try:
        # rastreando dependencias
        if d.permissions.count() > 0:
            raise Exception(("Perfil <b>%(name)s</b> tiene permisos asignados.") % {"name":d.name})
        if d.module_set.count() > 0:
            raise Exception(("Perfil <b>%(name)s</b> está asignado en módulos.") % {"name":d.name})
        if d.initial_groups_module_set.count() > 0:
            raise Exception(("Perfil <b>%(name)s</b> está asignado en módulos iniciales.") % {"name":d.name})
        if d.user_set.count() > 0:
            raise Exception(("Perfil <b>%(name)s</b> está asignado en usuarios.") % {"name":d.name})
        if d.userprofileassociation_set.count() > 0:
            raise Exception(("Perfil <b>%(name)s</b> está asignado en userprofileassociation.") % {"name":d.name})
        if d.userprofileenterprise_set.count() > 0:
            raise Exception(("Perfil <b>%(name)s</b> está asignado en userprofileenterprise.") % {"name":d.name})
        if d.userprofileheadquar_set.count() > 0:
            raise Exception(("Perfil <b>%(name)s</b> está asignado en userprofileheadquar.") % {"name":d.name})

        d.delete()
        if not d.id:
            Message.info(request, ("Perfil <b>%(name)s</b> ha sido eliminado correctamente.") % {"name":d.name}, True)
            return Redirect.to_action(request, "index")
    except Exception, e:
        Message.error(request, e)
        return Redirect.to_action(request, "index")

@permission_resource_required
@transaction.atomic
def group_permissions_edit(request):
    """
    Actualiza permisos(recursos) por grupo(perfil) de usuario en django.contrib.auth.models.Group.permissions.add(recurso)
    """
    if request.method == "POST":
        try:
            sid = transaction.savepoint()
            privilegios_r = request.POST.getlist("privilegios")
            old_privilegios_r = request.POST.get("old_privilegios")
            if old_privilegios_r:
                old_privilegios_r = old_privilegios_r.split(",")

            # Elimino los antiguos privilegios
            for value in  old_privilegios_r:
                data = value.split("-")  # el formato es 1-4 = recurso_id-perfil_id
                group = Group.objects.get(id=data[1])
                recur = Permission.objects.get(id=data[0])
                group.permissions.remove(recur)
            
            for value in  privilegios_r:
                data = value.split("-")  # el formato es 1-4 = recurso_id-perfil_id
                group = Group.objects.get(id=data[1])
                recur = Permission.objects.get(id=data[0])
                group.permissions.add(recur)
            Message.info(request, ("Los privilegios se han actualizados correctamente!"))
        except Exception, e:
            transaction.savepoint_rollback(sid)
            Message.error(request, e)
    try:
        resource_list = Permission.objects.all().order_by("content_type__app_label", "content_type__model")
        group_list = Group.objects.all().order_by("-id")

        # listar los privilegios y compararlos con los recursos(permisos) y perfiles(grupos)
        privilegios = []
        for g in group_list:
            for p in g.permissions.all() :
                privilegios.append("%s-%s" % (p.id, g.id))
    except Exception, e:
        Message.error(request, e)
    c = {
        "page_module":("Gestión de permisos"),
        "page_title":("Permisos y privilegios de usuarios. (auth_group_permissions)"),
        "resource_list":resource_list,
        "resource_list_len":len(resource_list),
        "group_list":group_list,
        "group_list_len":len(group_list),
        "privilegios":privilegios,
        }
    return render_to_response("sad/group/permissions_edit.html", c, context_instance=RequestContext(request))
# endregion group








# region resource OK
@permission_resource_required
def resource_index(request):
    """
    Página principal para trabajar con recursos (CRUD a la tabla Permission de django.contrib.auth.models)
    """
    try:
        resource_list = Permission.objects.all().order_by("content_type__app_label", "content_type__model")
    except Exception, e:
        Message.error(request, e)
    c = {
        "page_module":("Gestión de recursos"),
        "page_title":("Listado de recursos del sistema (django.contrib.auth.models.Permission)."),
        "resource_list":resource_list,
        }
    return render_to_response("sad/resource/index.html", c, context_instance=RequestContext(request))

@permission_resource_required
@transaction.atomic
def resource_add(request):
    """
    Agrega recurso en django.contrib.auth.models.Permission y obtiene o agrega un django.contrib.contenttypes.models.ContentType (ContentType.objects.get_or_create)
    """
    d = Permission()

    if request.method == "POST":
        try:
            sid = transaction.savepoint()
            d.description = request.POST.get("description")
            d.controller_view = request.POST.get("controller_view")
            d.app_label = request.POST.get("app_label")
            d.action_view = request.POST.get("action_view")
            content_type, is_content_type_created = ContentType.objects.get_or_create(
                name=d.controller_view.lower(),
                model=d.controller_view.lower(),
                app_label=d.app_label.lower(),
                )

            codename = ""
            recurso = "/%s/" % d.app_label.lower()
            if d.controller_view and d.action_view:
                codename = "%s_%s" % (d.controller_view.lower(), d.action_view.lower())
                recurso = "/%s/%s/%s/" % (d.app_label.lower(), d.controller_view.lower(), d.action_view.lower())
            if d.controller_view and not d.action_view:
                codename = "%s" % (d.controller_view.lower())
                recurso = "/%s/%s/" % (d.app_label.lower(), d.controller_view.lower())
            if not d.controller_view and d.action_view:
                raise Exception(("Complete controlador para la acción <b>%(action)s</b>.") % {"action":d.action_view})
            d.codename = codename
            d.name = request.POST.get("description")
            d.content_type = content_type
            if Permission.objects.exclude(id=d.id).filter(codename=d.codename, content_type=content_type).count() > 0:
                raise Exception(("Recurso <b>%(recurso)s</b> ya existe.") % {"recurso":recurso})

            d.save()
            if d.id:
                Message.info(request, ("Recurso %(recurso)s ha sido registrado correctamente.") % {"recurso":recurso})
                return Redirect.to_action(request, "index")
        except Exception, e:
            transaction.savepoint_rollback(sid)
            Message.error(request, e)
    c = {
        "page_module":("Gestión de recursos"),
        "page_title":("Agregar recurso (en django.contrib.contenttypes.models.ContentType y django.contrib.auth.models.Permission)."),
        "d":d,
        }
    return render_to_response("sad/resource/add.html", c, context_instance=RequestContext(request))

@permission_resource_required
@transaction.atomic
def resource_edit(request, key):
    """
    Actualiza recurso en django.contrib.auth.models.Permission y obtiene o agrega un django.contrib.contenttypes.models.ContentType (ContentType.objects.get_or_create)
    """
    id = SecurityKey.is_valid_key(request, key, "resource_upd")
    if not id:
        return Redirect.to_action(request, "index")
    d = None
    try:
        d = get_object_or_404(Permission, id=id)
        d.controller_view = d.content_type.name
        d.app_label = d.content_type.app_label
        codename_list = d.codename.split("_", 1)
        if len(codename_list) > 1:
            d.action_view = codename_list[1]
        d.description = d.name
    except:
        Message.error(request, ("Recurso no se encuentra en la base de datos."))
        return Redirect.to_action(request, "index")

    if d.id <= 50:
        Message.warning(request, ("Lo sentimos, pero este recurso no se puede editar."))
        return Redirect.to_action(request, "index")

    if request.method == "POST":
        try:
            sid = transaction.savepoint()
            d.controller_view = request.POST.get("controller_view")
            d.app_label = request.POST.get("app_label")
            d.action_view = request.POST.get("action_view")
            content_type, is_content_type_created = ContentType.objects.get_or_create(
                name=d.controller_view.lower(),
                model=d.controller_view.lower(),
                app_label=d.app_label.lower(),
                )

            codename = ""
            recurso = "/%s/" % d.app_label.lower()
            if d.controller_view and d.action_view:
                codename = "%s_%s" % (d.controller_view.lower(), d.action_view.lower())
                recurso = "/%s/%s/%s/" % (d.app_label.lower(), d.controller_view.lower(), d.action_view.lower())
            if d.controller_view and not d.action_view:
                codename = "%s" % (d.controller_view.lower())
                recurso = "/%s/%s/" % (d.app_label.lower(), d.controller_view.lower())
            if not d.controller_view and d.action_view:
                raise Exception(("Complete controlador para la acción <b>%(action)s</b>.") % {"action":d.action_view})
            d.codename = codename
            d.name = request.POST.get("description")
            d.content_type = content_type

            if Permission.objects.exclude(id=d.id).filter(codename=d.codename, content_type=content_type).count() > 0:
                raise Exception(("Recurso <b>%(recurso)s</b> ya existe.") % {"recurso":recurso})

            # salvar registro
            d.save()
            if d.id:
                Message.info(request, ("Recurso <b>%(recurso)s</b> ha sido actualizado correctamente.") % {"recurso":recurso})
                return Redirect.to_action(request, "index")

        except Exception, e:
            transaction.savepoint_rollback(sid)
            Message.error(request, e)
    c = {
        "page_module":("Gestión de recursos"),
        "page_title":("Actualizar recurso."),
        "d":d,
        }
    return render_to_response("sad/resource/edit.html", c, context_instance=RequestContext(request))

@permission_resource_required
def resource_delete(request, key):
    """
    Elimina recurso de django.contrib.auth.models.Permission
    """
    id = SecurityKey.is_valid_key(request, key, "resource_del")
    if not id:
        return Redirect.to_action(request, "index")
    try:
        d = get_object_or_404(Permission, id=id)
        recurso = "/%s/" % d.content_type.app_label
        if d.codename:
            recurso = "/%s/%s/" % (d.content_type.app_label, d.content_type.name)
            codename_list = d.codename.split("_", 1)
            if len(codename_list) > 1:
                recurso = "/%s/%s/%s/" % (d.content_type.app_label, d.content_type.name, codename_list[1])
    except:
        Message.error(request, ("Recurso no se encuentra en la base de datos."))
        return Redirect.to_action(request, "index")

    if d.id <= 50:
        Message.warning(request, ("Lo sentimos, pero este recurso no se puede eliminar."))
        return Redirect.to_action(request, "index")
    try:
        # rastreando dependencias
        if d.group_set.count() > 0:
            raise Exception(("Recurso <b>%(recurso)s</b> está asignado en perfiles.") % {"recurso":recurso})
        if d.menu_set.count() > 0:
            raise Exception(("Recurso <b>%(recurso)s</b> está asignado en menús.") % {"recurso":recurso})
        if d.user_set.count() > 0:
            raise Exception(("Recurso <b>%(recurso)s</b> está asignado en usuarios.") % {"recurso":recurso})

        d.delete()
        if not d.id:
            Message.info(request, ("Recurso <b>%(recurso)s</b> ha sido eliminado correctamente.") % {"recurso":recurso}, True)
            return Redirect.to_action(request, "index")
    except Exception, e:
        Message.error(request, e)
        return Redirect.to_action(request, "index")
# endregion resource