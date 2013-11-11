# Create your views here.
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from xindex.models import Service, BusinessUnit, Subsidiary, Moment, sbu_service
from xindex.models import sbu_service_moment_attribute, SubsidiaryBusinessUnit, sbu_service_moment
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.template.context import RequestContext
from services.forms import AddService
from django.utils import simplejson
import json


@login_required(login_url='/signin/')
@login_required(login_url='/signin/')
def index(request, business_unit_id=False):
    global service_list
    if business_unit_id:
        try:
            business_unit = BusinessUnit.objects.get(pk=business_unit_id)
            service_list = sbu_service.objects.filter(
                id_subsidiaryBU__id_business_unit=business_unit_id)
        except BusinessUnit.DoesNotExist:
            business_unit = False
            service_list = False
    else:
        business_unit = False

    services = {'services': [],
                'business_units': []}

    myServiceList = []
    mySubsidiaryList = []

    for eachAssignment in service_list:

        myServiceList.append(eachAssignment.id_service.id)
        myServiceList = list(set(myServiceList))

        mySubsidiaryList.append(eachAssignment.id_subsidiaryBU.id)
        mySubsidiaryList = list(set(mySubsidiaryList))

    for eachSubsidiaryBusinessUnit in mySubsidiaryList:

        mySubsidiaryBusinessUnit = SubsidiaryBusinessUnit.objects.get(
            pk=eachSubsidiaryBusinessUnit
        )

        mySubsidiary = Subsidiary.objects.get(
            pk=mySubsidiaryBusinessUnit.id_subsidiary.id
        )

        services['business_units'].append(
            {
                "name": mySubsidiary.name,
                "type": mySubsidiary.subsidiary_types.name,
                "zone": mySubsidiary.zone.name,
                "location": mySubsidiary.city_id.name,
                "id": mySubsidiary.id,
            }
        )

    for eachService in myServiceList:

        myServices = Service.objects.get(pk=eachService)
        myMoments = sbu_service_moment.objects.filter(
            id_sbu_service__id_service__id=myServices.id
        )

        #Counters!
        myMomentCounter = []
        myAttributeCounter = []
        for eachMoment in myMoments:
            myMomentCounter.append(eachMoment.id_moment.id)

        myMomentCounter = list(set(myMomentCounter))

        touch_count = 0
        indicator_count = 0
        for eachSetMoment in myMomentCounter:
            touch_count += 1

            myAtributtes = sbu_service_moment_attribute.objects.filter(
                id_sbu_service_moment__id_moment__id=eachSetMoment
            )

            print '========== C O N S U L T A ==========='
            print myAtributtes

            for eachAttribute in myAtributtes:
                print '====================='
                print eachAttribute.alias
                indicator_count += 1



        services['services'].append(
            {
                "name": myServices.name,
                "id": myServices.id,
                "indicator_counter": indicator_count,
                "touchPoint_counter": touch_count
            }
        )

    template_vars = {
        "titulo": "Servicios",
        "all_services": services,
        "business_unit": business_unit,
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

            allSubdidiaryBU = SubsidiaryBusinessUnit.objects.filter(
                id_business_unit=business_unit_id
            )

            for eachSubsidiaryBU in allSubdidiaryBU:

                alias = str(formToSave.name) \
                        + ', ' \
                        + str(eachSubsidiaryBU.alias)

                newSBU_service = sbu_service.objects.create(
                    id_subsidiaryBU=eachSubsidiaryBU,
                    id_service=formToSave,
                    alias=alias
                )
                newSBU_service.save()

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

    print '==ENTRA=='

    try:
        service = Service.objects.get(id=service_id)
    except Service.DoesNotExist:
        service = False

    if service:
        print '==SERVICE=='
        print '==REQUEST=='
        print request
        if request.POST:
            print '==POST=='
            formulario = AddService(request.POST or None, request.FILES,
                                    instance=service)
            if formulario.is_valid():
                formulario.save()
                template_vars = {
                    "titulo": "Servicios",
                    "message": "Servicios"
                }
                request_context = RequestContext(request, template_vars)
                return HttpResponseRedirect('/services/'+ business_unit_id)
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
                "formulario": formulario,
                "service_id": service_id
            }
            request_context = RequestContext(request, template_vars)
            return render_to_response("services/update.html", request_context)
    else:
        message = "No se ha podido encontrar el servicio"
        #return HttpResponse(message+"%s." % service_id)
        return HttpResponseRedirect('/services/'+ business_unit_id)


