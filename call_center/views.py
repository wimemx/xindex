import simplejson
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from xindex.models import Company, Zone, Subsidiary, SubsidiaryBusinessUnit, \
    sbu_service, BusinessUnit, Service, Survey


@login_required(login_url='/signin/')
def index(request):
    companies = Company.objects.filter(active=True)[:1]
    zones = Zone.objects.filter(active=True)
    subsidiaries = Subsidiary.objects.filter(zone=zones[0], active=True)
    businessUnits = SubsidiaryBusinessUnit.objects.filter(
        id_subsidiary__id=subsidiaries[0].id)

    try:
        sbu_services = sbu_service.objects.filter(
            id_subsidiaryBU__id_subsidiary__id=businessUnits[0].id_subsidiary.id
        )
    except:
        sbu_services = "Sin servicios"
    template_vars = {'companies': companies,
                     'zones': zones,
                     'zone': zones[0],
                     'subsidiaries': subsidiaries,
                     'businessUnits': businessUnits,
                     'sbu_services': sbu_services}
    request_context = RequestContext(request, template_vars)
    return render_to_response("call_center/index.html", request_context)


@login_required(login_url='/signin/')
def getZonesInJson(request, zone_id):
    subsidiary_list = Subsidiary.objects.filter(zone=zone_id, active=True)

    if subsidiary_list.count() == 0:
        print "CERO"
    else:

        subsidiariesToJson = {'subsidiaries': [],
                              'business': [],
                              'services': []}

        if subsidiary_list:
            counter = 0
            for eachSubsidiary in subsidiary_list:
                subsidiariesToJson['subsidiaries'].append(
                    {
                        "name": eachSubsidiary.name,
                        "id": eachSubsidiary.id
                    }
                )

            sBusinessUnits = SubsidiaryBusinessUnit.objects.filter(
                id_subsidiary=subsidiary_list[0].id
            )

            for eachSBU in sBusinessUnits:
                businessUnits = BusinessUnit.objects.get(
                    pk=eachSBU.id_business_unit.id,
                    active=True
                )
                subsidiariesToJson['business'].append(
                    {
                        "name": businessUnits.name,
                        "id": businessUnits.id
                    }
                )

                sbuService = sbu_service.objects.filter(
                    id_subsidiaryBU__id_business_unit=businessUnits.id
                )

                if counter == 0:
                    counter += 1
                    for eachService in sbuService:
                        services = Service.objects.get(
                            pk=eachService.id_service.id,
                            active=True
                        )

                        subsidiariesToJson['services'].append(
                            {
                                "name": services.name,
                                "id": services.id
                            }
                        )

        return HttpResponse(simplejson.dumps(subsidiariesToJson))


@login_required(login_url='/signin/')
def getBusinessInJson(request, subsidiary_id):
    subsidiary_list = Subsidiary.objects.get(pk=subsidiary_id, active=True)

    if subsidiary_list:

        businessToJson = {'business': [],
                              'services': []}

        if subsidiary_list:
            counter = 0

            sBusinessUnits = SubsidiaryBusinessUnit.objects.filter(
                id_subsidiary=subsidiary_list.id
            )

            for eachSBU in sBusinessUnits:
                businessUnits = BusinessUnit.objects.get(
                    pk=eachSBU.id_business_unit.id,
                    active=True
                )
                businessToJson['business'].append(
                    {
                        "name": businessUnits.name,
                        "id": businessUnits.id
                    }
                )

                sbuService = sbu_service.objects.filter(
                    id_subsidiaryBU__id_business_unit=businessUnits.id
                )

                if counter == 0:
                    counter += 1
                    for eachService in sbuService:
                        services = Service.objects.get(
                            pk=eachService.id_service.id,
                            active=True
                        )

                        businessToJson['services'].append(
                            {
                                "name": services.name,
                                "id": services.id
                            }
                        )

        return HttpResponse(simplejson.dumps(businessToJson))


@login_required(login_url='/signin/')
def getServicesInJson(request, business_id):

    servicesToJson = {'services': []}

    sbuService = sbu_service.objects.filter(
        id_subsidiaryBU__id_business_unit=business_id
    )

    if sbuService:
        myS = []
        for eachService in sbuService:
            services = Service.objects.get(
                pk=eachService.id_service.id,
                active=True
            )

            #myS.append(services)
            #myS = list(set(myS))
            """
            Se repiten los servicios al agregar los clientes
            """

            servicesToJson['services'].append(
                {
                    "name": services.name,
                    "id": services.id
                }
            )

    return HttpResponse(simplejson.dumps(servicesToJson))


@login_required(login_url='/signin/')
def getSurveyInJson(request, business_id, service_id):

    surveyToJson = {'survey': []}

    mySurvey = Survey.objects.filter(
        business_unit_id=business_id,
        service_id=service_id)[0]

    if mySurvey:
        surveyToJson['survey'].append(
            {
                "name": mySurvey.name,
                "id": mySurvey.id
            }
        )
    return HttpResponse(simplejson.dumps(surveyToJson))