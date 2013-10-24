# Create your views here.
from django.shortcuts import render_to_response
from xindex.models import Subsidiary
from django.http import HttpResponseRedirect, HttpResponse
from subsidiaries.forms import SubsidiaryForm, UpdateForm
from django.template.context import RequestContext
from django.core import serializers
from django.utils import simplejson
from xindex.models import Company, State, Zone, BusinessUnit


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

    business_units = BusinessUnit.objects.filter(subsidiary=subsidiary_id)

    services = {'services': []}
    for eachBusinessUnit in business_units:
        for eachService in eachBusinessUnit.service.all():
            services['services'].append({
                'service_name': eachService.name,
                'business_name': eachBusinessUnit.name
            })


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
                return HttpResponseRedirect('/subsidiaries/details/'+subsidiary_id)
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
        #return render_to_response("subsidiaries/index.html", request_context)
        return HttpResponseRedirect('/subsidiaries')


def getSubsidiariesInJson(request):
    subsidiaries = {}
    subsidiaries['subsidiarias'] = []

    for s in Subsidiary.objects.filter(active=True).order_by('-date'):
        print s.name
        subsidiaries['subsidiarias'].append(
            {
                "subsidiaryId": s.id,
                "subsidiaryIds": s.id,
                "name": s.name,
                "active": s.active,
                "detalles": s.id
            }
        )

    return HttpResponse(simplejson.dumps(subsidiaries))


def getSubsidiariesByCity(request):
    subsidiaries = {}
    subsidiaries['subsidiaries'] = []

    user = request.user.id

    companies = Company.objects.all()

    for c in companies:
        for u in c.staff.all():
            if user == u.user.id:
                company_id = c.id



    subsidiarias = Subsidiary.objects.filter(company_id=company_id)

    for subsidiary in subsidiarias:
        subsidiaries['subsidiaries'].append(
            {
                'id': subsidiary.id,
                'name': subsidiary.name,
                'city': subsidiary.city_id.name
            }
        )

    """
    for subsidiary in subsidiarias:
        for city in subsidiary.zone.cities.all():
            subsidiaries['subsidiaries'].append(
                {
                    'id': subsidiary.id,
                    'name': subsidiary.name,
                    'zone': subsidiary.zone.name,
                    'city': city.name
                }
            )
    """

    return HttpResponse(simplejson.dumps(subsidiaries))
