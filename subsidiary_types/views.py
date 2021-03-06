from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from rbacx.functions import has_permission
from rbacx.models import Operation
from xindex.models import Subsidiary_Type
from django.http import HttpResponseRedirect, HttpResponse
from subsidiary_types.forms import AddSubsidiaryType
from django.template.context import RequestContext
from django.utils import simplejson
from xindex.models import Subsidiary, Company

#VIEW = "Ver"
#CREATE = "Crear"
#DELETE = "Eliminar"
#UPDATE = "Editar"

VIEW = Operation.objects.get(name="Ver")
CREATE = Operation.objects.get(name="Crear")
DELETE = Operation.objects.get(name="Eliminar")
UPDATE = Operation.objects.get(name="Editar")


@login_required(login_url='/signin/')
def index(request):

    if has_permission(request.user, VIEW, "Ver tipos de subsidiarias") or \
            request.user.is_superuser:

        all_subsidiary_types = Subsidiary_Type.objects.all().order_by('-name')
        for s_t in all_subsidiary_types:
            print s_t.name
        template_vars = {
            "titulo": "Tipos de subsidiarias",
            "message": "",
            "all_subsidiary_types": all_subsidiary_types
        }
        request_context = RequestContext(request, template_vars)
        return render_to_response("subsidiary_types/index.html", request_context)
    else:
        template_vars = {}
        request_context = RequestContext(request, template_vars)
        return render_to_response("rbac/generic_error.html", request_context)


@login_required(login_url='/signin/')
def add(request):

    if has_permission(request.user, CREATE, "Crear tipos de subsidiarias") or \
            request.user.is_superuser:

        if request.POST:
            formulario = AddSubsidiaryType(request.POST or None)
            if formulario.is_valid():
                formulario.save()
                template_vars = {
                    "titulo": "Tipos de subsidiarias",
                    "message": "Se ha dado de alta el tipo de subsidiaria",
                    "formulario": formulario
                }
                request_context = RequestContext(request, template_vars)
                return HttpResponseRedirect('/subsidiary_types')
            else:
                template_vars = {
                    "titulo": "Agregar tipo de subsidiaria",
                    "message": "",
                    "formulario": formulario
                }
                request_context = RequestContext(request, template_vars)
                return render_to_response("subsidiary_types/add.html",
                                          request_context)

        else:
            formulario = AddSubsidiaryType()
            template_vars = {
                "titulo": "Agregar tipo de subsidiaria",
                "message": "",
                "formulario": formulario
            }
            request_context = RequestContext(request, template_vars)
            return render_to_response("subsidiary_types/add.html", request_context)
    else:
        template_vars = {}
        request_context = RequestContext(request, template_vars)
        return render_to_response("rbac/generic_error.html", request_context)


@login_required(login_url='/signin/')
def update(request, subsidiary_type_id):

    if has_permission(request.user, UPDATE, "Editar tipos de subsidiarias") or \
            request.user.is_superuser:

        try:
            sub_type = Subsidiary_Type.objects.get(id=subsidiary_type_id)
        except Subsidiary_Type.DoesNotExist:
            sub_type = False

        if sub_type:
            if request.POST:
                formulario = AddSubsidiaryType(request.POST or None,
                                               instance=sub_type)
                if formulario.is_valid():
                    formulario.save()
                    template_vars = {
                        "titulo": "Tipos de subsidiarias",
                        "message": "Se ha modificado el tipo de subsidiaria"
                    }
                    request_context = RequestContext(request, template_vars)
                    return HttpResponseRedirect('/subsidiary_types/')
                else:
                    template_vars = {
                        "titulo": "Editar tipo de subsidiaria",
                        "message": "",
                        "formulario": formulario
                    }
                    request_context = RequestContext(request, template_vars)
                    return render_to_response("subsidiary_types/update.html",
                                              request_context)
            else:
                formulario = AddSubsidiaryType(request.POST or None,
                                               instance=sub_type)
                template_vars = {
                    "titulo": "Editar tipo de subsidiaria",
                    "message": "",
                    "formulario": formulario,
                    "subsidiary_type_id": subsidiary_type_id
                }
                request_context = RequestContext(request, template_vars)
                return render_to_response("subsidiary_types/update.html",
                                          request_context)
        else:
            message = "No se ha podido encontrar la subsidiaria"
            return HttpResponseRedirect('/subsidiary_types/')
    else:
        template_vars = {}
        request_context = RequestContext(request, template_vars)
        return render_to_response("rbac/generic_error.html", request_context)


