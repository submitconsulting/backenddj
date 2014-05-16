# _*_ coding: utf-8 _*_
"""
@copyright   Copyright (c) 2014 Submit Consulting
@author      Angel Sullon (@asullom)
@package     account

Descripcion: Implementacion de los controladores de la app account
"""
from django.shortcuts import render_to_response, redirect
from django.template.context import RequestContext
from apps.utils.decorators import permission_resource_required
from django.contrib.auth.decorators import login_required
from apps.utils.messages import Message
from django.db import transaction
from django.contrib.auth.models import User, Group
from apps.params.models import Person
from apps.space.models import Association, Enterprise, Headquar, Solution
from apps.sad.models import Profile, Module, UserProfileAssociation, UserProfileEnterprise, UserProfileHeadquar
from unicodedata import normalize
from django.db.models import Q
from apps.utils.security import Redirect, DataAccessToken
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from apps.sad.models import Access
#from django.contrib.auth.views import redirect_to_login

# region registro cuenta OK
@login_required(login_url="/accounts/login/")
@transaction.atomic
def add_enterprise(request):

    d = Enterprise()
    if request.method == "POST":
        try:
            sid = transaction.savepoint()
            d.enterprise_name = request.POST.get("enterprise_name")
            d.enterprise_tax_id = request.POST.get("enterprise_tax_id")
            d.association_name = request.POST.get("association_name")
            d.association_type_a = request.POST.get("association_type_a")
            d.solution_id = request.POST.get("solution_id")
            
            solution = Solution.objects.get(id=d.solution_id)
            d.logo = request.POST.get("empresa_logo")
            user = request.user
            
            association = Association(name=d.association_name, type_a=d.association_type_a, solution=solution, logo=d.logo)
            if normalize("NFKD", u"%s" % d.association_name).encode("ascii", "ignore").lower() in list(
                normalize("NFKD", u"%s" % col["name"]).encode("ascii", "ignore").lower() for col in Association.objects.values("name")
                ):
                raise Exception("La asociación <b>%s</b> ya existe " % (d.association_name))
            association.save()

            enterprise = Enterprise(name=d.enterprise_name, tax_id=d.enterprise_tax_id, type_e=d.association_type_a, solution=solution, logo=d.logo)
            if normalize("NFKD", u"%s" % d.enterprise_name).encode("ascii", "ignore").lower() in list(
                normalize("NFKD", u"%s" % col["name"]).encode("ascii", "ignore").lower() for col in Enterprise.objects.values("name")
                ):
                raise Exception("La empresa <b>%s</b> ya existe " % (d.enterprise_name))
            if Enterprise.objects.filter(tax_id=d.enterprise_tax_id).count() > 0:
                raise Exception("La empresa con RUC <b>%s</b> ya existe " % (d.enterprise_tax_id))
            enterprise.save()

            headquar = Headquar(name="Principal", association=association, enterprise=enterprise)
            headquar.save()
            
            # asigna permisos al usuario para manipular datos de cierta sede, empresa o asociación
            group_dist_list = []
            for module in solution.module_set.all():  # .distinct()    
                for group in module.initial_groups.all() :
                    if len(group_dist_list) == 0 :
                        group_dist_list.append(group.id)
                        user.groups.add(group)
                        
                        user_profile_association = UserProfileAssociation()
                        user_profile_association.user = user
                        user_profile_association.association = association
                        user_profile_association.group = group
                        user_profile_association.save()

                        user_profile_enterprise = UserProfileEnterprise()
                        user_profile_enterprise.user = user
                        user_profile_enterprise.enterprise = enterprise
                        user_profile_enterprise.group = group
                        user_profile_enterprise.save()
                        
                        user_profile_headquar = UserProfileHeadquar()
                        user_profile_headquar.user = user
                        user_profile_headquar.headquar = headquar
                        user_profile_headquar.group = group
                        user_profile_headquar.save()
                    else :
                        if group.id not in group_dist_list:
                            group_dist_list.append(group.id)
                            user.groups.add(group)

                            user_profile_association = UserProfileAssociation()
                            user_profile_association.user = user
                            user_profile_association.association = association
                            user_profile_association.group = group
                            user_profile_association.save()

                            user_profile_enterprise = UserProfileEnterprise()
                            user_profile_enterprise.user = user
                            user_profile_enterprise.enterprise = enterprise
                            user_profile_enterprise.group = group
                            user_profile_enterprise.save()
                            
                            user_profile_headquar = UserProfileHeadquar()
                            user_profile_headquar.user = user
                            user_profile_headquar.headquar = headquar
                            user_profile_headquar.group = group
                            user_profile_headquar.save()
            Message.info(request, ("Empresa <b>%(name)s</b> ha sido registrado correctamente!.") % {"name":d.enterprise_name})
            return Redirect.to(request, "/accounts/choice_headquar/")
        except Exception, e:
            transaction.savepoint_rollback(sid)
            Message.error(request, e)
    try:
        solution_list = Solution.objects.filter(is_active=True).order_by("id")
    except Exception, e:
        Message.error(request, e)
    c = {
        "page_module":("Registro de empresa"),
        "page_title":("Agregar nueva empresa a la cuenta de <b>%(login)s</b>.") % {"login":request.user},
        "d":d,
        "solution_list":solution_list,
        "ASSOCIATION_TYPES":Association.TYPES,
        }
    return render_to_response("accounts/add_enterprise.html", c, context_instance=RequestContext(request))

