import json
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.utils import simplejson
from django.http import Http404, HttpResponseRedirect, HttpResponse
from rbacx.functions import has_permission
from rbacx.models import Operation
from xindex.forms import ZoneForm, StateListForm
from xindex.models import Zone, BusinessUnit, Country, State, City, \
    SubsidiaryBusinessUnit

#VIEW = "Ver"
#CREATE = "Crear"
#DELETE = "Eliminar"
#UPDATE = "Editar"

VIEW = Operation.objects.get(name="Ver")
CREATE = Operation.objects.get(name="Crear")
DELETE = Operation.objects.get(name="Eliminar")
UPDATE = Operation.objects.get(name="Editar")


def index(request):

    if has_permission(request.user, VIEW, "Ver zonas") or \
            request.user.is_superuser:

        zones = {'zones': []}
        all_zones = Zone.objects.all().filter(active=True).order_by('-date')

        for each_zone in all_zones:
            counter_states = 0
            states = {'states': []}
            counter_cities = 0
            cities = {'cities': []}
            counter_subsidiaries = 0
            subsidiaries = {'subsidiaries': []}

            for each_state in each_zone.states.all():
                counter_states += 1
                states['states'].append({
                    'name': each_state.name
                })

            for each_citie in each_zone.cities.all():
                counter_cities += 1
                cities['cities'].append({
                    'name': each_citie.name
                })

            for each_subsidiary in each_zone.subsidiary_set.all():
                counter_subsidiaries += 1
                subsidiaries['subsidiaries'].append({
                    'name': each_subsidiary.name
                })

            zones['zones'].append({
                'id': each_zone.id,
                'name': each_zone.name,
                'date': each_zone.date,
                'counter_states': counter_states,
                'states': states,
                'counter_cities': counter_cities,
                'cities': cities,
                'counter_subsidiaries': counter_subsidiaries,
                'subsidiaries': subsidiaries
            })

        template_vars = {"zones": zones}
        request_context = RequestContext(request, template_vars)
        return render_to_response("zones/index.html", request_context)
    else:
        template_vars = {}
        request_context = RequestContext(request, template_vars)
        return render_to_response("rbac/generic_error.html", request_context)


def add(request):

    if has_permission(request.user, CREATE, "Crear zonas") or \
            request.user.is_superuser:

        countries = Country.objects.filter(active=True)

        listform = StateListForm()
        listform.fields['countries'].choices = [(x.id, x) for x in
                                                Country.objects.filter(active=True)]

        states = request.POST.getlist('id_state')

        if request.POST:
            formulario = ZoneForm(request.POST or None)

            if formulario.is_valid():
                idZone = formulario.save()
                zoneAfterSave = Zone.objects.get(pk=idZone.id)

                countryToAdd = request.POST.getlist('id_country')

                for eachCountry in countryToAdd:
                    countrySelected = Country.objects.get(pk=eachCountry)
                    zoneAfterSave.countries.add(countrySelected)

                for eachState in states:
                    stateSelected = State.objects.get(pk=eachState)
                    zoneAfterSave.states.add(stateSelected)

                return HttpResponseRedirect('/zones')
            else:
                template_vars = {
                    "formulario": formulario
                }
                request_context = RequestContext(request, template_vars)
                return render_to_response("zones/new_zone.html", request_context)
        else:
            formulario = ZoneForm()
            request_context = RequestContext(request)
            return render_to_response("zones/new_zone.html",
                                      {"formulario": formulario,
                                       'countries': countries,
                                       'listform': listform},
                                      request_context)
    else:
        template_vars = {}
        request_context = RequestContext(request, template_vars)
        return render_to_response("rbac/generic_error.html", request_context)


def edit(request, zone_id):

    if has_permission(request.user, UPDATE, "Editar zonas") or \
            request.user.is_superuser:

        zona = Zone.objects.get(pk=zone_id)
        if request.method == 'POST':
            formulario = ZoneForm(request.POST, instance=zona)
            if formulario.is_valid():
                formulario.save()
                return HttpResponseRedirect('/zones/'+zone_id)
        else:
            formulario = ZoneForm(instance=zona)

        request_context = RequestContext(request)
        return render_to_response("zones/edit_zone.html",
                                  {"formulario": formulario,
                                   "zone_id": zone_id},
                                  request_context)
    else:
        template_vars = {}
        request_context = RequestContext(request, template_vars)
        return render_to_response("rbac/generic_error.html", request_context)


