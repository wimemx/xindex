from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, render_to_response
from django.template.context import RequestContext
from django.http import HttpResponse, Http404, HttpResponseRedirect
from xindex.models import Company, Xindex_User, Service
from xindex.models import Question, Option, Moment, Attributes
from xindex.models import Zone, Subsidiary, BusinessUnit, Service
from xindex.models import SubsidiaryBusinessUnit, sbu_service, sbu_service_moment
from xindex.models import sbu_service_moment_attribute
from xindex.models import Answer
from xindex.models import Client
from decimal import *


def index(request):

    template_vars = {
        'title': ''
    }
    request_context = RequestContext(request, template_vars)
    return render(request, 'reports/index.html', request_context)


def report_by_moment(request):
    global zone, subsidiary, businessUnit, service, moment
    survey_is_designed = False
    moment_xindex = Decimal(0)
    zones = []
    subsidiaries = []
    businessUnits = []
    services = []
    moments = []
    data_attribute = []
    historical_months = []
    current_data = {}
    xindex_diff = 0
    diff_type = ''
    xindex_user = Xindex_User.objects.get(pk=request.user.id)
    companies = xindex_user.company_set.all()

    '''
    #Get services
    for company in companies:
        for subsidiary in company.subsidiary_set.all():
            for business_unit in subsidiary:
                for service in business_unit.service.all():
                    coincidences = 0
                    for s in services:
                        if s == service:
                            coincidences += 1
                    if coincidences == 0:
                        services.append(service)

    #Get moments
    for company in companies:
        for subsidiary in company.subsidiary_set.all():
            for business_unit in subsidiary.businessunit_set.all():
                for service in business_unit.service.all():
                    for moment in service.moments.all():
                        coincidences = 0
                        for m in moments:
                            if m == moment:
                                coincidences += 1
                        if coincidences == 0:
                            moments.append(moment)
    '''

    #Get Zones
    myZones = Zone.objects.filter(active=True)
    for eachZone in myZones:
        zones.append(eachZone)

    #Get Subsidiaries
    mySubsidiaries = Subsidiary.objects.filter(active=True)
    for eachSubsidiary in mySubsidiaries:
        subsidiaries.append(eachSubsidiary)

    if request.POST:
        if 'zone' in request.POST:
            zone = Zone.objects.get(active=True, pk=int(request.POST['zone']))
            if 'subsidiary' in request.POST:
                subsidiary = Subsidiary.objects.get(active=True, pk=int(request.POST['subsidiary']))
                if 'business_unit' in request.POST:
                    businessUnit = BusinessUnit.objects.get(active=True, pk=int(request.POST['business_unit']))
                    if 'service' in request.POST:
                        service = Service.objects.get(active=True, pk=int(request.POST['service']))
                        if 'moment' in request.POST:
                            moment = Moment.objects.get(active=True, pk=int(request.POST['moment']))
                            print '{{{{{{{{{{{{{{'
                            print 'Obtuvo todos los parametros!'
                            print '{{{{{{{{{{{{{{'
                        else:
                            moment = False
                    else:
                        service = False
                else:
                    businessUnit = False
            else:
                subsidiary = False

        subsidiaries = zone.subsidiary_set.filter(pk=subsidiary.id)
        for subsidiary in subsidiaries:
            for s_bu in SubsidiaryBusinessUnit.objects.filter(id_subsidiary=subsidiary):
                #check business units list
                coincidences_bu = 0
                for bu in businessUnits:
                    if bu == s_bu.id_business_unit:
                        coincidences_bu += 1
                if coincidences_bu == 0:
                    businessUnits.append(s_bu.id_business_unit)

                for s_bu_s in sbu_service.objects.filter(id_subsidiaryBU=s_bu):
                    #check services list
                    coincidences_bu_s = 0
                    for s in services:
                        if s == s_bu_s.id_service:
                            coincidences_bu_s += 1
                    if coincidences_bu_s == 0:
                        services.append(s_bu_s.id_service)

                    for s_bu_s_m in sbu_service_moment.objects.filter(id_sbu_service=s_bu_s):
                        coincidences_bu_s_m = 0
                        for m in moments:
                            if m == s_bu_s_m.id_moment:
                                coincidences_bu_s_m += 1
                        if coincidences_bu_s_m == 0:
                            moments.append(s_bu_s_m.id_moment)

        subsidiaries = zone.subsidiary_set.all()

    else:
        zone = zones[0]
        subsidiary = Subsidiary.objects.filter(zone_id=zone.id)[0]

        #Adding to businessUnit list
        mySUB = SubsidiaryBusinessUnit.objects.filter(
            id_subsidiary__id=subsidiary.id
        )

        #Get Business Units
        myBUIdList = []
        for eachSubsidiaryBusinessUnit in mySUB:
            myBUIdList.append(eachSubsidiaryBusinessUnit.id_business_unit.id)

        myBUIdList = list(set(myBUIdList))
        for eachBUId in myBUIdList:
            myBusinessUnits = BusinessUnit.objects.get(pk=eachBUId)
            if myBusinessUnits.active:
                businessUnits.append(myBusinessUnits)

        businessUnit = businessUnits[0]


        #Adding to services list
        mySUBS = sbu_service.objects.filter(
            id_subsidiaryBU__id_business_unit=businessUnit.id
        )

        #Get Services
        mySIdList = []
        for eachSBUService in mySUBS:
            mySIdList.append(eachSBUService.id_service.id)

        mySIdList = list(set(mySIdList))
        for eachIdService in mySIdList:
            myServices = Service.objects.get(pk=eachIdService)
            services.append(myServices)

        service = services[0]

        #Adding to moment list
        mySUBSMIdList = []
        mySUBSM = sbu_service_moment.objects.filter(
            id_sbu_service__id_service=service.id
        )
        for eachSBUSMoment in mySUBSM:
            mySUBSMIdList.append(eachSBUSMoment.id_moment.id)

        #Get Moments
        mySUBSMIdList = list(set(mySUBSMIdList))
        for eachMoment in mySUBSMIdList:
            myMoments = Moment.objects.get(pk=eachMoment)
            moments.append(myMoments)

        moment = moments[0]
        #Get relations starting by subsidiary
    print '---------------------------------------'
    print zone
    print subsidiary
    print businessUnit
    print service
    print moment
    print '---------------------------------------'

    total_promoters = 0
    total_passives = 0
    total_detractors = 0
    total_answers = 0
    answers_list = []
    for child_subsidiary_bu in SubsidiaryBusinessUnit.objects.filter(id_subsidiary=subsidiary, id_business_unit=businessUnit):
        for child_sbu_service in sbu_service.objects.filter(id_subsidiaryBU=child_subsidiary_bu, id_service=service):
            for child_sbu_s_moment in sbu_service_moment.objects.filter(id_sbu_service=child_sbu_service, id_moment=moment):
                if len(sbu_service_moment_attribute.objects.filter(id_sbu_service_moment=child_sbu_s_moment)) > 0:
                    survey_is_designed = True
                    for child_sbu_s_m_a in sbu_service_moment_attribute.objects.filter(id_sbu_service_moment=child_sbu_s_moment).order_by('id_attribute'):
                        for relation_q_s_bu_s_m_a in child_sbu_s_m_a.question_sbu_s_m_a_set.all():
                            question_answers = Answer.objects.filter(question_id=relation_q_s_bu_s_m_a.question_id)
                            print 'wiwiwiwiwiwi'
                            print child_sbu_s_m_a.id_attribute
                            print 'wiwiwiwiwiwi'
                            for a in question_answers:
                                client = Client.objects.get(pk=a.client_id)
                                try:
                                    client_activity = client.clientactivity_set.get(subsidiary=subsidiary, business_unit=businessUnit, service=service)
                                    answers_list.append(a)
                                except client_activity.DoesNotExist:
                                    pass
                            total_surveyed = len(answers_list)
                            #total_surveyed = len(Answer.objects.filter(question_id=relation_q_s_bu_s_m_a.question_id, client_id__subsidiary=subsidiary))
                            attribute = child_sbu_s_m_a.id_attribute
                            promoters_9 = 0
                            promoters_10 = 0
                            passives = 0
                            detractors = 0
                            if total_surveyed > 0:

                                #for answer in Answer.objects.filter(question_id=relation_q_s_bu_s_m_a.question_id, client_id__subsidiary=subsidiary):
                                for answer in answers_list:
                                    print answer.value
                                    total_answers += 1
                                    if answer.value == 10:
                                        promoters_10 += 1
                                        total_promoters += 1
                                        print 'Respuesta: '+str(answer.value)+' is Promoter 10'
                                    elif answer.value == 9:
                                        promoters_9 += 1
                                        total_promoters += 1
                                        print 'Respuesta: '+str(answer.value)+' is Promoter 9'
                                    elif answer.value == 8 or answer.value == 7:
                                        passives += 1
                                        total_passives += 1
                                        print 'Respuesta: '+str(answer.value)+' is Passive'
                                    elif 1 <= answer.value <= 6:
                                        detractors += 1
                                        total_detractors += 1
                                        print 'Respuesta: '+str(answer.value)+' is Detractor'

                                getcontext().prec = 5

                                if promoters_10 == 0:
                                    promoters_10_percent = 0
                                else:
                                    promoters_10_percent = Decimal(promoters_10*100)/Decimal(total_surveyed)

                                if promoters_9 == 0:
                                    promoters_9_percent = 0
                                else:
                                    promoters_9_percent = Decimal(promoters_9*100)/Decimal(total_surveyed)

                                if passives == 0:
                                    passives_percent = 0
                                else:
                                    passives_percent = Decimal(passives*100)/Decimal(total_surveyed)

                                if detractors == 0:
                                    detractors_percent = 0
                                else:
                                    detractors_percent = Decimal(detractors*100)/Decimal(total_surveyed)

                                xindex_percent = Decimal(promoters_10_percent+promoters_9_percent)-Decimal(detractors_percent)

                                #round all the percents to 1 decimal
                                promoters_10_percent = round(promoters_10_percent, 5)
                                promoters_9_percent = round(promoters_9_percent, 5)
                                passives_percent = round(passives_percent, 5)
                                detractors_percent = round(detractors_percent, 5)
                                xindex_percent = round(xindex_percent, 5)

                                data_attribute.append(
                                    {
                                        'attribute_id': attribute.id,
                                        'attribute_name': attribute.name,
                                        'promoters_10_percent': promoters_10_percent,
                                        'promoters_9_percent': promoters_9_percent,
                                        'passives_percent': passives_percent,
                                        'detractors_percent': detractors_percent,
                                        'xindex_percent': xindex_percent
                                    }
                                )
                            else:
                                data_attribute.append(
                                    {
                                        'attribute_id': attribute.id,
                                        'attribute_name': attribute.name,
                                        'promoters_10_percent': 0,
                                        'promoters_9_percent': 0,
                                        'passives_percent': 0,
                                        'detractors_percent': 0,
                                        'xindex_percent': 0
                                    }
                                )
                else:
                    survey_is_designed = False
    if survey_is_designed is True:
        #TODO: Get the historical data for this moment from the new model (create model)
        historical_months = [
            {'month': '2013-07', 'value': Decimal(45.67)},
            {'month': '2013-08', 'value': Decimal(56.78)},
            {'month': '2013-09', 'value': Decimal(59.51)}
        ]

        getcontext().prec = 5
        print '____________'
        print total_promoters
        print total_detractors
        print total_passives
        print total_answers
        print '____________'
        if total_promoters == 0 and total_detractors == 0 and total_passives == 0 and total_answers == 0:
            moment_xindex = 0
        else:
            moment_xindex = ((Decimal(total_promoters-total_detractors))/(Decimal(total_promoters+total_passives+total_detractors)))*Decimal(100)

        #current data
        current_data = {'month': '2013-10', 'value': moment_xindex}

        #compare the xindex last month with the current xindex month
        last_month = historical_months[2]
        if last_month['value'] > current_data['value']:
            xindex_diff = last_month['value'] - current_data['value']
            diff_type = 'negative'
        else:
            diff_type = 'positive'
            xindex_diff = current_data['value'] - last_month['value']
    if total_answers == 0 and total_promoters == 0 and total_passives == 0 and total_detractors == 0:
        moment_data = {'promoters': 0, 'passives': 0, 'detractors': 0}
    else:
        moment_data = {'promoters': Decimal((Decimal(total_promoters)/total_answers)*100), 'passives': Decimal((Decimal(total_passives)/total_answers)*100), 'detractors': Decimal((Decimal(total_detractors)/total_answers)*100)}

    template_vars = {
        'title': '',
        'survey_is_designed': survey_is_designed,
        'moment_xindex': moment_xindex,
        'zones': zones,
        'subsidiaries': subsidiaries,
        'businessUnits': businessUnits,
        'moments': moments,
        'services': services,
        'current_zone': zone,
        'current_subsidiary': subsidiary,
        'current_businessUnit': businessUnit,
        'current_service': service,
        'current_moment': moment,
        'historical_months': historical_months,
        'current_data': current_data,
        'comparison': {'xindex_diff': xindex_diff, 'diff_type': diff_type},
        'data_attribute': data_attribute,
        'moment_data': moment_data
    }
    request_context = RequestContext(request, template_vars)
    return render(request, 'reports/moment-report.html', request_context)