@transaction.atomic
def signup_sys(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect("/accounts/choice_headquar/")
    d = Person()
    d.first_name = ""
    d.last_name = ""
    d.identity_num = ""
    if request.method == "POST":
        try:
            sid = transaction.savepoint()
            d.first_name = request.POST.get("first_name")
            d.last_name = request.POST.get("last_name")
            d.username = request.POST.get("login")
            d.enterprise_name = request.POST.get("enterprise_name")
            d.enterprise_tax_id = request.POST.get("enterprise_tax_id")
            d.association_name = request.POST.get("association_name")
            d.association_type_a = request.POST.get("association_type_a")
            d.solution_id = request.POST.get("solution_id")
            d.email = request.POST.get("email")
            d.photo = request.POST.get("persona_fotografia")
            
            d.identity_type = Person.DEFAULT #request.POST.get("identity_type")
            d.identity_num = request.POST.get("identity_num")
            identity_type_display = dict((x, y) for x, y in Person.IDENTITY_TYPES)[d.identity_type]
            
            solution = Solution.objects.get(id=d.solution_id)
            d.solution = solution
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

            association = Association(name=d.association_name, type_a=d.association_type_a, solution=solution)
            if normalize("NFKD", u"%s" % d.association_name).encode("ascii", "ignore").lower() in list(
                normalize("NFKD", u"%s" % col["name"]).encode("ascii", "ignore").lower() for col in Association.objects.values("name")
                ):
                raise Exception("La asociación <b>%s</b> ya existe " % (d.association_name))
            association.save()

            enterprise = Enterprise(name=d.enterprise_name, tax_id=d.enterprise_tax_id, type_e=d.association_type_a, solution=solution)
            if normalize("NFKD", u"%s" % d.enterprise_name).encode("ascii", "ignore").lower() in list(
                normalize("NFKD", u"%s" % col["name"]).encode("ascii", "ignore").lower() for col in Enterprise.objects.values("name")
                ):
                raise Exception("La empresa <b>%s</b> ya existe " % (d.enterprise_name))
            if Enterprise.objects.filter(tax_id=d.enterprise_tax_id).count() > 0:
                raise Exception("La empresa con RUC <b>%s</b> ya existe " % (d.enterprise_tax_id))
            enterprise.save()
            
            headquar = Headquar(name="Principal", association=association, enterprise=enterprise)
            
            headquar.save()
            
            # asigna permisos al usuario para manipular datos de cierta sede, empresa o asociación
            group_dist_list = []
            for module in solution.module_set.all():  # .distinct()    
                for group in module.initial_groups.all() :
                    if len(group_dist_list) == 0 :
                        group_dist_list.append(group.id)
                        user.groups.add(group)
                        
                        user_profile_association = UserProfileAssociation()
                        user_profile_association.user = user
                        user_profile_association.association = association
                        user_profile_association.group = group
                        user_profile_association.save()

                        user_profile_enterprise = UserProfileEnterprise()
                        user_profile_enterprise.user = user
                        user_profile_enterprise.enterprise = enterprise
                        user_profile_enterprise.group = group
                        user_profile_enterprise.save()
                        
                        user_profile_headquar = UserProfileHeadquar()
                        user_profile_headquar.user = user
                        user_profile_headquar.headquar = headquar
                        user_profile_headquar.group = group
                        user_profile_headquar.save()
                    else :
                        if group.id not in group_dist_list:
                            group_dist_list.append(group.id)
                            user.groups.add(group)

                            user_profile_association = UserProfileAssociation()
                            user_profile_association.user = user
                            user_profile_association.association = association
                            user_profile_association.group = group
                            user_profile_association.save()

                            user_profile_enterprise = UserProfileEnterprise()
                            user_profile_enterprise.user = user
                            user_profile_enterprise.enterprise = enterprise
                            user_profile_enterprise.group = group
                            user_profile_enterprise.save()
                            
                            user_profile_headquar = UserProfileHeadquar()
                            user_profile_headquar.user = user
                            user_profile_headquar.headquar = headquar
                            user_profile_headquar.group = group
                            user_profile_headquar.save()
            Message.info(request, ("Cuenta <b>%(name)s</b> ha sido registrado correctamente!.") % {"name":d.username})
            if request.is_ajax():
                request.path = "/accounts/login/"  # /app/controller_path/action/$params
                return redirect("/accounts/login/")
                # return login_sys(request)
            else:
                return redirect("/accounts/login/")
        except Exception, e:
            transaction.savepoint_rollback(sid)
            Message.error(request, e)
    try:
        solution_list = Solution.objects.filter(is_active=True).order_by("id")
    except Exception, e:
        Message.error(request, e)
    c = {
        "page_module":("Crear cuenta"),
        "page_title":("Registro de la cuenta."),
        "d":d,
        "solution_list":solution_list,
        "ASSOCIATION_TYPES":Association.TYPES,
        "IDENTITY_TYPE_DEFAULT":dict((x, y) for x, y in Person.IDENTITY_TYPES)[Person.DEFAULT],
        }
    return render_to_response("accounts/signup.html", c, context_instance=RequestContext(request))
# endregion registro cuenta

# region login OK

@login_required(login_url="/accounts/login/")
def load_access(request, headquar_id, module_id):
    if request.is_ajax():
        return HttpResponse("ESTA OPERACION NO DEBE SER CARGADO CON AJAX, Presione F5")
    else:
        try:
            try:
                headquar = Headquar.objects.get(id=headquar_id)
            except:
                Message.error(request, ("Sede no seleccionado o no se encuentra en la base de datos."))
                return Redirect.to(request, "/accounts/choice_headquar/")
            try:
                module = Module.objects.get(id=module_id)
            except:
                Message.error(request, ("Módulo no seleccionado o no se encuentra en la base de datos."))
                return Redirect.to(request, "/accounts/choice_headquar/")

            if not request.user.is_superuser:  # vovler a verificar si tiene permisos
                # obteniendo las sedes a la cual tiene acceso
                headquar_list = Headquar.objects.filter(userprofileheadquar__user__id=request.user.id).distinct()
                if headquar not in headquar_list:
                    raise Exception(("Acceso denegado. No tiene privilegio para ingresar a esta sede: %s %s." % (headquar.enterprise.name, headquar.name)))
                # obteniendo los módulos a la cual tiene acceso
                group_list = Group.objects.filter(userprofileheadquar__headquar__id=headquar.id, userprofileheadquar__user__id=request.user.id).distinct()
                module_list = Module.objects.filter(groups__in=group_list).distinct()
                
                if module not in module_list:
                    raise Exception(("Acceso denegado. No tiene privilegio para ingresar a este módulo: %s de %s %s." % (module.name, headquar.enterprise.name, headquar.name)))
                
            # cargando permisos de datos para el usuario
            DataAccessToken.set_association_id(request, headquar.association.id)
            DataAccessToken.set_enterprise_id(request, headquar.enterprise.id)
            DataAccessToken.set_headquar_id(request, headquar.id)

            try:
                profile = Profile.objects.get(user_id=request.user.id)
                if profile.id:
                    profile.last_headquar_id = headquar_id
                    profile.last_module_id = module_id
                    profile.save()
            except:
                person = Person(first_name=request.user.first_name, last_name=request.user.last_name)
                person.save()

                profile = Profile(user=request.user, last_headquar_id=headquar_id, last_module_id=module_id)
                profile.person = person
                profile.save()
                pass

            # Message.info(request, ("La sede %(name)s ha sido cargado correctamente.") % {"name":headquar_id} )
            if module.BACKEND == module.module:
                return Redirect.to(request, "/mod_backend/dashboard/")
            if module.VENTAS == module.module:
                return Redirect.to(request, "/mod_ventas/dashboard/")
            if module.PRO == module.module:
                return Redirect.to(request, "/mod_pro/dashboard/")
            # TODO agregue aqui su nuevo modulo
            else:
                Message.error(request, "Módulo no definido")
                return HttpResponseRedirect("/accounts/choice_headquar/")
        except Exception, e:
            Message.error(request, e)
        return HttpResponseRedirect("/accounts/choice_headquar/")
        # return HttpResponse("Ocurrió un grave error, comunique al administrador del sistema")

def login_sys(request):
    d = User()
    c = {
        "page_module":("Login"),
        "page_title":("Login."),
        "d":d,
        }

    if request.user.is_authenticated():
        try:  # intentar cargar la última session
            profile = Profile.objects.get(user_id=request.user.id)
            if profile.last_headquar_id and profile.last_module_id:
                if request.is_ajax():
                    request.path = "/accounts/load_access/%s/%s/" % (profile.last_headquar_id, profile.last_module_id)  # /app/controller_path/action/$params
                    return load_access(request, profile.last_headquar_id, profile.last_module_id)
                else:                        
                    return redirect("/accounts/load_access/%s/%s/" % (profile.last_headquar_id, profile.last_module_id))
        except:
            pass
        return HttpResponseRedirect("/accounts/choice_headquar/")
    if request.method == "POST":
        
        d.username = request.POST.get("login")
        password = request.POST.get("password")
        if '@' in d.username:
            try:
                check = User.objects.get(email=d.username)
                d.username = check.username
            except:
                pass
            
        account = authenticate(username=d.username, password=password)
        if account is not None and account.is_active is True:
            login(request, account)
            Access.objects.create(
                                  #access_type=Access.INPUT,
                                  ip=request.META['REMOTE_ADDR'],
                                  session_key=request.session['_auth_user_id'], #account.pk,
                                  user=account,
                                  )
            # cargando sesión para el usuario. no necesita
            # request.session["id"] = "Hola"
            if request.REQUEST.get("next"):
                return HttpResponseRedirect(request.REQUEST.get("next"))
            #redirect_to_login(request.REQUEST.get("next"))
            try:
                profile = Profile.objects.get(user_id=account.id)
                if profile:
                    Message.info(request, ("Bienvenido <b>%(name)s %(ape)s</b>.") % {"name":account.profile.person.first_name,"ape":account.profile.person.last_name})
            except:
                Message.info(request, ("Bienvenido <b>%(name)s</b>.") % {"name":account.username})
                pass
            try:  # intentar cargar la última session
                profile = Profile.objects.get(user_id=request.user.id)
                if profile.last_headquar_id and profile.last_module_id:
                    if request.is_ajax():
                        request.path = "/accounts/load_access/%s/%s/" % (profile.last_headquar_id, profile.last_module_id)  # /app/controller_path/action/$params
                        return load_access(request, profile.last_headquar_id, profile.last_module_id)
                    else:                        
                        return redirect("/accounts/load_access/%s/%s/" % (profile.last_headquar_id, profile.last_module_id))
            except:
                pass
            return HttpResponseRedirect("/accounts/choice_headquar/")
        else:
            Message.error(request, ("Contaseña para <b>%(name)s</b> no válido, o el usuario no existe o no está activo. ") % {"name":d.username})
            return render_to_response("accounts/login.html", c, context_instance=RequestContext(request))
    else:
        """ user is not submitting the form, show the login form """
        return render_to_response("accounts/login.html", c, context_instance=RequestContext(request))

def logout_sys(request):
    try:
        Access.objects.create(
                                  access_type=Access.OUTPUT,
                                  ip=request.META['REMOTE_ADDR'],
                                  session_key=request.user.pk,
                                  user=request.user,
                                  )
    except:
        pass
    logout(request)
    
    return HttpResponseRedirect("/")

@permission_resource_required
@transaction.atomic
def user_profile_edit(request):
    """
    Actualiza perfil del usuario
    """
    d = None
    try:
        d = request.user
        try:
            profile = Profile.objects.get(user_id=d.id)
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
        
    if request.method == "POST":
        try:
            sid = transaction.savepoint()
            # d.username = request.POST.get("login")       
            # if User.objects.exclude(id = d.id).filter(username = d.username).count()>0:
            #     raise Exception( "El usuario <b>%s</b> ya existe " % d.username )
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
                raise Exception("La persona <b>%s %s</b> y %s:<b>%s</b> ya existe " % (d.first_name, d.last_name, identity_type_display, d.identity_num))
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
                Message.info(request, ("Usuario <b>%(name)s</b> ha sido actualizado correctamente.") % {"name":d.username}, True)
                return Redirect.to(request, "/accounts/choice_headquar/")

        except Exception, e:
            transaction.savepoint_rollback(sid)
            Message.error(request, e)
            
    try:
        
        user_profile_headquar_list = UserProfileHeadquar.objects.filter(user=d).order_by("headquar")
        user_profile_enterprise_list = UserProfileEnterprise.objects.filter(user=d).order_by("enterprise")
        user_profile_association_list = UserProfileAssociation.objects.filter(user=d).order_by("association")

    except Exception, e:
        Message.error(request, e)
    c = {
        "page_module":("Perfil del usuario"),
        "page_title":("Actualizar información del usuario."),
        "d":d,
        "user_profile_headquar_list":user_profile_headquar_list,
        "user_profile_enterprise_list":user_profile_enterprise_list,
        "user_profile_association_list":user_profile_association_list,
        "IDENTITY_TYPES":Person.IDENTITY_TYPES,
        }
    return render_to_response("accounts/profile_edit.html", c, context_instance=RequestContext(request))
# endregion login



#@csrf_exempt
#@permission_resource_required
@login_required
def choice_headquar(request, field="enterprise__name", value="None"):
    """
    Muestra el listado de sedes con sus respectivos módulos a las cuales el usuario tiene acceso 
    """
    field = (field if not request.REQUEST.get("field") else request.REQUEST.get("field")).strip()
    value = (value if not request.REQUEST.get("value") else request.REQUEST.get("value")).strip()

    value_f = "" if value == "None" else value
    column_contains = u"%s__%s" % (field, "contains")

    headquar_list_by_user = []
    headquar_list = []
    if request.user.is_superuser:
        headquar_list = Headquar.objects.filter(**{ column_contains: value_f }).order_by("-association__name", "-enterprise__name", "-id").distinct()  # Trae todo
    else:
        if request.user.id:
            # print "--%s" % request.user.id
            headquar_list = Headquar.objects.filter(**{ column_contains: value_f }).filter(userprofileheadquar__user__id=request.user.id).order_by("-association__name", "-enterprise__name", "-id").distinct()  # request.user.id
    
    for headquar in headquar_list:
        group_list = Group.objects.filter(userprofileheadquar__headquar__id=headquar.id, userprofileheadquar__user__id=request.user.id).distinct()
        module_list = Module.objects.filter(groups__in=group_list).distinct()
        if request.user.is_superuser:
            """
            permitir ingresar al módulo:Django Backend 
            """
            if len(module_list) == 0:
                module_list = Module.objects.filter(module=Module.BACKEND).distinct()
            else:
                if Module.objects.get(module=Module.BACKEND) not in module_list:
                    module_list = Module.objects.filter(Q(groups__in=group_list) | Q(module=Module.BACKEND)).distinct()

        headquar_list_by_user.append({
            "association": headquar.association,
            "enterprise": headquar.enterprise,
            "headquar": headquar,
            "modules": module_list,
            "groups": group_list,
            })
    
    c = {
        "page_module":("Elegir Módulo"),
        "page_title":("Listado de empresas en los cuales colabora."),
        "headquar_list": headquar_list_by_user,

        "field":field,
        "value":value.replace("/", "-"),
        # "order":order,
        }
    return render_to_response("accounts/choice_headquar.html", c, context_instance=RequestContext(request))
