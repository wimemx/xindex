# Create your views here.
from django.shortcuts import render_to_response
from xindex.models import BusinessUnit, Subsidiary
from django.http import HttpResponseRedirect, HttpResponse
from django.template.context import RequestContext
from business_units.forms import AddBusinessUnit
from django.utils import simplejson


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
            template_vars = {
                "titulo": "Agregar unidad de negocio",
                "message": "",
                "formulario": formulario
            }
            request_context = RequestContext(request, template_vars)
            return render_to_response("business_units/add.html", request_context)
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
                template_vars = {
                    "titulo": "Modificar unidad de negocio",
                    "message": "",
                    "formulario": formulario
                }
                request_context = RequestContext(request, template_vars)
                return render_to_response("business_units/update.html", request_context)
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
        return HttpResponseRedirect('/business_units/')


def remove(request, business_unit_id):

    try:
        bus_unit = BusinessUnit.objects.get(id=business_unit_id)
    except BusinessUnit.DoesNotExist:
        bus_unit = False

    if bus_unit:
        try:
            bus_unit.active = False
            bus_unit.save()
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
        #return HttpResponse('No se pudo encontrar la unidad de negocio')
        return HttpResponseRedirect('/business_units')



def getBUInJson(request):
    b_u = {}
    b_u['business_u'] = []

    subsidiaries = Subsidiary.objects.filter(company__id=1,active=True)
    print subsidiaries
    for subsidiary in subsidiaries:
        for business_unit in subsidiary.business_unit.all():

            b_u['business_u'].append(
                {
                    "name": business_unit.name,
                    "subsidiary": subsidiary.name,
                    "zone": subsidiary.zone.name or '',
                    "business_unit_id": business_unit.id
                }
            )
    """
    print(subsidiaries)
    for bu in BusinessUnit.objects.filter(active=True).order_by('-date'):
        b_u['business_u'].append(
            {
                "name": bu.name,
                "description":bu.description,
                "bu_det": bu.id,
                "bu_up": bu.id,
                "bu_del": bu.id,
            }
        )
    """
    #subsidiaries['subsidiarias'] = serializers.serialize('json', Subsidiary.objects.all())

    return HttpResponse(simplejson.dumps(b_u))


def details(request, business_unit_id):
    template_vars = {
        'titulo': 'Detalles'
    }
    try:
        bus_u = BusinessUnit.objects.get(id=business_unit_id)

        bus_u = False if bus_u.active==False else bus_u
    except BusinessUnit.DoesNotExist:
        bus_u = False

    template_vars['bus_u'] = bus_u
    request_context = RequestContext(request, template_vars)
    return render_to_response('business_units/details.html', request_context)