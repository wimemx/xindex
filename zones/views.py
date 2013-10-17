from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.utils import simplejson
from django.http import Http404, HttpResponseRedirect, HttpResponse
from xindex.forms import ZoneForm
from xindex.models import Zone


def index(request):
    all_zones = Zone.objects.all().filter(active=True).order_by('-date')
    template_vars = {"zones": all_zones}
    request_context = RequestContext(request, template_vars)
    return render_to_response("zones/index.html", request_context)


def add(request):
    if request.method=='POST':
        formulario = ZoneForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect('/zones')
    else:
        formulario = ZoneForm()

    request_context = RequestContext(request)
    return render_to_response("zones/new_zone.html", {"title": "New Zone",
                                                      "formulario": formulario,
                                                      "Add": "Add",
                                                      "reset": "reset"},
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
