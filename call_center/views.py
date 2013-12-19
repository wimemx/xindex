import simplejson
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from random import sample
import short_url
from call_center.functions import randomClient
from xindex.models import Company, Zone, Subsidiary, SubsidiaryBusinessUnit, \
    sbu_service, BusinessUnit, Service, Survey, Client, ClientActivity


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


@login_required(login_url='/signin/')
def getClient(request, business_id, service_id):

    clientToJson = {'client': []}
    myClientActivity = randomClient(business_id, service_id)

    a_id_and_c_id = str(myClientActivity.id)+str(myClientActivity.client.id)
    activity_code = short_url.encode_url(int(a_id_and_c_id))

    url = "http://xindex.wimjapps.com/surveys/answer/"\
          + str(short_url.encode_url(myClientActivity.survey.id))\
          + "/"\
          + str(activity_code)\
          + "/"\
          + str(short_url.encode_url(myClientActivity.client.id))

    if myClientActivity:
        clientToJson['client'].append({
            "first_name": myClientActivity.client.first_name,
            "last_name": myClientActivity.client.last_name,
            "phone": myClientActivity.client.phone,
            "email": myClientActivity.client.email,
            "survey": url
        })

    template_vars = {
        "first_name": myClientActivity.client.first_name,
        "last_name": myClientActivity.client.last_name,
        "phone": myClientActivity.client.phone,
        "email": myClientActivity.client.email,
        "survey": url,
        "subsidiary": myClientActivity.subsidiary.name,
        "service": myClientActivity.service.name
    }
    request_context = RequestContext(request, template_vars)
    return render_to_response("call_center/modal.html", request_context)
    #return HttpResponse(simplejson.dumps(clientToJson))


@login_required(login_url='/signin/')
def getClientSearch(request, client_id, b_id, s_id):

    clientToJson = {'client': []}

    client = Client.objects.get(pk=client_id, active=True)
    businessUnit = BusinessUnit.objects.get(pk=b_id, active=True)
    service = Service.objects.get(pk=s_id, active=True)

    myClientActivity = ClientActivity.objects.filter(
        business_unit=businessUnit, service=service, client=client
    ).order_by('?').exclude(status="A").exclude(status="D")[0]

    a_id_and_c_id = str(myClientActivity.id)+str(myClientActivity.client.id)
    activity_code = short_url.encode_url(int(a_id_and_c_id))

    url = "http://xindex.wimjapps.com/surveys/answer/"\
          + str(short_url.encode_url(myClientActivity.survey.id))\
          + "/"\
          + str(activity_code)\
          + "/"\
          + str(short_url.encode_url(myClientActivity.client.id))

    if myClientActivity:
        clientToJson['client'].append({
            "first_name": myClientActivity.client.first_name,
            "last_name": myClientActivity.client.last_name,
            "phone": myClientActivity.client.phone,
            "email": myClientActivity.client.email,
            "survey": url
        })

    template_vars = {
        "first_name": myClientActivity.client.first_name,
        "last_name": myClientActivity.client.last_name,
        "phone": myClientActivity.client.phone,
        "email": myClientActivity.client.email,
        "survey": url,
        "subsidiary": myClientActivity.subsidiary.name,
        "service": myClientActivity.service.name
    }
    request_context = RequestContext(request, template_vars)
    return render_to_response("call_center/modal.html", request_context)
    #return HttpResponse(simplejson.dumps(clientToJson))


@login_required(login_url='/signin/')
def getClientsInJson(request, text):

    clientsToJson = {'client': []}

    myClients = Client.objects.filter(
        first_name__contains=text
    ) | Client.objects.filter(
        last_name__contains=text
    ) | Client.objects.filter(
        email__contains=text
    )

    if myClients:
        for eachClient in myClients:
            clientsToJson['client'].append(
                {
                    "name": eachClient.first_name + " " + eachClient.last_name,
                    "id": eachClient.id
                }
            )

    print clientsToJson
    return HttpResponse(simplejson.dumps(clientsToJson))