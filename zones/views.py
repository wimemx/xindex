from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.utils import simplejson
from django.http import Http404, HttpResponseRedirect, HttpResponse
from xindex.forms import ZoneForm
from xindex.models import Zone


def index(request):
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


def add(request):
    if request.POST:
        formulario = ZoneForm(request.POST or None)
        if formulario.is_valid():
            formulario.save()
            if formulario.save():
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
        return render_to_response("zones/new_zone.html", {"formulario": formulario},
                                  request_context)


def edit(request, zone_id):
    #return HttpResponse("You're editing zone %s." % zone_id)
    zona = Zone.objects.get(pk=zone_id)
    if request.method=='POST':
        formulario = ZoneForm(request.POST, instance=zona)
        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect('/zones')
    else:
        formulario = ZoneForm(instance=zona)

    request_context = RequestContext(request)
    return render_to_response("zones/new_zone.html",
                              {"formulario": formulario,
                               "Add": "Save",
                               "reset": "button",
                               "onclick": "javascript:history.go(-1)"},
                              request_context)


def remove(request, zone_id):
    zone = Zone.objects.get(pk=zone_id)
    #zone.delete()
    zone.active = False
    zone.save()
    return HttpResponseRedirect('/zones')


def detail(request, zone_id):
    try:
        zone = Zone.objects.get(pk=zone_id)
        status = str(zone.active)
    except Zone.DoesNotExist:
        raise Http404
    return render_to_response('zones/detail.html',
                              {'zone': zone, 'status': status})


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
