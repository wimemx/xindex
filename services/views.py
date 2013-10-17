# Create your views here.
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
import services
from xindex.models import Service, BusinessUnit, Subsidiary, Moment
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.template.context import RequestContext
from services.forms import AddService
from django.utils import simplejson


@login_required(login_url='/signin/')
def index(request, business_unit_id=False):
    if business_unit_id:
        try:
            business_unit = BusinessUnit.objects.get(pk=business_unit_id)
        except BusinessUnit.DoesNotExist:
            business_unit = False
    else:
        business_unit = False

    if business_unit:
        company = business_unit.subsidiary
    else:
        subsidiaries = False
        company = False

    all_services = Service.objects.all().order_by('-name')
    print all_services
    template_vars = {
        "titulo": "Servicios",
        "all_services": all_services,
        "business_unit": business_unit,
        "company": company
    }
    request_context = RequestContext(request, template_vars)
    return render_to_response("services/index.html", request_context)


@login_required(login_url='/signin/')
def add(request, business_unit_id):
    business_unit = BusinessUnit.objects.get(pk=business_unit_id)
    if request.POST:
        formulario = AddService(request.POST or None)
        if formulario.is_valid():
            formToSave = formulario.save()
            business_unit.service.add(formToSave)
            business_unit.save()
            template_vars = {
                "titulo": "Servicios",
                "message": "Se ha dado de alta el servicio",
                "formulario": formulario
            }
            request_context = RequestContext(request, template_vars)
            #return render_to_response("services/index.html", request_context)
            return HttpResponseRedirect('/services/'+str(business_unit_id))
        else:
            template_vars = {
                "titulo": "Agregar servicio",
                "message": "",
                "formulario": formulario,
                "buid": business_unit_id
            }
            request_context = RequestContext(request, template_vars)
            return render_to_response("services/add.html", request_context)
    else:
        formulario = AddService()
        template_vars = {
            "titulo": "Agregar servicio",
            "message": "",
            "formulario": formulario,
            "buid": business_unit_id
        }
        request_context = RequestContext(request, template_vars)
        return render_to_response("services/add.html", request_context)


@login_required(login_url='/signin/')
def update(request, service_id, business_unit_id):
    try:
        service = Service.objects.get(id=service_id)
    except Service.DoesNotExist:
        service = False

    if service:
        if request.POST:
            formulario = AddService(request.POST or None, request.FILES,
                                    instance=service)
            if formulario.is_valid():
                formulario.save()
                template_vars = {
                    "titulo": "Servicios",
                    "message": "Servicios"
                }
                request_context = RequestContext(request, template_vars)
                return HttpResponseRedirect('/services/'+business_unit_id)
            else:
                template_vars = {
                    "titulo": "Editar servicio",
                    "message": "",
                    "formulario": formulario
                }
                request_context = RequestContext(request, template_vars)
                return render_to_response("services/update.html",
                                          request_context)
        else:
            formulario = AddService(instance=service)
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
        return HttpResponseRedirect('/services/'+business_unit_id)


@login_required(login_url='/signin/')
def remove(request, service_id, business_unit_id):
    try:
        service = Service.objects.get(pk=service_id)
        business_unit = BusinessUnit.objects.get(pk=business_unit_id)
    except Service.DoesNotExist:
        service = False

    try:
        business_unit = BusinessUnit.objects.get(pk=business_unit_id)
    except BusinessUnit.DoesNotExist:
        business_unit = False

    if service and business_unit:
        try:
            business_unit.service.remove(service)
            business_unit.save()
            service.active = False
            service.save()
            message = "Se ha eliminado el servicio"
            template_vars = {
                "titulo": "Servicios",
                "message": "Se ha eliminado el servicio"
            }
            request_context = RequestContext(request, template_vars)
            #return render_to_response("services/index.html", request_context)
            return HttpResponseRedirect('/services/'+str(business_unit_id))

        except:
            message = "No se pudo eliminar"
            template_vars = {
                "titulo": "Servicios",
                "message": message
            }
            request_context = RequestContext(request, template_vars)
            #return render_to_response("services/index.html", request_context)
            return HttpResponseRedirect('/services/'+str(business_unit_id))
    else:
        message = "No se ha encontrado el servicio "
        template_vars = {
            "titulo": "Servicios",
            "message": message
        }
        request_context = RequestContext(request, template_vars)
        #return render_to_response("services/index.html", request_context)
        return HttpResponseRedirect('/services/'+str(business_unit_id))


@login_required(login_url='/signin/')
def getSInJson(request):
    service = {}
    service['services'] = []
    service_query = Service.objects.filter(active=True).order_by('-date')
    business_unit_query = BusinessUnit.objects.filter(active=True)

    for each_service in service_query:
        service['services'].append(
            {
                "name": each_service.name,
                "business_unit": "Unidad de servicio",
                "subsidiary": "Sucursal",
                "zone": "Ubicacion",
                "delete": each_service.id,
                "edit": each_service.id,
                "details": each_service.id
            }
        )

    return HttpResponse(simplejson.dumps(service))


@login_required(login_url='/signin/')
def getSByBUInJson(request, business_unit_id):
    business_unit = BusinessUnit.objects.get(pk=business_unit_id)

    services = {'services': []}
    service_query = Service.objects.filter(active=True).order_by('-date')
    business_unit_query = BusinessUnit.objects.filter(active=True)

    for service in business_unit.service.all():
        if service.active == True:
            services['services'].append(
                {
                    "name": service.name,
                    "business_unit": business_unit.name,
                    "business_unit_id": business_unit.id,
                    "subsidiary": business_unit.subsidiary.name,
                    "subsidiary_id": business_unit.subsidiary.id,
                    "zone": business_unit.subsidiary.address,
                    "delete": service.id,
                    "edit": service.id,
                    "details": service.id
                }
            )

        #subsidiaries['subsidiarias'] = serializers.serialize('json', Subsidiary.objects.all())

    return HttpResponse(simplejson.dumps(services))


'''
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
'''


@login_required(login_url='/signin/')
def details(request, service_id, business_unit_id):
    try:
        moments = Service.objects.get(pk=service_id)
        business_unit = BusinessUnit.objects.get(pk=business_unit_id)
        status = str(moments.active)
    except Service.DoesNotExist:
        raise Http404

    counter_moments = 0
    for a in moments.moments.all():
        counter_moments += 1

    counter_attributes_ = 0
    for each_moment in moments.moments.all():
        each_moment_to_compare = Moment.objects.get(pk=each_moment.id)
        for attribute in each_moment_to_compare.attributes.all():
            counter_attributes_ += 1

    template_vars = {
        'titulo': 'Detalles',
        'service': moments,
        'service_id': service_id,
        'counter_moments': counter_moments,
        'counter_attributes': counter_attributes_,
        'business_unit': business_unit
    }
    request_context = RequestContext(request, template_vars)
    return render_to_response('services/details.html', request_context)