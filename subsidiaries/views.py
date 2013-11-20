import json
from django.shortcuts import render_to_response
from xindex.models import Subsidiary
from django.http import HttpResponseRedirect, HttpResponse
from subsidiaries.forms import SubsidiaryForm
from django.template.context import RequestContext
from django.utils import simplejson
from xindex.models import State, Zone, BusinessUnit
from xindex.models import SubsidiaryBusinessUnit, sbu_service


def index(request, message=''):
    all_subsidiaries = Subsidiary.objects.filter(active='True')
    return render_to_response(
        'subsidiaries/index.html',
        {
            'all_subsidiaries': all_subsidiaries,
            'message': message
        }
    )


def details(request, subsidiary_id):

    business_units = SubsidiaryBusinessUnit.objects.filter(
        id_subsidiary__id=subsidiary_id
    )

    myBusinessUnitList = []
    myServiceList = []
    for eachBusinessUnit in business_units:
        myBusinessUnitList.append(eachBusinessUnit.id_business_unit.id)

    myBusinessUnitList = list(set(myBusinessUnitList))

    for eachSetBusinessUnit in myBusinessUnitList:
        myBusinessUnit = BusinessUnit.objects.get(pk=eachSetBusinessUnit)

        mySBUSS = sbu_service.objects.filter(
            id_subsidiaryBU__id_subsidiary__id=subsidiary_id
        )

        services = {'services': []}
        for eachSBUS in mySBUSS:
            myServiceList.append(eachSBUS.id_service.id)
            services['services'].append({
                'service_name': eachSBUS.id_service.name,
                'business_name': eachSBUS.id_subsidiaryBU.id_business_unit.name
            })

        myServiceList = list(set(myServiceList))


    template_vars = {
        'titulo': 'Detalles'
    }
    try:
        sub = Subsidiary.objects.get(id=subsidiary_id)

        sub = False if sub.active == False else sub
    except Subsidiary.DoesNotExist:
        sub = False

    template_vars['sub'] = sub
    template_vars['business_units'] = business_units
    template_vars['services'] = services
    request_context = RequestContext(request, template_vars)
    return render_to_response('subsidiaries/details.html', request_context)


def add(request):
    if request.POST:
        formulario = SubsidiaryForm(request.POST or None)
        if formulario.is_valid():
            print "Formulario valido"
            form = formulario.save()

            state = State.objects.get(pk=request.POST['state_id'])
            zones = Zone.objects.filter(active=True)

            for eachZone in zones:
                for eachState in eachZone.states.all():
                    if eachState == state:
                        form.zone = eachZone
                        form.save()

            template_vars = {
                "titulo": "Subsidiarias",
                "message": "Se ha dado de alta la subsidiaria",
                "formulario": formulario
            }
            request_context = RequestContext(request, template_vars)
            return HttpResponseRedirect('/subsidiaries')
        else:

            template_vars = {
                "titulo": "Agregar subsidiaria",
                "message": "",
                "formulario": formulario
            }
            request_context = RequestContext(request, template_vars)
            return render_to_response("subsidiaries/add.html", request_context)
    else:
        formulario = SubsidiaryForm()
        template_vars = {
            "titulo": "Agregar subsidiaria",
            "message": "",
            "formulario": formulario
        }
        request_context = RequestContext(request, template_vars)
        return render_to_response("subsidiaries/add.html", request_context)