def remove(request, zone_id):

    if has_permission(request.user, DELETE, "Eliminar zonas") or \
            request.user.is_superuser:

        zone = Zone.objects.get(pk=zone_id)
        zone.active = False
        zone.save()
        return HttpResponse('Si')
    else:
        template_vars = {}
        request_context = RequestContext(request, template_vars)
        return render_to_response("rbac/generic_error.html", request_context)


def detail(request, zone_id):
    zones = {'zones': []}
    subsidiaries = {'subsidiaries': []}
    business_units = {'business_units': []}
    counter_business_units = 0

    business_units_all = BusinessUnit.objects.filter(active=True)
    try:
        zone = Zone.objects.get(pk=zone_id)
        status = str(zone.active)

        for each_subsidiary in zone.subsidiary_set.all():

            mySBU = SubsidiaryBusinessUnit.objects.filter(
                id_subsidiary__id=each_subsidiary.id)

            for each_business_unit in mySBU:
                counter_business_units += 1

            subsidiaries['subsidiaries'].append({
                'id': each_subsidiary.id,
                'name': each_subsidiary.name,
                'type': 'TIPO',
                'city': each_subsidiary.city_id.name,
                'state': each_subsidiary.state_id.name,
                'business_units': business_units,
                'counter_business_units': counter_business_units

            })
        zones['zones'].append({
            'id': zone.id,
            'name': zone.name,
            'description': zone.description,
            'date': zone.date,
            'subsidiaries': subsidiaries
        })

    except Zone.DoesNotExist:
        raise Http404

    request_context = RequestContext(request, {'zones': zones,
                                                'id': zone.id})
    return render_to_response("zones/detail.html", request_context)


def getZonesInJson(request):
    zonesToJson = {'zones': []}

    zonesObj = Zone.objects.filter(active=True)
    for eachZone in zonesObj:
        zonesToJson['zones'].append(
            {
                "name": eachZone.name,
                "someAttr": "someAttr",
                "zone_id": eachZone.id
            }
        )
    return HttpResponse(simplejson.dumps(zonesToJson))


def country(request, country_id):
    #state_list = State.objects.filter(country_id=country_id)
    states = State.objects.filter(active=True, country_id=country_id)
    state_list = []
    for state in states:
        if not state.zone_set.all():
            state_list.append(state)

    statesToJson = {'states': []}

    if state_list:
        for eachState in state_list:
            statesToJson['states'].append(
                {
                    "name": eachState.name,
                    "id": eachState.id
                }
            )

    return HttpResponse(simplejson.dumps(statesToJson))


def add_state(request, zone_id):
    zone = Zone.objects.get(pk=zone_id)

    if request.method == 'POST':
        states = request.POST.getlist('id_state')

        for eachState in states:
            stateSelected = State.objects.get(pk=eachState)

            zone.states.add(stateSelected)

        return HttpResponseRedirect('/zones/'+zone_id)
    else:
        for i in zone.countries.all():
            states = State.objects.filter(country_id=i)
            request_context = RequestContext(request)

            return render_to_response("zones/add_state.html",
                                      {"name": i.name,
                                       "id": i.id,
                                       'states': states,
                                       'id_zone': zone_id},
                                  request_context)


def get_subsidiaries(request):
    subsidiariesList = []
    if request.POST:
        if 'zone' in request.POST:
            #check if all zones are selected
            if request.POST['zone'] == 'all':
                subsidiariesList.append(
                    {
                        'subsidiary_id': 'all',
                        'subsidiary_name': 'Todas'
                    }
                )
                json_response = {
                    'answer': True,
                    'subsidiaries': subsidiariesList
                }
                return HttpResponse(json.dumps(json_response))
            else:
                try:
                    zone = Zone.objects.get(pk=int(request.POST['zone']))
                    subsidiaries = zone.subsidiary_set.all()
                    if len(subsidiaries) == 0:
                        json_response = {
                            'answer': False
                        }
                        return HttpResponse(json.dumps(json_response))
                    else:
                        for subsidiary in subsidiaries:
                            subsidiariesList.append(
                                {
                                    'subsidiary_id': subsidiary.id,
                                    'subsidiary_name': subsidiary.name

                                }
                            )
                        json_response = {
                            'answer': True,
                            'subsidiaries': subsidiariesList
                        }

                    return HttpResponse(json.dumps(json_response))
                except Zone.DoesNotExist:
                    pass
        else:
            pass