# Create your views here.
from django.shortcuts import render_to_response
from xindex.models import BusinessUnit
from django.http import HttpResponseRedirect, HttpResponse
from django.template.context import RequestContext
from business_units.forms import AddBusinessUnit


def index(request, message = ''):
    all_business_units = BusinessUnit.objects.all().order_by('-name')
    template_vars = {
        "titulo": "Unidades de negocio",
        "all_business_units": all_business_units
    }
    request_context = RequestContext(request, template_vars)
    return render_to_response("business_units/index.html", request_context)

def add(request):
    if request.POST:
        formulario = AddBusinessUnit(request.POST or None)
        if formulario.is_valid():
            formulario.save()
            template_vars = {
                "titulo": "Agregar unidad de negocio",
                "message": "Se ha dado de alta la unidad de negocio",
                "formulario": formulario
            }
            request_context = RequestContext(request, template_vars)
            #return render_to_response("business_units/index.html", request_context)
            return HttpResponseRedirect('/business_units')
        else:
            return HttpResponse("El formulario no es valido %s.")
    else:
        formulario = AddBusinessUnit()
        template_vars = {
            "titulo": "Agregar unidad de negocio",
            "message": "",
            "formulario": formulario
        }
        request_context = RequestContext(request, template_vars)
        return render_to_response("business_units/add.html", request_context)


def update(request, business_unit_id):
    try:
        bus_unit = BusinessUnit.objects.get(id=business_unit_id)
    except BusinessUnit.DoesNotExist:
        bus_unit = False

    if bus_unit:
        if request.POST:
            formulario = AddBusinessUnit(request.POST or None, instance=bus_unit)
            if formulario.is_valid():
                formulario.save()
                template_vars = {
                    "titulo": "Unidades de negocio",
                    "message": "Se ha modificado la unidad de negocio"
                }
                request_context = RequestContext(request, template_vars)
                return HttpResponseRedirect('/business_units/')
            else:
                return HttpResponse('El formulario no es valido')
        else:
            formulario = AddBusinessUnit(request.POST or None, instance=bus_unit)
            template_vars = {
                "titulo": "Modificar unidad de negocio",
                "message": "",
                "formulario": formulario
            }
            request_context = RequestContext(request, template_vars)
            return render_to_response("business_units/update.html", request_context)
    else:
        message = "No se ha podido encontrar la unidad de negocio"
        return HttpResponse(message+"%s." % business_unit_id)


def remove(request, business_unit_id):

    try:
        bus_unit = BusinessUnit.objects.get(id=business_unit_id)
    except BusinessUnit.DoesNotExist:
        bus_unit = False

    if bus_unit:
        try:
            bus_unit.delete()
            message="Se ha eliminado la unidad de negocio"
            template_vars = {
                "titulo": "Unidades de negocio",
                "message": message
            }
            request_context = RequestContext(request, template_vars)
            #return render_to_response("business_units/index.html", request_context)
            return HttpResponseRedirect('/business_units')

        except:
            message = "No se pudo eliminar la unidad de negocio"
            template_vars = {
                "titulo": "Unidades de negocio",
                "message": message
            }
            request_context = RequestContext(request, template_vars)
            #return render_to_response("business_units/index.html", request_context)
            return HttpResponse('No se pudo eliminar la unidad de negocio')
    else:
        message = "No se ha encontrado la unidad de negocio"
        template_vars = {
            "titulo": "Unidades de negocio",
            "message": message
        }
        request_context = RequestContext(request, template_vars)
        #return render_to_response("business_units/index.html", request_context)
        return HttpResponse('No se pudo encontrar la unidad de negocio')