@login_required(login_url='/signin/')
def remove(request, subsidiary_type_id):

    if has_permission(request.user, DELETE, "Eliminar tipos de subsidiarias") or \
            request.user.is_superuser:

        try:
            sub_type = Subsidiary_Type.objects.get(id=subsidiary_type_id)
        except Subsidiary_Type.DoesNotExist:
            sub_type = False

        if sub_type:
            try:
                sub_type.active = False
                sub_type.save()
                message="Se ha eliminado el tipo de subsidiaria"
                template_vars = {
                    "titulo": "Tipos de subsidiarias",
                    "message": message
                }
                return HttpResponse("Si")

            except:
                message = "No se pudo eliminar el tipo de subsidiaria"
                template_vars = {
                    "titulo": "Tipos de subsidiarias",
                    "message": message
                }
                request_context = RequestContext(request, template_vars)
                return HttpResponse('No se pudo eliminar el tipo de subsidiaria')
        else:
            message = "No se ha encontrado el tipo de subsidiaria"
            template_vars = {
                "titulo": "tipos de subsidiarias",
                "message": message
            }
            return HttpResponseRedirect('/subsidiary_types')
    else:
        template_vars = {}
        request_context = RequestContext(request, template_vars)
        return render_to_response("rbac/generic_error.html", request_context)


@login_required(login_url='/signin/')
def getSTInJson(request):
    s_types = {'s_types': []}

    for st in Subsidiary_Type.objects.filter(active=True).order_by('-date'):
        s_types['s_types'].append(
            {
                "name": st.name,
                "description": st.description,
                "st_det": st.id,
                "st_up": st.id,
                "st_del": st.id
            }
        )

    return HttpResponse(simplejson.dumps(s_types))


@login_required(login_url='/signin/')
def details(request, subsidiary_type_id):

    if has_permission(request.user, VIEW, "Ver tipos de subsidiarias") or \
            request.user.is_superuser:

        template_vars = {
            'titulo': 'Detalles'
        }
        try:
            sub_t = Subsidiary_Type.objects.get(id=subsidiary_type_id)

            sub_t = False if sub_t.active==False else sub_t
        except Subsidiary_Type.DoesNotExist:
            sub_t = False

        template_vars['sub_t'] = sub_t
        request_context = RequestContext(request, template_vars)
        return render_to_response('subsidiary_types/details.html', request_context)
    else:
        template_vars = {}
        request_context = RequestContext(request, template_vars)
        return render_to_response("rbac/generic_error.html", request_context)


@login_required(login_url='/signin/')
def stByCompany(request):

    global company_id
    user = request.user.id

    companies = Company.objects.all()

    for c in companies:
        for u in c.staff.all():
            if user == u.user.id:
                company_id = c.id

    subsidiaries = Subsidiary.objects.filter(company_id=company_id)

    sub_t = {'subsidiary_types': []}

    for subsidiary in subsidiaries:
        for st in subsidiary.subsidiary_types.all():
            sub_t['subsidiary_types'].append(
                {
                    'name': st.name,
                    'id': st.id
                }
            )

    sub_types = {'subsidiary_types': []}

    for st in sub_t['subsidiary_types']:
        counter = 0
        for sub_t in sub_types['subsidiary_types']:
            if st['name'] == sub_t['name']:
                counter = counter + 1

        if counter == 0:
            sub_types['subsidiary_types'].append(
                {
                    'name': st['name'],
                    'id': st['id']
                }
            )

    return HttpResponse(simplejson.dumps(sub_types))