@login_required(login_url='/signin/')
def remove(request, service_id, business_unit_id):
    try:
        mySbuService = sbu_service.objects.filter(
            id_subsidiaryBU__id_business_unit__id=business_unit_id,
            id_service__id=service_id
        )

        for each_serviceRelation in mySbuService:
            each_serviceRelation.delete()

        message = "Se ha eliminado el servicio"
        template_vars = {
            "titulo": "Servicios",
            "message": "Se ha eliminado el servicio"
        }
        request_context = RequestContext(request, template_vars)
        #return render_to_response("services/index.html", request_context)
        return HttpResponseRedirect('/services/' + str(business_unit_id))

    except:
        message = "No se pudo eliminar"
        template_vars = {
            "titulo": "Servicios",
            "message": message
        }
        request_context = RequestContext(request, template_vars)
        #return render_to_response("services/index.html", request_context)
        return HttpResponseRedirect('/services/' + str(business_unit_id))



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
def details(request, service_id):
    try:
        all_sbuServiceMoment = sbu_service_moment.objects.filter(
            id_sbu_service__id_service=service_id
        )
        status = 'STATUS'
    except Service.DoesNotExist:
        raise Http404

    momentsInService = {'moments': []}
    myMomentList = []

    for eachSbuServiceMoment in all_sbuServiceMoment:
        myMomentList.append(eachSbuServiceMoment.id_moment.id)

    myMomentList = list(set(myMomentList))

    for eachMoment in myMomentList:
        myMoment = Moment.objects.get(pk=eachMoment)
        momentsInService['moments'].append(
            {
                "id": myMoment.id,
                "name": myMoment.name,
                "description": myMoment.description
            }
        )

    '''
    counter_moments = 0
    for a in moments.moments.all():
        counter_moments += 1

    counter_attributes_ = 0
    for each_moment in moments.moments.all():
        each_moment_to_compare = Moment.objects.get(pk=each_moment.id)
        for attribute in each_moment_to_compare.attributes.all():
            counter_attributes_ += 1
    '''
    template_vars = {
        'titulo': 'Detalles',
        'service': momentsInService,
        'service_id': service_id,
        'counter_moments': 'counter_moments',
        'counter_attributes': 'counter_attributes_',
        'business_unit': 'business_unit'
    }
    request_context = RequestContext(request, template_vars)
    return render_to_response('services/details.html', request_context)


def get_moments(request):
    service_id = int(request.POST['select_service'])
    try:
        all_sbuServiceMoment = sbu_service_moment.objects.filter(
            id_sbu_service__id_service=service_id
        )
    except Service.DoesNotExist:
        raise Http404

    momentsInService = []
    myMomentList = []

    for eachSbuServiceMoment in all_sbuServiceMoment:
        myMomentList.append(eachSbuServiceMoment.id_moment.id)

    myMomentList = list(set(myMomentList))

    for eachMoment in myMomentList:
        myMoment = Moment.objects.get(pk=eachMoment)
        if myMoment.active:
            momentsInService.append(
                {
                    "moment_id": myMoment.id,
                    "moment_name": myMoment.name
                }
            )

    json_response = json.dumps(
        {
            'answer': True,
            'moments': momentsInService
        }
    )

    return HttpResponse(json_response, content_type="application/json")


def get_services(request):
    businessUnit_id = int(request.POST['select_businessUnit'])
    try:
        all_sbuService = sbu_service.objects.filter(
            id_subsidiaryBU__id_business_unit=businessUnit_id
        )
    except BusinessUnit.DoesNotExist:
        raise Http404

    servicesInBU = []
    myServiceList = []

    momentsInService = []
    myMomentList = []

    for eachSbuService in all_sbuService:
        myServiceList.append(eachSbuService.id_service.id)

    myServiceList = list(set(myServiceList))
    myMomentList = list(set(myMomentList))

    for eachService in myServiceList:
        myService = Service.objects.get(pk=eachService)
        if myService.active:
            servicesInBU.append(
                {
                    'service_id': myService.id,
                    'service_name': myService.name
                }
            )

    '''
    for eachMoment in myMomentList:
        myMoment = Moment.objects.get(pk=eachMoment)
        if myMoment.active:
            momentsInService.append(
                {
                    "moment_id": myMoment.id,
                    "moment_name": myMoment.name
                }
            )
    '''
    json_response = json.dumps(
        {
            'answer': True,
            'services': servicesInBU
        }
    )

    return HttpResponse(json_response, content_type="application/json")