def edit(request, subsidiary_id):
    try:
        sub = Subsidiary.objects.get(id=subsidiary_id)
    except Subsidiary.DoesNotExist:
        sub = False

    if sub:
        #formulario = UpdateForm(initial=
        # {'id': sub.id,'name': sub.name, 'business_unit': [1,2]})

        if request.POST:
            formulario = SubsidiaryForm(request.POST or None, instance=sub)
            if formulario.is_valid():
                formulario.save()
                template_vars = {
                    "titulo": "Subsidiarias",
                    "message": "Se ha modificado la subsidiaria"
                }
                request_context = RequestContext(request, template_vars)
                return HttpResponseRedirect('/subsidiaries/details/' +
                                            subsidiary_id)
            else:
                template_vars = {
                    "titulo": "Editar subsidiaria",
                    "message": "",
                    "formulario": formulario
                }
                request_context = RequestContext(request, template_vars)
                return render_to_response("subsidiaries/update.html",
                                          request_context)
        else:
            formulario = SubsidiaryForm(request.POST or None, instance=sub)
            template_vars = {
                "titulo": "Editar subsidiaria",
                "message": "",
                "formulario": formulario,
                "subsidiary_id": subsidiary_id
            }
            request_context = RequestContext(request, template_vars)
            return render_to_response("subsidiaries/update.html",
                                      request_context)
    else:
        message = "No se ha podido encontrar la subsidiaria"
        return HttpResponseRedirect('/subsidiaries/')


def remove(request, subsidiary_id):
    try:
        sub = Subsidiary.objects.get(id=subsidiary_id)
    except Subsidiary.DoesNotExist:
        sub = False

    if sub:
        try:
            businessUnit = BusinessUnit.objects.filter(subsidiary=sub)

            for eachBusinessUnit in businessUnit:
                eachBusinessUnit.active = False
                eachBusinessUnit.save()

            sub.active = False
            sub.save()
            template_vars = {
                "titulo": "Subsidiarias",
                "message": "Se ha eliminado la subsidiaria"
            }
            request_context = RequestContext(request, template_vars)
            return HttpResponse('Si')

        except:
            message = "No se pudo eliminar"
            template_vars = {
                "titulo": "Subsidiarias",
                "message": message
            }
            request_context = RequestContext(request, template_vars)
            return HttpResponse('No se ha podido eliminar la subsidiaria')
    else:
        message = "No se ha encontrado la subsidiaria "
        template_vars = {
            "titulo": "Subsidiarias",
            "message": message
        }
        request_context = RequestContext(request, template_vars)
        return HttpResponseRedirect('/subsidiaries')


def getSubsidiariesInJson(request):
    subsidiaries = {'subsidiaries': []}

    for s in Subsidiary.objects.filter(active=True).order_by('-date'):
        subsidiaries['subsidiaries'].append(
            {
                "subsidiaryId": s.id,
                "name": s.name or 'subsidiaryName',
                "type": s.subsidiary_types.name or 'typeName',
                "zone": s.zone.name or 'zoneName',
                "location": s.state_id.name
            }
        )

    return HttpResponse(simplejson.dumps(subsidiaries))


def getSubsidiaryDetailsInJson(request, subsidiary_id):

    mySBUSS = sbu_service.objects.filter(
        id_subsidiaryBU__id_subsidiary__id=subsidiary_id
    )

    services = {'services': []}
    for eachSBUS in mySBUSS:
        services['services'].append({
            'service_name': eachSBUS.id_service.name,
            'business_name': eachSBUS.id_subsidiaryBU.id_business_unit.name
        })

    return HttpResponse(simplejson.dumps(services))


def get_business_units(request):
    businessUnitsList = []
    if request.POST:
        if 'zone' in request.POST and 'subsidiary' in request.POST:
            try:
                zone = Zone.objects.get(pk=int(request.POST['zone']))
                subsidiary = zone.subsidiary_set.get(
                    pk=int(request.POST['subsidiary']))
                for subsidiary_business_unit in SubsidiaryBusinessUnit.objects.filter(
                        id_subsidiary=subsidiary):
                    businessUnitsList.append(
                        {
                            'business_unit_id': subsidiary_business_unit.id_business_unit.id,
                            'business_unit_name': subsidiary_business_unit.id_business_unit.name + ' - ' + subsidiary_business_unit.alias
                        }
                    )
                if len(businessUnitsList) == 0:
                    pass
                else:
                    json_response = {
                        'answer': True,
                        'business_units': businessUnitsList
                    }
                    return HttpResponse(json.dumps(json_response))
            except Zone.DoesNotExist:
                pass
        else:
            pass
