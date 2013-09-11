# Create your views here.
from django.shortcuts import render_to_response
from xindex.models import Subsidiary_Type
from django.http import HttpResponseRedirect, HttpResponse
from subsidiary_types.forms import AddSubsidiaryType
from django.template.context import RequestContext
from django.utils import simplejson

def index(request, message = ''):
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

def add(request):
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
            #return render_to_response("subsidiary_types/index.html", request_context)
            return HttpResponseRedirect('/subsidiary_types')
        else:
            template_vars = {
                "titulo": "Agregar tipo de subsidiaria",
                "message": "",
                "formulario": formulario
            }
            request_context = RequestContext(request, template_vars)
            return render_to_response("subsidiary_types/add.html", request_context)

    else:
        formulario = AddSubsidiaryType()
        template_vars = {
            "titulo": "Agregar tipo de subsidiaria",
            "message": "",
            "formulario": formulario
        }
        request_context = RequestContext(request, template_vars)
        return render_to_response("subsidiary_types/add.html", request_context)


def update(request, subsidiary_type_id):
    try:
        sub_type = Subsidiary_Type.objects.get(id=subsidiary_type_id)
    except Subsidiary_Type.DoesNotExist:
        sub_type = False

    if sub_type:
        if request.POST:
            formulario = AddSubsidiaryType(request.POST or None, instance=sub_type)
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
                return render_to_response("subsidiary_types/update.html", request_context)
        else:
            formulario = AddSubsidiaryType(request.POST or None, instance=sub_type)
            template_vars = {
                "titulo": "Editar tipo de subsidiaria",
                "message": "",
                "formulario": formulario
            }
            request_context = RequestContext(request, template_vars)
            return render_to_response("subsidiary_types/update.html", request_context)
    else:
        message = "No se ha podido encontrar la subsidiaria"
        return HttpResponseRedirect('/subsidiary_types/')


def remove(request, subsidiary_type_id):

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
            request_context = RequestContext(request, template_vars)
            #return render_to_response("subsidiary_types/index.html", request_context)
            return HttpResponseRedirect('/subsidiary_types')

        except:
            message = "No se pudo eliminar el tipo de subsidiaria"
            template_vars = {
                "titulo": "Tipos de subsidiarias",
                "message": message
            }
            request_context = RequestContext(request, template_vars)
            #return render_to_response("subsidiary_types/index.html", request_context)
            return HttpResponse('No se pudo eliminar el tipo de subsidiaria')
    else:
        message = "No se ha encontrado el tipo de subsidiaria"
        template_vars = {
            "titulo": "tipos de subsidiarias",
            "message": message
        }
        request_context = RequestContext(request, template_vars)
        #return render_to_response("subsidiary_types/index.html", request_context)
        #return HttpResponse('No se encontro el tipo de subsidiaria')
        return HttpResponseRedirect('/subsidiary_types')


def getSTInJson(request):
    s_types = {}
    s_types['s_types'] = []

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

    #subsidiaries['subsidiarias'] = serializers.serialize('json', Subsidiary.objects.all())

    return HttpResponse(simplejson.dumps(s_types))


def details(request, subsidiary_type_id):
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