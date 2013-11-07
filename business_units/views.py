# Create your views here.
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.template.context import RequestContext
from business_units.forms import AddBusinessUnit
from django.utils import simplejson
from xindex.models import BusinessUnit, Subsidiary, SubsidiaryBusinessUnit, Service, sbu_service


def index(request):
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

            newBusinessUnit = formulario.save()

            subSelected = request.POST.getlist('bu-sub')
            serSelected = request.POST.getlist('bu-ser')

            for eachSub in subSelected:
                subToAssign = Subsidiary.objects.get(pk=eachSub)
                alias = str(newBusinessUnit) + ', ' + str(subToAssign.name)

                bu_assignment = SubsidiaryBusinessUnit.objects.create(
                    id_subsidiary=subToAssign,
                    id_business_unit=newBusinessUnit,
                    alias=alias
                )

                bu_assignment.save()

                for eachService in serSelected:
                    serToAssign = Service.objects.get(pk=eachService)
                    alias = str(serToAssign.name) + ', ' \
                            + str(bu_assignment.alias)

                    service_assignment = sbu_service.objects.create(
                        id_subsidiaryBU=bu_assignment,
                        id_service=serToAssign,
                        alias=alias
                    )

                    service_assignment.save()

            return HttpResponseRedirect('/business_units/')
            #return HttpResponse('Si')
        else:

            template_vars = {
                "titulo": "Agregar unidad de negocio",
                "message": "",
                "formulario": formulario
            }
            request_context = RequestContext(request, template_vars)
            return HttpResponse('No')
    else:
        subsidiaries = Subsidiary.objects.filter(active=True)
        services = Service.objects.filter(active=True)

        formulario = AddBusinessUnit()
        template_vars = {
            "titulo": "Agregar unidad de negocio",
            "message": "",
            "formulario": formulario,
            "subsidiaries": subsidiaries,
            "services": services
        }
        request_context = RequestContext(request, template_vars)
        return render_to_response("business_units/add.html", request_context)


def update(request, business_unit_id):
    print str(request.method)
    try:
        bus_unit = BusinessUnit.objects.get(pk=business_unit_id)
    except BusinessUnit.DoesNotExist:
        bus_unit = False

    if bus_unit:
        if request.method == 'POST':
            print 'POST ENCONTRADO ____________________'
            formulario = AddBusinessUnit(request.POST or None,
                                         instance=bus_unit)
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
                    "formulario": formulario,
                    "business_unit_id": business_unit_id
                }
                request_context = RequestContext(request, template_vars)
                return render_to_response("business_units/update.html",
                                          request_context)
        else:
            print 'POST NO ENCONTRADO__________:x__________'
            print str(request.method)
            formulario = AddBusinessUnit(request.POST or None,
                                         instance=bus_unit)
            template_vars = {
                "titulo": "Modificar unidad de negocio",
                "message": "",
                "formulario": formulario,
                "business_unit_id": business_unit_id
            }
            request_context = RequestContext(request, template_vars)
            return render_to_response("business_units/update.html",
                                      request_context)
    else:
        message = "No se ha podido encontrar la unidad de negocio"
        return HttpResponseRedirect('/business_units/')


def remove(request, business_unit_id):

    try:
        business_unit = BusinessUnit.objects.get(pk=business_unit_id)
    except BusinessUnit.DoesNotExist:
        business_unit = False

    if business_unit:
        business_unit.active = False
        business_unit.save()
        return HttpResponse('Si')
    else:
        return HttpResponse('No')


def getBUInJson(request):
    b_u = {'business_u': []}

    business_unit = BusinessUnit.objects.filter(active=True)
    for eachBusinessUnit in business_unit:
        b_u['business_u'].append(
            {
                "name": eachBusinessUnit.name,
                "subsidiary": 'default',
                "zone": 'default',
                "business_unit_id": eachBusinessUnit.id,
                "subsidiary_id": 'default'
            }
        )

    return HttpResponse(simplejson.dumps(b_u))


def details(request, business_unit_id):
    template_vars = {'titulo': 'Detalles'}
    try:
        bus_u = BusinessUnit.objects.get(id=business_unit_id)

        bus_u = False if bus_u.active==False else bus_u
    except BusinessUnit.DoesNotExist:
        bus_u = False

    template_vars['bus_u'] = bus_u
    request_context = RequestContext(request, template_vars)
    return render_to_response('business_units/details.html', request_context)