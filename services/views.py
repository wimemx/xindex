# Create your views here.
from django.shortcuts import render_to_response
import services
from xindex.models import Service
from django.http import HttpResponseRedirect, HttpResponse
from django.template.context import RequestContext
from services.forms import AddService
from django.utils import simplejson


def index(request, message = ''):
    all_services = Service.objects.all().order_by('-name')
    print all_services
    template_vars = {
        "titulo": "Servicios",
        "all_services": all_services
    }
    request_context = RequestContext(request, template_vars)
    return render_to_response("services/index.html", request_context)

def add(request):
    if request.POST:
        formulario = AddService(request.POST or None, request.FILES)
        if formulario.is_valid():
            formulario.save()
            template_vars = {
                "titulo": "Servicios",
                "message": "Se ha dado de alta el servicio",
                "formulario": formulario
            }
            request_context = RequestContext(request, template_vars)
            #return render_to_response("services/index.html", request_context)
            return HttpResponseRedirect('/services/')
        else:
            template_vars = {
                "titulo": "Agregar servicio",
                "message": "",
                "formulario": formulario
            }
            request_context = RequestContext(request, template_vars)
            return render_to_response("services/add.html", request_context)
    else:
        formulario = AddService()
        template_vars = {
            "titulo": "Agregar servicio",
            "message": "",
            "formulario": formulario
        }
        request_context = RequestContext(request, template_vars)
        return render_to_response("services/add.html", request_context)


def update(request, service_id):
    try:
        ser = Service.objects.get(id=service_id)
    except Service.DoesNotExist:
        ser = False

    if ser:
        if request.POST:
            formulario = AddService(request.POST or None, request.FILES, instance=ser)
            if formulario.is_valid():
                formulario.save()
                template_vars = {
                    "titulo": "Servicios",
                    "message": "Servicios"
                }
                request_context = RequestContext(request, template_vars)
                return HttpResponseRedirect('/services/')
            else:
                template_vars = {
                    "titulo": "Editar servicio",
                    "message": "",
                    "formulario": formulario
                }
                request_context = RequestContext(request, template_vars)
                return render_to_response("services/update.html", request_context)
        else:
            formulario = AddService(instance=ser)
            template_vars = {
                "titulo": "Editar servicio",
                "message": "",
                "formulario": formulario
            }
            request_context = RequestContext(request, template_vars)
            return render_to_response("services/update.html", request_context)
    else:
        message = "No se ha podido encontrar el servicio"
        #return HttpResponse(message+"%s." % service_id)
        return HttpResponseRedirect('/services/')


def remove(request, service_id):

    try:
        ser = Service.objects.get(id=service_id)
    except Service.DoesNotExist:
        ser = False

    if ser:
        try:
            ser.active = False
            ser.save()
            message="Se ha eliminado el servicio"
            template_vars = {
                "titulo": "Servicios",
                "message": "Se ha eliminado el servicio"
            }
            request_context = RequestContext(request, template_vars)
            #return render_to_response("services/index.html", request_context)
            return HttpResponseRedirect('/services/')

        except:
            message = "No se pudo eliminar"
            template_vars = {
                "titulo": "Servicios",
                "message": message
            }
            request_context = RequestContext(request, template_vars)
            #return render_to_response("services/index.html", request_context)
            return HttpResponseRedirect('/services/')
    else:
        message = "No se ha encontrado el servicio "
        template_vars = {
            "titulo": "Servicios",
            "message": message
        }
        request_context = RequestContext(request, template_vars)
        #return render_to_response("services/index.html", request_context)
        return HttpResponseRedirect('/services/')


def getSInJson(request):
    s = {}
    s['services'] = []

    for ser in Service.objects.filter(active=True).order_by('-date'):
        s['services'].append(
            {
                "name": ser.name,
                "description": ser.description,
                "s_det": ser.id,
                "s_up": ser.id,
                "s_del": ser.id
            }
        )

    #subsidiaries['subsidiarias'] = serializers.serialize('json', Subsidiary.objects.all())

    return HttpResponse(simplejson.dumps(s))


def details(request, service_id):
    template_vars = {
        'titulo': 'Detalles'
    }
    try:
        s = Service.objects.get(id=service_id)

        s = False if s.active==False else s
    except Service.DoesNotExist:
        s = False

    template_vars['service'] = s
    request_context = RequestContext(request, template_vars)
    return render_to_response('services/details.html', request_context)