def report_by_attribute(request):
    if request.POST:
        print request.POST
        if 'zone' in request.POST:
            zone = Zone.objects.get(active=True, pk=int(request.POST['zone']))
            if 'subsidiary' in request.POST:
                subsidiary = Subsidiary.objects.get(active=True, pk=int(request.POST['subsidiary']))
                if 'business_unit' in request.POST:
                    businessUnit = BusinessUnit.objects.get(active=True, pk=int(request.POST['business_unit']))
                    if 'service' in request.POST:
                        service = Service.objects.get(active=True, pk=int(request.POST['service']))
                        if 'moment' in request.POST:
                            moment = Moment.objects.get(active=True, pk=int(request.POST['moment']))
                            if 'attribute' in request.POST:
                                attribute = Attributes.objects.get(pk=int(request.POST['attribute']))
                        else:
                            moment = False
                    else:
                        service = False
                else:
                    businessUnit = False
            else:
                subsidiary = False
    else:
        pass

    s_bu = SubsidiaryBusinessUnit.objects.get(id_subsidiary=subsidiary, id_business_unit=businessUnit)

    for s_bu_s in sbu_service.objects.filter(id_subsidiaryBU=s_bu, id_service=service):
        for s_bu_s_m in sbu_service_moment.objects.filter(id_sbu_service=s_bu_s, id_moment=moment):
            for s_bu_s_m_a in sbu_service_moment_attribute.objects.filter(id_sbu_service_moment=s_bu_s_m, id_attribute=attribute):
                for s_bu_s_m_a_q in s_bu_s_m_a.question_sbu_s_m_a_set.all():
                    attrib_answers = Answer.objects.filter(question=s_bu_s_m_a_q.question_id)
                    total_answers = []
                    for answer in attrib_answers:
                        client = Client.objects.get(pk=int(answer.client.id))
                        try:
                            client_activity = client.clientactivity_set.get(subsidiary=subsidiary, business_unit=businessUnit, service=service)
                            if client_activity.subsidiary == subsidiary and client_activity.business_unit == businessUnit:
                                total_answers.append(answer)
                        except client_activity.DoesNotExist:
                            pass

                    for answer in total_answers:
                        print answer
    template_vars = {}
    request_context = RequestContext(request, template_vars)
    return render(request, 'reports/attribute-report.html', request_context)

    return HttpResponse('This is the report by attribute')