# Create your views here.
from django.shortcuts import render_to_response
import services
from xindex.models import Service
from django.http import HttpResponseRedirect, HttpResponse
from django.template.context import RequestContext
from services.forms import AddService


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
            return HttpResponse("El formulario no es valido %s.")
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
            ser.delete()
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


