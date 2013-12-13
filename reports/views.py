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
from xindex.models import ClientActivity
from xindex.models import Cumulative_Report
from decimal import *
import random
import datetime



def index(request):

    template_vars = {
        'title': ''
    }
    request_context = RequestContext(request, template_vars)
    return render(request, 'reports/index.html', request_context)


@login_required(login_url='/signin/')
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

    #Get Zones
    myZones = Zone.objects.filter(active=True)
    for eachZone in myZones:
        zones.append(eachZone)

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

        subsidiaries = zone.subsidiary_set.all()

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

    total_promoters = 0
    total_passives = 0
    total_detractors = 0
    total_answers = 0

    for child_subsidiary_bu in SubsidiaryBusinessUnit.objects.filter(id_subsidiary=subsidiary, id_business_unit=businessUnit):
        for child_sbu_service in sbu_service.objects.filter(id_subsidiaryBU=child_subsidiary_bu, id_service=service):
            for child_sbu_s_moment in sbu_service_moment.objects.filter(id_sbu_service=child_sbu_service, id_moment=moment):
                if len(sbu_service_moment_attribute.objects.filter(id_sbu_service_moment=child_sbu_s_moment)) > 0:
                    survey_is_designed = True
                    for child_sbu_s_m_a in sbu_service_moment_attribute.objects.filter(id_sbu_service_moment=child_sbu_s_moment).order_by('id_attribute'):
                        for relation_q_s_bu_s_m_a in child_sbu_s_m_a.question_sbu_s_m_a_set.all():
                            question_answers = Answer.objects.filter(question_id=relation_q_s_bu_s_m_a.question_id)

                            answers_list = []
                            for a in question_answers:
                                client = Client.objects.get(pk=a.client_id)
                                try:

                                    client_activity = ClientActivity.objects.get(client=client, subsidiary=subsidiary, business_unit=businessUnit, service=service)
                                    c_d = datetime.date.today()
                                    if a.date.year == c_d.year and a.date.month == c_d.month and client_activity.subsidiary == subsidiary and client_activity.business_unit == businessUnit:
                                        answers_list.append(a)
                                        print 'Today is '+str(c_d.day)+' from '+str(c_d.year)
                                        print 'Question date is '+str(a.date.day)+' from '+str(a.date.year)
                                except ClientActivity.DoesNotExist:
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
                                    elif answer.value == 9:
                                        promoters_9 += 1
                                        total_promoters += 1
                                    elif answer.value == 8 or answer.value == 7:
                                        passives += 1
                                        total_passives += 1
                                    elif 1 <= answer.value <= 6:
                                        detractors += 1
                                        total_detractors += 1

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

        historical_data = Cumulative_Report.objects.filter(
            id_subsidiary=subsidiary, id_business_unit=businessUnit,
            id_service=service, id_moment=moment, id_attribute=None
        ).order_by('-date')[:3]

        historical_months = []

        for last_data in reversed(historical_data):
            historical_months.append(
                {
                    'month': str(last_data.date.year)+'-'+str(last_data.date.month),
                    'value': last_data.grade
                }
            )

        getcontext().prec = 5

        if total_promoters == 0 and total_detractors == 0 and total_passives == 0 and total_answers == 0:
            moment_xindex = 0
        else:
            moment_xindex = ((Decimal(total_promoters-total_detractors))/(Decimal(total_promoters+total_passives+total_detractors)))*Decimal(100)

        #current data
        current_date = datetime.date.today()
        current_data = {'month': str(current_date.year)+'-'+str(current_date.month), 'value': moment_xindex}

        #compare the xindex last month with the current xindex month
        if len(historical_months) < 3:
            if len(historical_months) == 2:
                last_month = historical_months[1]
            elif len(historical_months) == 1:
                last_month = historical_months[0]
            elif len(historical_months) == 0:
                #create an object of the last month
                if current_date.month == 01:
                    month = 12
                    year = current_date.year - 1
                else:
                    month = current_date.month - 1
                    year = current_date.year
                last_month = {
                    'month': str(year)+'-'+str(month),
                    'value': Decimal(0)
                }
                #historical_months.append(last_month)
        else:
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


@login_required(login_url='/signin/')
def report_by_attribute(request):
    zones_list = Zone.objects.all()
    business_units_list = []
    services_list = []
    moments_list = []
    attributes_list = []
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
        zone = Zone.objects.filter(active=True)[0]

        subsidiary = zone.subsidiary_set.filter(active=True)[0]

        for s_bu in SubsidiaryBusinessUnit.objects.filter(id_subsidiary=subsidiary):
            counter_s_bu = 0
            if counter_s_bu == 0:
                businessUnit = s_bu.id_business_unit
                for s_bu_s in sbu_service.objects.filter(id_subsidiaryBU=s_bu):
                    counter_s_bu_s = 0
                    if counter_s_bu_s == 0:
                        service = s_bu_s.id_service
                        for s_bu_s_m in sbu_service_moment.objects.filter(id_sbu_service=s_bu_s):
                            counter_s_bu_s_m = 0
                            if counter_s_bu_s_m == 0:
                                moment = s_bu_s_m.id_moment
                                for s_bu_s_m_a in sbu_service_moment_attribute.objects.filter(id_sbu_service_moment=s_bu_s_m):
                                    counter_s_bu_s_m_a = 0
                                    if counter_s_bu_s_m_a == 0:
                                        attribute = s_bu_s_m_a.id_attribute
                                    counter_s_bu_s_m_a += 1
                            counter_s_bu_s_m += 1
                    counter_s_bu_s += 1
            counter_s_bu += 1

    subsidiaries_list = zone.subsidiary_set.all()

    for s_bu in SubsidiaryBusinessUnit.objects.filter(id_subsidiary=subsidiary):
        if len(business_units_list) > 0:
            coincidences_bu = 0
            for business_unit in business_units_list:
                if business_unit == s_bu.id_business_unit:
                    coincidences_bu += 1
            if coincidences_bu == 0:
                business_units_list.append(s_bu.id_business_unit)
        else:
            business_units_list.append(s_bu.id_business_unit)

    for s_bu in SubsidiaryBusinessUnit.objects.filter(id_subsidiary=subsidiary, id_business_unit=businessUnit):
        for s_bu_s in sbu_service.objects.filter(id_subsidiaryBU=s_bu):
            if len(services_list) > 0:
                coincidences_s = 0
                for s in services_list:
                    if s == s_bu_s.id_service:
                        coincidences_s += 1
                if coincidences_s == 0:
                    services_list.append(s_bu_s.id_service)
            else:
                services_list.append(s_bu_s.id_service)

    for s_bu in SubsidiaryBusinessUnit.objects.filter(id_subsidiary=subsidiary, id_business_unit=businessUnit):
        for s_bu_s in sbu_service.objects.filter(id_subsidiaryBU=s_bu, id_service=service):
            for s_bu_s_m in sbu_service_moment.objects.filter(id_sbu_service=s_bu_s):
                if len(moments_list) > 0:
                    coincidences_m = 0
                    for m in moments_list:
                        if m == s_bu_s_m.id_moment:
                            coincidences_m += 1
                    if coincidences_m == 0:
                        moments_list.append(s_bu_s_m.id_moment)
                else:
                    moments_list.append(s_bu_s_m.id_moment)

    for s_bu in SubsidiaryBusinessUnit.objects.filter(id_subsidiary=subsidiary, id_business_unit=businessUnit):
        for s_bu_s in sbu_service.objects.filter(id_subsidiaryBU=s_bu, id_service=service):
            for s_bu_s_m in sbu_service_moment.objects.filter(id_sbu_service=s_bu_s, id_moment=moment):
                for s_bu_s_m_a in sbu_service_moment_attribute.objects.filter(id_sbu_service_moment=s_bu_s_m):
                    if len(attributes_list) > 0:
                        coincidences_a = 0
                        for a in attributes_list:
                            if a == s_bu_s_m_a.id_attribute:
                                coincidences_a += 1
                        if coincidences_a == 0:
                            attributes_list.append(s_bu_s_m_a.id_attribute)
                    else:
                        attributes_list.append(s_bu_s_m_a.id_attribute)

    s_bu = SubsidiaryBusinessUnit.objects.get(id_subsidiary=subsidiary, id_business_unit=businessUnit)
    total_answers = []
    for s_bu_s in sbu_service.objects.filter(id_subsidiaryBU=s_bu, id_service=service):
        for s_bu_s_m in sbu_service_moment.objects.filter(id_sbu_service=s_bu_s, id_moment=moment):
            for s_bu_s_m_a in sbu_service_moment_attribute.objects.filter(id_sbu_service_moment=s_bu_s_m, id_attribute=attribute):
                for s_bu_s_m_a_q in s_bu_s_m_a.question_sbu_s_m_a_set.all():
                    attrib_answers = Answer.objects.filter(question=s_bu_s_m_a_q.question_id)
                    for answer in attrib_answers:
                        client = Client.objects.get(pk=int(answer.client.id))
                        try:
                            #client_activity = client.clientactivity_set.get(subsidiary=subsidiary, business_unit=businessUnit, service=service)
                            c_d = datetime.date.today()
                            client_activity = ClientActivity.objects.get(client=client, subsidiary=subsidiary, business_unit=businessUnit, service=service)
                            if client_activity.subsidiary == subsidiary and client_activity.business_unit == businessUnit and answer.date.year == c_d.year and answer.date.month == c_d.month:
                                total_answers.append(answer)
                        except ClientActivity.DoesNotExist:
                            pass

    xindex_attribute = 0
    promoters = 0
    passives = 0
    detractors = 0
    promoters_percent = 0
    passives_percent = 0
    detractors_percent = 0
    total_surveyed = len(total_answers)
    if not total_surveyed == 0:
        for answer in total_answers:
            if answer.value == 10 or answer.value == 9:
                promoters += 1
            elif answer.value == 8 or answer.value == 7:
                passives += 1
            elif 1 <= answer.value <= 6:
                detractors += 1

        getcontext().prec = 5

        if not promoters == 0:
            promoters_percent = Decimal(promoters*100)/Decimal(total_surveyed)

        if not passives == 0:
            passives_percent = Decimal(passives*100)/Decimal(total_surveyed)

        if not detractors == 0:
            detractors_percent = Decimal(detractors*100)/Decimal(total_surveyed)

    if promoters == 0 and passives == 0 and detractors == 0:
        xindex_attribute = 0
    else:
        xindex_attribute = ((Decimal(promoters-detractors))/(Decimal(promoters+passives+detractors)))*Decimal(100)

    historical_data = Cumulative_Report.objects.filter(
        id_subsidiary=subsidiary, id_business_unit=businessUnit,
        id_service=service, id_moment=moment, id_attribute=attribute
    ).order_by('-date')[:3]

    historical_months = []

    for last_data in reversed(historical_data):
        historical_months.append(
            {
                'month': str(last_data.date.year)+'-'+str(last_data.date.month),
                'value': last_data.grade
            }
        )

    getcontext().prec = 5

    #current data
    current_date = datetime.date.today()
    current_data = {'month': str(current_date.year)+'-'+str(current_date.month), 'value': xindex_attribute}

    #compare the xindex last month with the current xindex month
    if len(historical_months) < 3:
        if len(historical_months) == 2:
            last_month = historical_months[1]
        elif len(historical_months) == 1:
            last_month = historical_months[0]
        elif len(historical_months) == 0:
            #create an object of the last month
            if current_date.month == 01:
                month = 12
                year = current_date.year - 1
            else:
                month = current_date.month - 1
                year = current_date.year
            last_month = {
                'month': str(year)+'-'+str(month),
                'value': Decimal(0)
            }
            #historical_months.append(last_month)
    else:
        last_month = historical_months[2]

    if last_month['value'] > current_data['value']:
        xindex_diff = last_month['value'] - current_data['value']
        diff_type = 'negative'
    else:
        diff_type = 'positive'
        xindex_diff = current_data['value'] - last_month['value']

    if total_answers == 0 and promoters == 0 and passives == 0 and detractors == 0:
        attribute_data = {'promoters': 0, 'passives': 0, 'detractors': 0}
    else:
        attribute_data = {'promoters': promoters_percent, 'passives': passives_percent, 'detractors': detractors_percent}

    template_vars = {
        'promoters': promoters_percent,
        'passives': passives_percent,
        'attribute_data': attribute_data,
        'xindex_attribute': xindex_attribute,
        'historical_months': historical_months,
        'current_data': current_data,
        'comparison': {'xindex_diff': xindex_diff, 'diff_type': diff_type},
        'current_zone': zone,
        'current_subsidiary': subsidiary,
        'current_businessUnit': businessUnit,
        'current_service': service,
        'current_moment': moment,
        'current_attribute': attribute,
        'zones_list': zones_list,
        'subsidiaries_list': subsidiaries_list,
        'business_units_list': business_units_list,
        'services_list': services_list,
        'moments_list': moments_list,
        'attributes_list': attributes_list
    }
    request_context = RequestContext(request, template_vars)
    return render(request, 'reports/attribute-report.html', request_context)


@login_required(login_url='/signin/')
def report_by_service(request):
    #data for service
    xindex_service = 0
    promoters_percent = 0
    passives_percent = 0
    detractors_percent = 0
    #lists
    zones_list = Zone.objects.all()
    business_units_list = []
    services_list = []
    #moments data
    moments_data = []
    #data for relation?
    survey_is_designed = True
    #current date
    c_d = datetime.date.today()
    if request.POST:
        if 'zone' in request.POST:
            zone = Zone.objects.get(active=True, pk=int(request.POST['zone']))
            if 'subsidiary' in request.POST:
                subsidiary = Subsidiary.objects.get(active=True, pk=int(request.POST['subsidiary']))
                if 'business_unit' in request.POST:
                    business_unit = BusinessUnit.objects.get(active=True, pk=int(request.POST['business_unit']))
                    if 'service' in request.POST:
                        service = Service.objects.get(active=True, pk=int(request.POST['service']))
                    else:
                        service = False
                else:
                    business_unit = False
            else:
                subsidiary = False
    else:
        zone = Zone.objects.filter(active=True)[0]

        subsidiary = zone.subsidiary_set.filter(active=True).order_by('id')[0]

        for s_bu in SubsidiaryBusinessUnit.objects.filter(id_subsidiary=subsidiary):
            counter_s_bu = 0
            if counter_s_bu == 0:
                business_unit = s_bu.id_business_unit
                for s_bu_s in sbu_service.objects.filter(id_subsidiaryBU=s_bu):
                    counter_s_bu_s = 0
                    if counter_s_bu_s == 0:
                        service = s_bu_s.id_service
                    counter_s_bu_s += 1
            counter_s_bu += 1

    #Get subsidiaries
    subsidiaries_list = zone.subsidiary_set.all()

    #Get business units for first subsidiary
    for s_bu in SubsidiaryBusinessUnit.objects.filter(id_subsidiary=subsidiary):
        if len(business_units_list) > 0:
            coincidences_bu = 0
            for b_u in business_units_list:
                if b_u == s_bu.id_business_unit:
                    coincidences_bu += 1
            if coincidences_bu == 0:
                business_units_list.append(s_bu.id_business_unit)
        else:
            business_units_list.append(s_bu.id_business_unit)

    #Get services for first business unit
    for s_bu in SubsidiaryBusinessUnit.objects.filter(id_subsidiary=subsidiary, id_business_unit=business_unit):
        for s_bu_s in sbu_service.objects.filter(id_subsidiaryBU=s_bu):
            if len(services_list) > 0:
                coincidences_s = 0
                for s in services_list:
                    if s == s_bu_s.id_service:
                        coincidences_s += 1
                if coincidences_s == 0:
                    services_list.append(s_bu_s.id_service)
            else:
                services_list.append(s_bu_s.id_service)

    #Get data for service moments
    total_promoters = 0
    total_passives = 0
    total_detractors = 0
    total_surveyed = 0
    #relation between subsidiary and business unit
    s_bu = SubsidiaryBusinessUnit.objects.get(id_subsidiary=subsidiary, id_business_unit=business_unit)
    for s_bu_s in sbu_service.objects.filter(id_subsidiaryBU=s_bu, id_service=service):
        #All moments for this service
        if len(sbu_service_moment.objects.filter(id_sbu_service=s_bu_s)) == 0:
            survey_is_designed = False
        for s_bu_s_m in sbu_service_moment.objects.filter(id_sbu_service=s_bu_s).order_by('id_moment'):
            #All attributes for all moments

            total_answers_by_moment = []
            total_promoters_moment = 0
            promoters_10_moment = 0
            promoters_percent_10_moment = 0
            promoters_9_moment = 0
            promoters_percent_9_moment = 0
            passives_moment = 0
            passives_percent_moment = 0
            detractors_moment = 0
            detractors_percent_moment = 0
            xindex_moment = 0

            for s_bu_s_m_a in sbu_service_moment_attribute.objects.filter(id_sbu_service_moment=s_bu_s_m):
                for s_bu_s_m_a_q in s_bu_s_m_a.question_sbu_s_m_a_set.all():
                    attrib_answers = Answer.objects.filter(question=s_bu_s_m_a_q.question_id)

                    for answer in attrib_answers:
                        client = Client.objects.get(pk=int(answer.client.id))
                        try:
                            client_activity = ClientActivity.objects.get(client=client, subsidiary=subsidiary, business_unit=business_unit, service=service)
                            if answer.date.year == c_d.year and answer.date.month == c_d.month and client_activity.subsidiary == subsidiary and client_activity.business_unit == business_unit:
                                total_answers_by_moment.append(answer)
                        except ClientActivity.DoesNotExist:
                            pass

            if not len(total_answers_by_moment) == 0:
                for answer_moment in total_answers_by_moment:
                    #total answers for service
                    total_surveyed += 1
                    if answer_moment.value == 10:
                        promoters_10_moment += 1
                        total_promoters_moment += 1
                        #promoters for service
                        total_promoters += 1
                    elif answer_moment.value == 9:
                        promoters_9_moment += 1
                        total_promoters_moment += 1
                        #promoters for service
                        total_promoters += 1
                    elif answer_moment.value == 8 or answer_moment.value == 7:
                        passives_moment += 1
                        #passives for service
                        total_passives += 1
                    elif 1 <= answer_moment.value <= 6:
                        detractors_moment += 1
                        #detractors for service
                        total_detractors += 1

            getcontext().prec = 5
            if not promoters_10_moment == 0:
                promoters_percent_10_moment = Decimal(promoters_10_moment*100)/Decimal(len(total_answers_by_moment))

            if not promoters_9_moment == 0:
                promoters_percent_9_moment = Decimal(promoters_9_moment*100)/Decimal(len(total_answers_by_moment))

            if not passives_moment == 0:
                passives_percent_moment = Decimal(passives_moment*100)/Decimal(len(total_answers_by_moment))

            if not detractors_moment == 0:
                detractors_percent_moment = Decimal(detractors_moment*100)/Decimal(len(total_answers_by_moment))

            if promoters_percent_10_moment == 0 and promoters_percent_9_moment == 0 and passives_percent_moment == 0 and detractors_percent_moment == 0:
                xindex_moment = 0
            else:
                xindex_moment = ((Decimal((promoters_percent_10_moment+promoters_percent_9_moment)-detractors_percent_moment))
                                 / (Decimal(promoters_percent_10_moment+promoters_percent_9_moment+passives_percent_moment+detractors_percent_moment)))*Decimal(100)

            moments_data.append(
                {
                    #xindex for moment
                    'xindex_moment': xindex_moment,
                    #info
                    'moment_id': s_bu_s_m.id_moment.id,
                    'moment_name': s_bu_s_m.id_moment.name,
                    #data
                    'promoters_10': promoters_percent_10_moment,
                    'promoters_9': promoters_percent_9_moment,
                    'passives': passives_percent_moment,
                    'detractors': detractors_percent_moment,
                }
            )

    #Calculate the service data
    getcontext().prec = 5

    if total_promoters != 0 and total_surveyed != 0:
        promoters_percent = Decimal(total_promoters*100)/Decimal(total_surveyed)

    if total_passives != 0 and total_surveyed != 0:
        passives_percent = Decimal(total_passives*100)/Decimal(total_surveyed)

    if total_detractors != 0 and total_surveyed != 0:
        detractors_percent = Decimal(total_detractors*100)/Decimal(total_surveyed)

    if promoters_percent != 0 and passives_percent != 0 and detractors_percent != 0:
        #xindex_service = ((Decimal(promoters_percent-detractors_percent))/(Decimal(promoters_percent+passives_percent+detractors_percent)))*Decimal(100)
        total_promoters_percent = Decimal(total_promoters)/Decimal(total_surveyed)
        total_detractors_percent = Decimal(total_detractors)/Decimal(total_surveyed)
        xindex_service = Decimal(total_promoters_percent-total_detractors_percent)*100

    ##############
    historical_data = Cumulative_Report.objects.filter(
        id_subsidiary=subsidiary, id_business_unit=business_unit,
        id_service=service, id_moment=None, id_attribute=None
    ).order_by('-date')[:3]

    historical_months = []

    for last_data in reversed(historical_data):
        historical_months.append(
            {
                'month': str(last_data.date.year)+'-'+str(last_data.date.month),
                'value': last_data.grade
            }
        )

    getcontext().prec = 5

    #current data
    current_data = {'month': str(c_d.year)+'-'+str(c_d.month), 'value': xindex_service}

    #compare the xindex last month with the current xindex month
    if len(historical_months) < 3:
        if len(historical_months) == 2:
            last_month = historical_months[1]
        elif len(historical_months) == 1:
            last_month = historical_months[0]
        elif len(historical_months) == 0:
            #create an object of the last month
            current_date = datetime.date.today()
            if current_date.month == 01:
                month = 12
                year = current_date.year - 1
            else:
                month = current_date.month - 1
                year = current_date.year
            last_month = {
                'month': str(year)+'-'+str(month),
                'value': Decimal(0)
            }
            #historical_months.append(last_month)
    else:
        last_month = historical_months[2]

    if last_month['value'] > current_data['value']:
        xindex_diff = last_month['value'] - current_data['value']
        diff_type = 'negative'
    else:
        diff_type = 'positive'
        xindex_diff = current_data['value'] - last_month['value']

    if total_surveyed == 0 and total_promoters == 0 and total_passives == 0 and total_detractors == 0:
        service_data = {'promoters': 0, 'passives': 0, 'detractors': 0}
    else:
        service_data = {'promoters': promoters_percent, 'passives': passives_percent, 'detractors': detractors_percent}
    ##############

    ##GET DATA TO COMPARE##
    comparative_data = []
    subsidiaries = zone.subsidiary_set.exclude(id=subsidiary.id)
    if len(subsidiaries) == 0:
        there_are_subsidiaries = False
    if len(subsidiaries) > 0:
        for subsidiary_c in subsidiaries:

            promoters_c = 0
            promoters_percent_c = 0
            passives_c = 0
            passives_percent_c = 0
            detractors_c = 0
            detractors_percent_c = 0
            xindex_service_c = 0
            total_surveyed_c = 0
            total_answers_c = []
            for s_bu in SubsidiaryBusinessUnit.objects.filter(id_subsidiary=subsidiary_c):
                for s_bu_s in sbu_service.objects.filter(id_subsidiaryBU=s_bu, id_service=service):
                    for s_bu_s_m in sbu_service_moment.objects.filter(id_sbu_service=s_bu_s).order_by('id_moment'):
                        for s_bu_s_m_a in sbu_service_moment_attribute.objects.filter(id_sbu_service_moment=s_bu_s_m):
                            for s_bu_s_m_a_q in s_bu_s_m_a.question_sbu_s_m_a_set.all():
                                attrib_answers = Answer.objects.filter(question=s_bu_s_m_a_q.question_id)

                                for answer in attrib_answers:
                                    client = Client.objects.get(pk=int(answer.client.id))
                                    try:
                                        client_activity = ClientActivity.objects.get(client=client, subsidiary=subsidiary_c, business_unit=business_unit, service=service)
                                        if client_activity.subsidiary == subsidiary_c and client_activity.business_unit == business_unit:
                                            total_answers_c.append(answer)
                                    except ClientActivity.DoesNotExist:
                                        pass

            if not len(total_answers_c) == 0:
                for answer_service in total_answers_c:
                    #total answers for service
                    total_surveyed_c += 1
                    if answer_service.value == 10 or answer_service.value == 9:
                        promoters_c += 1
                    elif answer_service.value == 8 or answer_service.value == 7:
                        passives_c += 1
                    elif 1 <= answer_service.value <= 6:
                        detractors_c += 1

            getcontext().prec = 5
            if not promoters_c == 0:
                promoters_percent_c = Decimal(promoters_c*100)/Decimal(len(total_answers_c))

            if not passives_c == 0:
                passives_percent_c = Decimal(passives_c*100)/Decimal(len(total_answers_c))

            if not detractors_c == 0:
                detractors_percent_c = Decimal(detractors_c*100)/Decimal(len(total_answers_c))

            if promoters_percent_c == 0 and passives_percent_c == 0 and detractors_percent_c == 0:
                xindex_service_c = 0
            else:
                xindex_service_c = (Decimal(promoters_percent_c)-Decimal(detractors_percent_c))

            r = lambda: random.randint(0, 255)

            comparative_data.append(
                {
                    #xindex for moment
                    'xindex_service': xindex_service_c,
                    'subsidiary': subsidiary_c,
                    'color': ('#%02X%02X%02X' % (r(), r(), r()))
                }
            )

    ##------------------##

    template_vars = {
        #data for service
        'xindex_service': xindex_service,
        'historical_months': historical_months,
        'current_data': current_data,
        'service_data': service_data,
        'comparison': {'xindex_diff': xindex_diff, 'diff_type': diff_type},
        #data for relation?
        'survey_is_designed': survey_is_designed,
        #current list values
        'current_zone': zone,
        'current_subsidiary': subsidiary,
        'current_business_unit': business_unit,
        'current_service': service,
        #moments data
        'moments_data': moments_data,
        #lists
        'zones': zones_list,
        'subsidiaries': subsidiaries_list,
        'business_units': business_units_list,
        'services': services_list,
        #comparattive data
        'comparative_data': comparative_data
    }
    request_context = RequestContext(request, template_vars)
    return render(request, 'reports/service-report.html', request_context)


@login_required(login_url='/signin/')
def report_by_business_unit(request):
    #data for business unit
    xindex_business_unit = 0
    promoters_percent = 0
    passives_percent = 0
    detractors_percent = 0
    #lists
    zones_list = Zone.objects.all()
    subsidiaries_list = []
    business_units_list = []
    #services data
    services_data = []
    #data for relation?
    survey_is_designed = True

    c_d = datetime.date.today()
    if request.POST:
        print request.POST
        if 'zone' in request.POST:
            #return another report
            if request.POST['zone'] == 'all':
                return report_by_business_unit_not_instances(request)
            else:
                zone = Zone.objects.get(active=True, pk=int(request.POST['zone']))
            if 'subsidiary' in request.POST:
                if request.POST['subsidiary'] == 'all':
                    return report_by_business_unit_not_instances(request)
                else:
                    subsidiary = Subsidiary.objects.get(active=True, pk=int(request.POST['subsidiary']))
                if 'business_unit' in request.POST:
                    business_unit = BusinessUnit.objects.get(active=True, pk=int(request.POST['business_unit']))
                else:
                    businessUnit = False
            else:
                subsidiary = False
    else:
        zone = Zone.objects.filter(active=True)[0]

        if not zone:
            template_vars = {
                'empty_data': True
            }
            request_context = RequestContext(request, template_vars)
            return render(request, 'reports/business-unit-report.html', request_context)

        subsidiary = zone.subsidiary_set.filter(active=True)[0]

        for s_bu in SubsidiaryBusinessUnit.objects.filter(id_subsidiary=subsidiary):
            counter_s_bu = 0
            if counter_s_bu == 0:
                business_unit = s_bu.id_business_unit
            counter_s_bu += 1

    #Get subsidiaries
    subsidiaries_list = zone.subsidiary_set.all()

    #Get business units for first subsidiary
    for s_bu in SubsidiaryBusinessUnit.objects.filter(id_subsidiary=subsidiary):
        if len(business_units_list) > 0:
            coincidences_bu = 0
            for b_u in business_units_list:
                if b_u == s_bu.id_business_unit:
                    coincidences_bu += 1
            if coincidences_bu == 0:
                business_units_list.append(s_bu.id_business_unit)
        else:
            business_units_list.append(s_bu.id_business_unit)

    #Get data for business unit services
    total_promoters = 0
    total_passives = 0
    total_detractors = 0
    total_surveyed = 0
    #relation between subsidiary and business unit
    s_bu = SubsidiaryBusinessUnit.objects.get(id_subsidiary=subsidiary, id_business_unit=business_unit)
    if len(sbu_service.objects.filter(id_subsidiaryBU=s_bu)) == 0:
        survey_is_designed = False
    for s_bu_s in sbu_service.objects.filter(id_subsidiaryBU=s_bu).order_by('id_service'):
        #All services for all business unit
        total_answers_by_service = []
        promoters_service = 0
        promoters_percent_service = 0
        passives_service = 0
        passives_percent_service = 0
        detractors_service = 0
        detractors_percent_service = 0
        xindex_service = 0

        for s_bu_s_m in sbu_service_moment.objects.filter(id_sbu_service=s_bu_s).order_by('id_moment'):
            for s_bu_s_m_a in sbu_service_moment_attribute.objects.filter(id_sbu_service_moment=s_bu_s_m):
                for s_bu_s_m_a_q in s_bu_s_m_a.question_sbu_s_m_a_set.all():
                    attrib_answers = Answer.objects.filter(question=s_bu_s_m_a_q.question_id)

                    for answer in attrib_answers:
                        client = Client.objects.get(pk=int(answer.client.id))
                        try:
                            client_activity = ClientActivity.objects.get(client=client, subsidiary=subsidiary, business_unit=business_unit)
                            if client_activity.subsidiary == subsidiary and client_activity.business_unit == business_unit and answer.date.year == c_d.year and answer.date.month == c_d.month:
                                total_answers_by_service.append(answer)
                        except ClientActivity.DoesNotExist:
                            pass

        if not len(total_answers_by_service) == 0:
            for answer_service in total_answers_by_service:
                #total answers for service
                total_surveyed += 1
                if answer_service.value == 10 or answer_service.value == 9:
                    promoters_service += 1
                    #promoters for business unit
                    total_promoters += 1
                elif answer_service.value == 8 or answer_service.value == 7:
                    passives_service += 1
                    #passives for business unit
                    total_passives += 1
                elif 1 <= answer_service.value <= 6:
                    detractors_service += 1
                    #detractors for business unit
                    total_detractors += 1

        getcontext().prec = 5

        if not promoters_service == 0:
            promoters_percent_service = Decimal(promoters_service*100)/Decimal(len(total_answers_by_service))

        if not passives_service == 0:
            passives_percent_service = Decimal(passives_service*100)/Decimal(len(total_answers_by_service))

        if not detractors_service == 0:
            detractors_percent_service  = Decimal(detractors_service*100)/Decimal(len(total_answers_by_service))

        if promoters_percent_service != 0 and passives_percent_service != 0 and detractors_percent_service != 0:
            #xindex_service = ((Decimal(promoters_percent_service-detractors_percent_service))/(Decimal(promoters_percent_service+passives_percent_service+detractors_percent_service)))*Decimal(100)
            xindex_service = Decimal(promoters_percent_service-detractors_percent_service)

        r = lambda: random.randint(0, 255)

        services_data.append(
            {
                #xindex for moment
                'xindex_service': xindex_service,
                #info
                'service_id': s_bu_s.id_service.id,
                'service_name': s_bu_s.id_service.name,
                #data
                'promoters': promoters_percent_service,
                'passives': passives_percent_service,
                'detractors': detractors_percent_service,
                #extra
                'color': ('#%02X%02X%02X' % (r(), r(), r()))
            }
        )

    #Calculate the business unit data
    getcontext().prec = 5

    if total_promoters != 0 and total_surveyed != 0:
        promoters_percent = Decimal(total_promoters*100)/Decimal(total_surveyed)

    if total_passives != 0 and total_surveyed != 0:
        passives_percent = Decimal(total_passives*100)/Decimal(total_surveyed)

    if total_detractors != 0 and total_surveyed != 0:
        detractors_percent = Decimal(total_detractors*100)/Decimal(total_surveyed)

    if promoters_percent != 0 and passives_percent != 0 and detractors_percent != 0:
        #xindex_service = ((Decimal(promoters_percent-detractors_percent))/(Decimal(promoters_percent+passives_percent+detractors_percent)))*Decimal(100)
        xindex_business_unit = Decimal(promoters_percent-detractors_percent)

    ##############

    historical_data = Cumulative_Report.objects.filter(
        id_subsidiary=subsidiary, id_business_unit=business_unit,
        id_service=None, id_moment=None, id_attribute=None
    ).order_by('-date')[:3]

    historical_months = []

    for last_data in reversed(historical_data):
        historical_months.append(
            {
                'month': str(last_data.date.year)+'-'+str(last_data.date.month),
                'value': last_data.grade
            }
        )

    getcontext().prec = 5

    #current data
    current_date = datetime.date.today()
    current_data = {'month': str(current_date.year)+'-'+str(current_date.month), 'value': xindex_business_unit}

    #compare the xindex last month with the current xindex month
    if len(historical_months) < 3:
        if len(historical_months) == 2:
            last_month = historical_months[1]
        elif len(historical_months) == 1:
            last_month = historical_months[0]
        elif len(historical_months) == 0:
            #create an object of the last month
            if current_date.month == 01:
                month = 12
                year = current_date.year - 1
            else:
                month = current_date.month - 1
                year = current_date.year
            last_month = {
                'month': str(year)+'-'+str(month),
                'value': Decimal(0)
            }
            #historical_months.append(last_month)
    else:
        last_month = historical_months[2]

    if last_month['value'] > current_data['value']:
        xindex_diff = last_month['value'] - current_data['value']
        diff_type = 'negative'
    else:
        diff_type = 'positive'
        xindex_diff = current_data['value'] - last_month['value']

    ##############

    ##GET DATA TO COMPARE##
    comparative_data = []
    subsidiaries = zone.subsidiary_set.exclude(id=subsidiary.id)
    if len(subsidiaries) == 0:
        there_are_subsidiaries = False
    if len(subsidiaries) > 0:
        for subsidiary_c in subsidiaries:

            promoters_c = 0
            promoters_percent_c = 0
            passives_c = 0
            passives_percent_c = 0
            detractors_c = 0
            detractors_percent_c = 0
            xindex_service_c = 0
            total_surveyed_c = 0
            total_answers_c = []
            for s_bu in SubsidiaryBusinessUnit.objects.filter(id_subsidiary=subsidiary_c, id_business_unit=business_unit):
                for s_bu_s in sbu_service.objects.filter(id_subsidiaryBU=s_bu):
                    for s_bu_s_m in sbu_service_moment.objects.filter(id_sbu_service=s_bu_s).order_by('id_moment'):
                        for s_bu_s_m_a in sbu_service_moment_attribute.objects.filter(id_sbu_service_moment=s_bu_s_m):
                            for s_bu_s_m_a_q in s_bu_s_m_a.question_sbu_s_m_a_set.all():
                                attrib_answers = Answer.objects.filter(question=s_bu_s_m_a_q.question_id)

                                for answer in attrib_answers:
                                    client = Client.objects.get(pk=int(answer.client.id))
                                    try:
                                        client_activity = ClientActivity.objects.get(client=client, subsidiary=subsidiary_c, business_unit=business_unit)
                                        if client_activity.subsidiary == subsidiary_c and client_activity.business_unit == business_unit:
                                            total_answers_c.append(answer)
                                    except ClientActivity.DoesNotExist:
                                        pass

            if not len(total_answers_c) == 0:
                for answer_service in total_answers_c:
                    #total answers for service
                    total_surveyed_c += 1
                    if answer_service.value == 10 or answer_service.value == 9:
                        promoters_c += 1
                    elif answer_service.value == 8 or answer_service.value == 7:
                        passives_c += 1
                    elif 1 <= answer_service.value <= 6:
                        detractors_c += 1

            getcontext().prec = 5
            if not promoters_c == 0:
                promoters_percent_c = Decimal(promoters_c*100)/Decimal(len(total_answers_c))

            if not passives_c == 0:
                passives_percent_c = Decimal(passives_c*100)/Decimal(len(total_answers_c))

            if not detractors_c == 0:
                detractors_percent_c = Decimal(detractors_c*100)/Decimal(len(total_answers_c))

            if promoters_percent_c == 0 and passives_percent_c == 0 and detractors_percent_c == 0:
                xindex_service_c = 0
            else:
                xindex_service_c = (Decimal(promoters_percent_c)-Decimal(detractors_percent_c))

            r = lambda: random.randint(0, 255)

            comparative_data.append(
                {
                    #xindex for moment
                    'xindex_business_unit': xindex_service_c,
                    'subsidiary': subsidiary_c,
                    'color': ('#%02X%02X%02X' % (r(), r(), r()))
                }
            )
    ##------------------##

    template_vars = {
        #data for business unit
        'xindex_business_unit': xindex_business_unit,
        'historical_months': historical_months,
        'current_data': current_data,
        'comparison': {'xindex_diff': xindex_diff, 'diff_type': diff_type},
        #data for relation?
        'survey_is_designed': survey_is_designed,
        #current list values
        'current_zone': zone,
        'current_subsidiary': subsidiary,
        'current_business_unit': business_unit,
        #services data
        'services_data': services_data,
        #lists
        'zones': zones_list,
        'subsidiaries': subsidiaries_list,
        'business_units': business_units_list,
        #comparative data
        'comparative_data': comparative_data
    }
    request_context = RequestContext(request, template_vars)
    return render(request, 'reports/business-unit-report.html', request_context)


@login_required(login_url='/signin/')
def report_by_subsidiary(request):
    #data for subsidiary
    xindex_subsidiary = 0
    promoters_percent = 0
    passives_percent = 0
    detractors_percent = 0
    #lists
    zones_list = Zone.objects.all()
    subsidiaries_list = []
    #business units data
    business_units_data = []
    #data for relation?
    survey_is_designed = True
    c_d = datetime.date.today()
    if request.POST:
        if 'zone' in request.POST:
            zone = Zone.objects.get(active=True, pk=int(request.POST['zone']))
            if 'subsidiary' in request.POST:
                subsidiary = Subsidiary.objects.get(active=True, pk=int(request.POST['subsidiary']))
            else:
                subsidiary = False
    else:
        zone = Zone.objects.filter(active=True)[0]

        subsidiary = zone.subsidiary_set.filter(active=True)[0]

    #Get subsidiaries
    subsidiaries_list = zone.subsidiary_set.all()

    #Get data for subsidiary business units
    total_promoters = 0
    total_passives = 0
    total_detractors = 0
    total_surveyed = 0
    #relation between subsidiary and business unit
    if len(SubsidiaryBusinessUnit.objects.filter(id_subsidiary=subsidiary)) == 0:
        survey_is_designed = False
    for s_bu in SubsidiaryBusinessUnit.objects.filter(id_subsidiary=subsidiary).order_by('id_business_unit'):
        #All business units for subsidiaries
        total_answers_by_business_unit = []
        promoters_business_unit = 0
        promoters_percent_business_unit = 0
        passives_business_unit = 0
        passives_percent_business_unit = 0
        detractors_business_unit = 0
        detractors_percent_business_unit = 0
        xindex_business_unit = 0

        for s_bu_s in sbu_service.objects.filter(id_subsidiaryBU=s_bu):
            for s_bu_s_m in sbu_service_moment.objects.filter(id_sbu_service=s_bu_s).order_by('id_moment'):
                for s_bu_s_m_a in sbu_service_moment_attribute.objects.filter(id_sbu_service_moment=s_bu_s_m):
                    for s_bu_s_m_a_q in s_bu_s_m_a.question_sbu_s_m_a_set.all():
                        attrib_answers = Answer.objects.filter(question=s_bu_s_m_a_q.question_id)

                        for answer in attrib_answers:
                            client = Client.objects.get(pk=int(answer.client.id))
                            try:
                                #client_activity = client.clientactivity_set.get(subsidiary=subsidiary)
                                client_activity = ClientActivity.objects.get(client=client, subsidiary=subsidiary)
                                if client_activity.subsidiary == subsidiary and client_activity.subsidiary.zone == zone and answer.date.year == c_d.year and answer.date.month == c_d.month:
                                    total_answers_by_business_unit.append(answer)
                            except ClientActivity.DoesNotExist:
                                pass

        if not len(total_answers_by_business_unit) == 0:
            for answer_business_unit in total_answers_by_business_unit:
                #total answers for subsidiary
                total_surveyed += 1
                if answer_business_unit.value == 10 or answer_business_unit.value == 9:
                    promoters_business_unit += 1
                    #promoters for subsidiary
                    total_promoters += 1
                elif answer_business_unit.value == 8 or answer_business_unit.value == 7:
                    passives_business_unit += 1
                    #passives for subsidiary
                    total_passives += 1
                elif 1 <= answer_business_unit.value <= 6:
                    detractors_business_unit += 1
                    #detractors for subsidiary
                    total_detractors += 1

        getcontext().prec = 5

        if not promoters_business_unit == 0:
            promoters_percent_business_unit = Decimal(promoters_business_unit*100)/Decimal(len(total_answers_by_business_unit))

        if not passives_business_unit == 0:
            passives_percent_business_unit = Decimal(passives_business_unit*100)/Decimal(len(total_answers_by_business_unit))

        if not detractors_business_unit == 0:
            detractors_percent_business_unit  = Decimal(detractors_business_unit*100)/Decimal(len(total_answers_by_business_unit))

        if promoters_percent_business_unit != 0 and passives_percent_business_unit != 0 and detractors_percent_business_unit != 0:
            #check this operation
            xindex_business_unit = Decimal(promoters_percent_business_unit-detractors_percent_business_unit)

        r = lambda: random.randint(0, 255)

        business_units_data.append(
            {
                #xindex for business unit
                'xindex_business_unit': xindex_business_unit,
                #info
                'business_unit_id': s_bu.id_business_unit.id,
                'business_unit_name': s_bu.id_business_unit.name,
                #data
                'promoters': promoters_percent_business_unit,
                'passives': passives_percent_business_unit,
                'detractors': detractors_percent_business_unit,
                #extra
                'color': ('#%02X%02X%02X' % (r(), r(), r()))
            }
        )

    #Calculate the subsidiary data
    getcontext().prec = 5

    if total_promoters != 0 and total_surveyed != 0:
        promoters_percent = Decimal(total_promoters*100)/Decimal(total_surveyed)

    if total_passives != 0 and total_surveyed != 0:
        passives_percent = Decimal(total_passives*100)/Decimal(total_surveyed)

    if total_detractors != 0 and total_surveyed != 0:
        detractors_percent = Decimal(total_detractors*100)/Decimal(total_surveyed)

    if promoters_percent != 0 and passives_percent != 0 and detractors_percent != 0:
        #xindex_service = ((Decimal(promoters_percent-detractors_percent))/(Decimal(promoters_percent+passives_percent+detractors_percent)))*Decimal(100)
        xindex_subsidiary = Decimal(promoters_percent-detractors_percent)

    ##############

    historical_data = Cumulative_Report.objects.filter(
        id_subsidiary=subsidiary, id_business_unit=None,
        id_service=None, id_moment=None, id_attribute=None
    ).order_by('-date')[:3]

    historical_months = []

    for last_data in reversed(historical_data):
        historical_months.append(
            {
                'month': str(last_data.date.year)+'-'+str(last_data.date.month),
                'value': last_data.grade
            }
        )

    getcontext().prec = 5

    #current data
    current_data = {'month': str(c_d.year)+'-'+str(c_d.month), 'value': xindex_subsidiary}

    #compare the xindex last month with the current xindex month
    if len(historical_months) < 3:
        if len(historical_months) == 2:
            last_month = historical_months[1]
        elif len(historical_months) == 1:
            last_month = historical_months[0]
        elif len(historical_months) == 0:
            #create an object of the last month
            current_date = datetime.date.today()
            if current_date.month == 01:
                month = 12
                year = current_date.year - 1
            else:
                month = current_date.month - 1
                year = current_date.year
            last_month = {
                'month': str(year)+'-'+str(month),
                'value': Decimal(0)
            }
            #historical_months.append(last_month)
    else:
        last_month = historical_months[2]

    if last_month['value'] > current_data['value']:
        xindex_diff = last_month['value'] - current_data['value']
        diff_type = 'negative'
    else:
        diff_type = 'positive'
        xindex_diff = current_data['value'] - last_month['value']

    ##############

    ##GET DATA TO COMPARE##
    comparative_data = []
    subsidiaries = zone.subsidiary_set.exclude(id=subsidiary.id)

    if len(subsidiaries) > 0:
        for subsidiary_c in subsidiaries:

            promoters_c = 0
            promoters_percent_c = 0
            passives_c = 0
            passives_percent_c = 0
            detractors_c = 0
            detractors_percent_c = 0
            xindex_service_c = 0
            total_surveyed_c = 0
            total_answers_c = []
            for s_bu in SubsidiaryBusinessUnit.objects.filter(id_subsidiary=subsidiary_c):
                for s_bu_s in sbu_service.objects.filter(id_subsidiaryBU=s_bu):
                    for s_bu_s_m in sbu_service_moment.objects.filter(id_sbu_service=s_bu_s).order_by('id_moment'):
                        for s_bu_s_m_a in sbu_service_moment_attribute.objects.filter(id_sbu_service_moment=s_bu_s_m):
                            for s_bu_s_m_a_q in s_bu_s_m_a.question_sbu_s_m_a_set.all():
                                attrib_answers = Answer.objects.filter(question=s_bu_s_m_a_q.question_id)

                                for answer in attrib_answers:
                                    client = Client.objects.get(pk=int(answer.client.id))
                                    try:
                                        client_activity = ClientActivity.objects.get(client=client, subsidiary=subsidiary_c)
                                        if client_activity.subsidiary == subsidiary_c:
                                            total_answers_c.append(answer)
                                    except ClientActivity.DoesNotExist:
                                        pass

            if not len(total_answers_c) == 0:
                for answer_service in total_answers_c:
                    #total answers for service
                    total_surveyed_c += 1
                    if answer_service.value == 10 or answer_service.value == 9:
                        promoters_c += 1
                    elif answer_service.value == 8 or answer_service.value == 7:
                        passives_c += 1
                    elif 1 <= answer_service.value <= 6:
                        detractors_c += 1

            getcontext().prec = 5
            if not promoters_c == 0:
                promoters_percent_c = Decimal(promoters_c*100)/Decimal(len(total_answers_c))

            if not passives_c == 0:
                passives_percent_c = Decimal(passives_c*100)/Decimal(len(total_answers_c))

            if not detractors_c == 0:
                detractors_percent_c = Decimal(detractors_c*100)/Decimal(len(total_answers_c))

            if promoters_percent_c == 0 and passives_percent_c == 0 and detractors_percent_c == 0:
                xindex_service_c = 0
            else:
                xindex_service_c = (Decimal(promoters_percent_c)-Decimal(detractors_percent_c))

            r = lambda: random.randint(0, 255)

            comparative_data.append(
                {
                    #xindex for moment
                    'xindex_subsidiary': xindex_service_c,
                    'subsidiary': subsidiary_c,
                    'color': ('#%02X%02X%02X' % (r(), r(), r()))
                }
            )
    ##------------------##

    template_vars = {
        #data for subsidiary
        'xindex_subsidiary': xindex_subsidiary,
        'historical_months': historical_months,
        'current_data': current_data,
        'comparison': {'xindex_diff': xindex_diff, 'diff_type': diff_type},
        #data for relation?
        'survey_is_designed': survey_is_designed,
        #current list values
        'current_zone': zone,
        'current_subsidiary': subsidiary,
        #services data
        'business_units_data': business_units_data,
        #lists
        'zones': zones_list,
        'subsidiaries': subsidiaries_list,
        #comparative data
        'comparative_data': comparative_data
    }
    request_context = RequestContext(request, template_vars)
    return render(request, 'reports/subsidiary-report.html', request_context)


@login_required(login_url='/signin/')
def report_by_zone(request):
    #data for zone
    xindex_zone = 0
    promoters_percent = 0
    passives_percent = 0
    detractors_percent = 0
    #lists
    zones_list = Zone.objects.all()
    #subsidiaries data
    subsidiaries_data = []
    #data for relation?
    survey_is_designed = True
    #current date
    c_d = datetime.date.today()
    if request.POST:
        if 'zone' in request.POST:
            zone = Zone.objects.get(active=True, pk=int(request.POST['zone']))
    else:
        zone = Zone.objects.filter(active=True)[0]

    if len(Zone.objects.filter(active=True)) == 0:
        template_vars = {
            #not data
            'empty_data': True
        }
        request_context = RequestContext(request, template_vars)
        return render(request, 'reports/zone-report.html', request_context)


    #Get data for zone subsidiaries
    total_promoters = 0
    total_passives = 0
    total_detractors = 0
    total_surveyed = 0
    #relation between subsidiary and business unit
    if len(zone.subsidiary_set.filter(active=True)) == 0:
        survey_is_designed = False
    for subsidiary in zone.subsidiary_set.filter(active=True).order_by('id'):

        #All subsidiaries for zone
        total_answers_by_subsidiary = []
        promoters_subsidiary = 0
        promoters_percent_subsidiary = 0
        passives_subsidiary = 0
        passives_percent_subsidiary = 0
        detractors_subsidiary = 0
        detractors_percent_subsidiary = 0
        xindex_subsidiary = 0

        for s_bu in SubsidiaryBusinessUnit.objects.filter(id_subsidiary=subsidiary):
            for s_bu_s in sbu_service.objects.filter(id_subsidiaryBU=s_bu):
                for s_bu_s_m in sbu_service_moment.objects.filter(id_sbu_service=s_bu_s).order_by('id_moment'):
                    for s_bu_s_m_a in sbu_service_moment_attribute.objects.filter(id_sbu_service_moment=s_bu_s_m):
                        for s_bu_s_m_a_q in s_bu_s_m_a.question_sbu_s_m_a_set.all():
                            attrib_answers = Answer.objects.filter(question=s_bu_s_m_a_q.question_id)

                            for answer in attrib_answers:
                                client = Client.objects.get(pk=int(answer.client.id))
                                try:
                                    #client_activity = client.clientactivity_set.get(subsidiary=subsidiary)
                                    client_activity = ClientActivity.objects.get(client=client, subsidiary=subsidiary)
                                    if client_activity.subsidiary == subsidiary and client_activity.subsidiary.zone == zone and c_d.month == answer.date.month and c_d.year == answer.date.year:
                                        total_answers_by_subsidiary.append(answer)
                                except ClientActivity.DoesNotExist:
                                    pass

        if not len(total_answers_by_subsidiary) == 0:
            for answer_subsidiary in total_answers_by_subsidiary:
                #total answers for zone
                total_surveyed += 1
                if answer_subsidiary.value == 10 or answer_subsidiary.value == 9:
                    promoters_subsidiary += 1
                    #promoters for zone
                    total_promoters += 1
                elif answer_subsidiary.value == 8 or answer_subsidiary.value == 7:
                    passives_subsidiary += 1
                    #passives for zone
                    total_passives += 1
                elif 1 <= answer_subsidiary.value <= 6:
                    detractors_subsidiary += 1
                    #detractors for zone
                    total_detractors += 1

        getcontext().prec = 5

        if not promoters_subsidiary == 0:
            promoters_percent_subsidiary = Decimal(promoters_subsidiary*100)/Decimal(len(total_answers_by_subsidiary))

        if not passives_subsidiary == 0:
            passives_percent_subsidiary = Decimal(passives_subsidiary*100)/Decimal(len(total_answers_by_subsidiary))

        if not detractors_subsidiary == 0:
            detractors_percent_subsidiary = Decimal(detractors_subsidiary*100)/Decimal(len(total_answers_by_subsidiary))

        if promoters_percent_subsidiary != 0 and passives_percent_subsidiary != 0 and detractors_percent_subsidiary != 0:
            #check this operation
            xindex_subsidiary = Decimal(promoters_percent_subsidiary-detractors_percent_subsidiary)

        r = lambda: random.randint(0, 255)
        print()

        subsidiaries_data.append(
            {
                #xindex for subsidiary
                'xindex_subsidiary': xindex_subsidiary,
                #info
                'subsidiary_id': subsidiary.id,
                'subsidiary_name': subsidiary.name,
                #data
                'promoters': promoters_percent_subsidiary,
                'passives': passives_percent_subsidiary,
                'detractors': detractors_percent_subsidiary,
                #extra
                'color': ('#%02X%02X%02X' % (r(), r(), r()))
            }
        )

    #Calculate the zone data
    getcontext().prec = 5

    if total_promoters != 0 and total_surveyed != 0:
        promoters_percent = Decimal(total_promoters*100)/Decimal(total_surveyed)

    if total_passives != 0 and total_surveyed != 0:
        passives_percent = Decimal(total_passives*100)/Decimal(total_surveyed)

    if total_detractors != 0 and total_surveyed != 0:
        detractors_percent = Decimal(total_detractors*100)/Decimal(total_surveyed)

    if promoters_percent != 0 and passives_percent != 0 and detractors_percent != 0:
        #xindex_service = ((Decimal(promoters_percent-detractors_percent))/(Decimal(promoters_percent+passives_percent+detractors_percent)))*Decimal(100)
        xindex_zone = Decimal(promoters_percent-detractors_percent)

    ##############
    historical_months = [
        {'month': '2013-07', 'value': Decimal(21.67)},
        {'month': '2013-08', 'value': Decimal(85.78)},
        {'month': '2013-09', 'value': Decimal(48.51)}
    ]

    getcontext().prec = 5

    #current data
    current_data = {'month': '2013-10', 'value': xindex_zone}

    #compare the xindex last month with the current xindex month
    if len(historical_months) < 3:
        if len(historical_months) == 2:
            last_month = historical_months[1]
        elif len(historical_months) == 1:
            last_month = historical_months[0]
        elif len(historical_months) == 0:
            #create an object of the last month
            current_date = datetime.date.today()
            if current_date.month == 01:
                month = 12
                year = current_date.year - 1
            else:
                month = current_date.month - 1
                year = current_date.year
            last_month = {
                'month': str(year)+'-'+str(month),
                'value': Decimal(0)
            }
            #historical_months.append(last_month)
    else:
        last_month = historical_months[2]

    if last_month['value'] > current_data['value']:
        xindex_diff = last_month['value'] - current_data['value']
        diff_type = 'negative'
    else:
        diff_type = 'positive'
        xindex_diff = current_data['value'] - last_month['value']

    ##############

    ##GET DATA TO COMPARE##
    comparative_data = []
    user = Xindex_User.objects.get(user=request.user.id)
    company = user.company_set.all()[0]
    zones = company.zone.exclude(id=zone.id)

    for zone_c in zones:
        promoters_c = 0
        promoters_percent_c = 0
        passives_c = 0
        passives_percent_c = 0
        detractors_c = 0
        detractors_percent_c = 0
        xindex_zone_c = 0
        total_surveyed_c = 0
        total_answers_c = []
        subsidiaries = zone_c.subsidiary_set.all()
        if len(subsidiaries) > 0:
            for subsidiary_c in subsidiaries:
                for s_bu in SubsidiaryBusinessUnit.objects.filter(id_subsidiary=subsidiary_c):
                    for s_bu_s in sbu_service.objects.filter(id_subsidiaryBU=s_bu):
                        for s_bu_s_m in sbu_service_moment.objects.filter(id_sbu_service=s_bu_s).order_by('id_moment'):
                            for s_bu_s_m_a in sbu_service_moment_attribute.objects.filter(id_sbu_service_moment=s_bu_s_m):
                                for s_bu_s_m_a_q in s_bu_s_m_a.question_sbu_s_m_a_set.all():
                                    attrib_answers = Answer.objects.filter(question=s_bu_s_m_a_q.question_id)

                                    for answer in attrib_answers:
                                        client = Client.objects.get(pk=int(answer.client.id))
                                        try:
                                            client_activity = ClientActivity.objects.get(client=client, subsidiary=subsidiary_c)
                                            if client_activity.subsidiary == subsidiary_c and answer.date.year == c_d.year and answer.date.month == c_d.month:
                                                total_answers_c.append(answer)
                                        except ClientActivity.DoesNotExist:
                                            pass

        if not len(total_answers_c) == 0:
            for answer_zone in total_answers_c:
                #total answers for zone
                total_surveyed_c += 1
                if answer_zone.value == 10 or answer_zone.value == 9:
                    promoters_c += 1
                elif answer_zone.value == 8 or answer_zone.value == 7:
                    passives_c += 1
                elif 1 <= answer_zone.value <= 6:
                    detractors_c += 1

        getcontext().prec = 5
        if not promoters_c == 0:
            promoters_percent_c = Decimal(promoters_c*100)/Decimal(len(total_answers_c))

        if not passives_c == 0:
            passives_percent_c = Decimal(passives_c*100)/Decimal(len(total_answers_c))

        if not detractors_c == 0:
            detractors_percent_c = Decimal(detractors_c*100)/Decimal(len(total_answers_c))

        if promoters_percent_c == 0 and passives_percent_c == 0 and detractors_percent_c == 0:
            pass
        else:
            xindex_zone_c = (Decimal(promoters_percent_c)-Decimal(detractors_percent_c))

        r = lambda: random.randint(0, 255)

        comparative_data.append(
            {
                #xindex for moment
                'xindex_zone': xindex_zone_c,
                'zone': zone_c,
                'color': ('#%02X%02X%02X' % (r(), r(), r()))
            }
        )
    ##------------------##

    template_vars = {
        #data for zone
        'xindex_zone': xindex_zone,
        'historical_months': historical_months,
        'current_data': current_data,
        'comparison': {'xindex_diff': xindex_diff, 'diff_type': diff_type},
        #data for relation?
        'survey_is_designed': survey_is_designed,
        #current list values
        'current_zone': zone,
        #subsidiaries data
        'subsidiaries_data': subsidiaries_data,
        #lists
        'zones': zones_list,
        #comparative data
        'comparative_data': comparative_data
    }
    request_context = RequestContext(request, template_vars)
    return render(request, 'reports/zone-report.html', request_context)


@login_required(login_url='/signin/')
def general_report(request):
    #data for company
    xindex_company = 0
    promoters_percent = 0
    passives_percent = 0
    detractors_percent = 0
    #zones data
    zones_data = []
    #data for relation?
    survey_is_designed = True

    user = Xindex_User.objects.get(user=request.user.id)

    #Get data for zone subsidiaries
    total_promoters = 0
    total_passives = 0
    total_detractors = 0
    total_surveyed = 0
    company = user.company_set.get()
    if len(user.company_set.all()) == 0:
        survey_is_designed = False
    for zone in company.zone.all():
        #All zones for company
        total_answers_by_zone = []
        promoters_zone = 0
        promoters_percent_zone = 0
        passives_zone = 0
        passives_percent_zone = 0
        detractors_zone = 0
        detractors_percent_zone = 0
        xindex_zone = 0
        for subsidiary in zone.subsidiary_set.filter(active=True).order_by('id'):
            for s_bu in SubsidiaryBusinessUnit.objects.filter(id_subsidiary=subsidiary):
                for s_bu_s in sbu_service.objects.filter(id_subsidiaryBU=s_bu):
                    for s_bu_s_m in sbu_service_moment.objects.filter(id_sbu_service=s_bu_s).order_by('id_moment'):
                        for s_bu_s_m_a in sbu_service_moment_attribute.objects.filter(id_sbu_service_moment=s_bu_s_m):
                            for s_bu_s_m_a_q in s_bu_s_m_a.question_sbu_s_m_a_set.all():
                                attrib_answers = Answer.objects.filter(question=s_bu_s_m_a_q.question_id)

                                for answer in attrib_answers:
                                    client = Client.objects.get(pk=int(answer.client.id))
                                    try:
                                        #client_activity = client.clientactivity_set.get(company=company)
                                        c_d = datetime.date.today()
                                        client_activity = ClientActivity.objects.get(client=client, subsidiary=subsidiary)
                                        if c_d.year == answer.date.year and c_d.month == answer.date.month:
                                            total_answers_by_zone.append(answer)
                                            print 'Today is '+str(c_d.day)+' from '+str(c_d.month)+' from '+str(c_d.year)
                                            print 'Question date is '+str(answer.date.day)+' from '+str(answer.date.month)+' from '+str(answer.date.year)
                                    except ClientActivity.DoesNotExist:
                                        pass

        if not len(total_answers_by_zone) == 0:
            for answer_zone in total_answers_by_zone:
                #total answers for company
                total_surveyed += 1
                if answer_zone.value == 10 or answer_zone.value == 9:
                    promoters_zone += 1
                    #promoters for company
                    total_promoters += 1
                elif answer_zone.value == 8 or answer_zone.value == 7:
                    passives_zone += 1
                    #passives for company
                    total_passives += 1
                elif 1 <= answer_zone.value <= 6:
                    detractors_zone += 1
                    #detractors for company
                    total_detractors += 1

        getcontext().prec = 5

        if not promoters_zone == 0:
            promoters_percent_zone = Decimal(promoters_zone*100)/Decimal(len(total_answers_by_zone))

        if not passives_zone == 0:
            passives_percent_zone = Decimal(passives_zone*100)/Decimal(len(total_answers_by_zone))

        if not detractors_zone == 0:
            detractors_percent_zone = Decimal(detractors_zone*100)/Decimal(len(total_answers_by_zone))

        if promoters_percent_zone != 0 and passives_percent_zone != 0 and detractors_percent_zone != 0:
            #check this operation
            xindex_zone = Decimal(promoters_percent_zone-detractors_percent_zone)

        r = lambda: random.randint(0, 255)
        print()

        zones_data.append(
            {
                #xindex for zone
                'xindex_zone': xindex_zone,
                #info
                'zone_id':zone.id,
                'zone_name': zone.name,
                #data
                'promoters': promoters_percent_zone,
                'passives': passives_percent_zone,
                'detractors': detractors_percent_zone,
                #extra
                'color': ('#%02X%02X%02X' % (r(), r(), r()))
            }
        )

    #Calculate the company data
    getcontext().prec = 5

    if total_promoters != 0 and total_surveyed != 0:
        promoters_percent = Decimal(total_promoters*100)/Decimal(total_surveyed)

    if total_passives != 0 and total_surveyed != 0:
        passives_percent = Decimal(total_passives*100)/Decimal(total_surveyed)

    if total_detractors != 0 and total_surveyed != 0:
        detractors_percent = Decimal(total_detractors*100)/Decimal(total_surveyed)

    if promoters_percent != 0 and passives_percent != 0 and detractors_percent != 0:
        #xindex_service = ((Decimal(promoters_percent-detractors_percent))/(Decimal(promoters_percent+passives_percent+detractors_percent)))*Decimal(100)
        xindex_company = Decimal(promoters_percent-detractors_percent)

    ##############
    historical_months = [
        {'month': '2013-07', 'value': Decimal(21.67)},
        {'month': '2013-08', 'value': Decimal(85.78)},
        {'month': '2013-09', 'value': Decimal(48.51)}
    ]

    getcontext().prec = 5

    #current data
    current_data = {'month': '2013-10', 'value': xindex_company}

    #compare the xindex last month with the current xindex month
    if len(historical_months) < 3:
        if len(historical_months) == 2:
            last_month = historical_months[1]
        elif len(historical_months) == 1:
            last_month = historical_months[0]
        elif len(historical_months) == 0:
            #create an object of the last month
            current_date = datetime.date.today()
            if current_date.month == 01:
                month = 12
                year = current_date.year - 1
            else:
                month = current_date.month - 1
                year = current_date.year
            last_month = {
                'month': str(year)+'-'+str(month),
                'value': Decimal(0)
            }
            #historical_months.append(last_month)
    else:
        last_month = historical_months[2]

    if last_month['value'] > current_data['value']:
        xindex_diff = last_month['value'] - current_data['value']
        diff_type = 'negative'
    else:
        diff_type = 'positive'
        xindex_diff = current_data['value'] - last_month['value']

    ##############

    template_vars = {
        #data for company
        'company_name': company.name,
        'xindex_company': xindex_company,
        'historical_months': historical_months,
        'current_data': current_data,
        'comparison': {'xindex_diff': xindex_diff, 'diff_type': diff_type},
        #data for relation?
        'survey_is_designed': survey_is_designed,
        #zones data
        'zones_data': zones_data
    }
    request_context = RequestContext(request, template_vars)
    return render(request, 'reports/general-report.html', request_context)


#################################################################NEW METHODS##################################################################

@login_required(login_url='/signin/')
def report_by_business_unit_not_instances(request):
    #data for business unit
    xindex_business_unit = 0
    promoters_percent = 0
    passives_percent = 0
    detractors_percent = 0
    #lists
    zones_list = Zone.objects.all()
    subsidiaries_list = []
    business_units_list = []
    #services data
    services_data = []
    #data for relation?
    survey_is_designed = True

    c_d = datetime.date.today()
    if request.POST:
        if 'zone' in request.POST:
            if request.POST['zone'] == 'all':
                zone = Zone.objects.filter(active=True)
            else:
                zone = Zone.objects.get(active=True, pk=int(request.POST['zone']))
            if 'subsidiary' in request.POST:
                if request.POST['subsidiary'] == 'all':
                    if isinstance(zone, Zone):
                        subsidiary = zone.subsidiary_set.filter(active=True)
                    else:
                        subsidiary = []
                        for z in zone:
                            for s in z.subsidiary_set.filter(active=True):
                                subsidiary.append(s)
                else:
                    subsidiary = Subsidiary.objects.get(active=True, pk=int(request.POST['subsidiary']))
                if 'business_unit' in request.POST:
                    business_unit = BusinessUnit.objects.get(active=True, pk=int(request.POST['business_unit']))
                else:
                    businessUnit = False
            else:
                subsidiary = False

    #Get subsidiaries
    if isinstance(zone, Zone):
        subsidiaries_list = zone.subsidiary_set.all()
        if isinstance(subsidiary, Subsidiary):
            #Get business units for first subsidiary
            for s_bu in SubsidiaryBusinessUnit.objects.filter(id_subsidiary=subsidiary):
                if len(business_units_list) > 0:
                    coincidences_bu = 0
                    for b_u in business_units_list:
                        if b_u == s_bu.id_business_unit:
                            coincidences_bu += 1
                    if coincidences_bu == 0:
                        business_units_list.append(s_bu.id_business_unit)
                else:
                    business_units_list.append(s_bu.id_business_unit)
        else:
            for s in zone.subsidiary_set.filter(active=True):
                for s_bu in SubsidiaryBusinessUnit.objects.filter(id_subsidiary=s):
                    if len(business_units_list) > 0:
                        coincidences_bu = 0
                        for b_u in business_units_list:
                            if b_u == s_bu.id_business_unit:
                                coincidences_bu += 1
                        if coincidences_bu == 0:
                            business_units_list.append(s_bu.id_business_unit)
                    else:
                        business_units_list.append(s_bu.id_business_unit)
    else:
        subsidiaries_list = []
        for z in zone:
            for s in z.subsidiary_set.filter(active=True):
                for s_bu in SubsidiaryBusinessUnit.objects.filter(id_subsidiary=s):
                    if len(business_units_list) > 0:
                        coincidences_bu = 0
                        for b_u in business_units_list:
                            if b_u == s_bu.id_business_unit:
                                coincidences_bu += 1
                        if coincidences_bu == 0:
                            business_units_list.append(s_bu.id_business_unit)
                    else:
                        business_units_list.append(s_bu.id_business_unit)

    ###############################################################################

    #Get data for business unit services
    total_promoters = 0
    total_passives = 0
    total_detractors = 0
    total_surveyed = 0
    #relation between subsidiary and business unit
    if isinstance(subsidiary, Subsidiary):
        s_bu = SubsidiaryBusinessUnit.objects.get(id_subsidiary=subsidiary, id_business_unit=business_unit)
        if len(sbu_service.objects.filter(id_subsidiaryBU=s_bu)) == 0:
            survey_is_designed = False
        for s_bu_s in sbu_service.objects.filter(id_subsidiaryBU=s_bu).order_by('id_service'):
            #All services for all business unit
            total_answers_by_service = []
            promoters_service = 0
            promoters_percent_service = 0
            passives_service = 0
            passives_percent_service = 0
            detractors_service = 0
            detractors_percent_service = 0
            xindex_service = 0

            for s_bu_s_m in sbu_service_moment.objects.filter(id_sbu_service=s_bu_s).order_by('id_moment'):
                for s_bu_s_m_a in sbu_service_moment_attribute.objects.filter(id_sbu_service_moment=s_bu_s_m):
                    for s_bu_s_m_a_q in s_bu_s_m_a.question_sbu_s_m_a_set.all():
                        attrib_answers = Answer.objects.filter(question=s_bu_s_m_a_q.question_id)

                        for answer in attrib_answers:
                            client = Client.objects.get(pk=int(answer.client.id))
                            try:
                                client_activity = ClientActivity.objects.get(client=client, subsidiary=subsidiary, business_unit=business_unit)
                                if client_activity.subsidiary == subsidiary and client_activity.business_unit == business_unit and answer.date.year == c_d.year and answer.date.month == c_d.month:
                                    total_answers_by_service.append(answer)
                            except ClientActivity.DoesNotExist:
                                pass

            if not len(total_answers_by_service) == 0:
                for answer_service in total_answers_by_service:
                    #total answers for service
                    total_surveyed += 1
                    if answer_service.value == 10 or answer_service.value == 9:
                        promoters_service += 1
                        #promoters for business unit
                        total_promoters += 1
                    elif answer_service.value == 8 or answer_service.value == 7:
                        passives_service += 1
                        #passives for business unit
                        total_passives += 1
                    elif 1 <= answer_service.value <= 6:
                        detractors_service += 1
                        #detractors for business unit
                        total_detractors += 1

            getcontext().prec = 5

            if not promoters_service == 0:
                promoters_percent_service = Decimal(promoters_service*100)/Decimal(len(total_answers_by_service))

            if not passives_service == 0:
                passives_percent_service = Decimal(passives_service*100)/Decimal(len(total_answers_by_service))

            if not detractors_service == 0:
                detractors_percent_service  = Decimal(detractors_service*100)/Decimal(len(total_answers_by_service))

            if promoters_percent_service != 0 and passives_percent_service != 0 and detractors_percent_service != 0:
                #xindex_service = ((Decimal(promoters_percent_service-detractors_percent_service))/(Decimal(promoters_percent_service+passives_percent_service+detractors_percent_service)))*Decimal(100)
                xindex_service = Decimal(promoters_percent_service-detractors_percent_service)

            r = lambda: random.randint(0, 255)

            services_data.append(
                {
                    #xindex for moment
                    'xindex_service': xindex_service,
                    #info
                    'service_id': s_bu_s.id_service.id,
                    'service_name': s_bu_s.id_service.name,
                    #data
                    'promoters': promoters_percent_service,
                    'passives': passives_percent_service,
                    'detractors': detractors_percent_service,
                    #extra
                    'color': ('#%02X%02X%02X' % (r(), r(), r()))
                }
            )
    else:
        for subsidiary_a in subsidiary:
            try:
                s_bu = SubsidiaryBusinessUnit.objects.get(id_subsidiary=subsidiary_a, id_business_unit=business_unit)
                if len(sbu_service.objects.filter(id_subsidiaryBU=s_bu)) == 0:
                    survey_is_designed = False
                for s_bu_s in sbu_service.objects.filter(id_subsidiaryBU=s_bu).order_by('id_service'):
                    #All services for all business unit
                    total_answers_by_service = []
                    promoters_service = 0
                    promoters_percent_service = 0
                    passives_service = 0
                    passives_percent_service = 0
                    detractors_service = 0
                    detractors_percent_service = 0
                    xindex_service = 0

                    for s_bu_s_m in sbu_service_moment.objects.filter(id_sbu_service=s_bu_s).order_by('id_moment'):
                        for s_bu_s_m_a in sbu_service_moment_attribute.objects.filter(id_sbu_service_moment=s_bu_s_m):
                            for s_bu_s_m_a_q in s_bu_s_m_a.question_sbu_s_m_a_set.all():
                                attrib_answers = Answer.objects.filter(question=s_bu_s_m_a_q.question_id)

                                for answer in attrib_answers:
                                    client = Client.objects.get(pk=int(answer.client.id))
                                    try:
                                        client_activity = ClientActivity.objects.get(client=client, subsidiary=subsidiary_a, business_unit=business_unit)
                                        if client_activity.subsidiary == subsidiary_a and client_activity.business_unit == business_unit and answer.date.year == c_d.year and answer.date.month == c_d.month:
                                            total_answers_by_service.append(answer)
                                    except ClientActivity.DoesNotExist:
                                        pass

                    if not len(total_answers_by_service) == 0:
                        for answer_service in total_answers_by_service:
                            #total answers for service
                            total_surveyed += 1
                            if answer_service.value == 10 or answer_service.value == 9:
                                promoters_service += 1
                                #promoters for business unit
                                total_promoters += 1
                            elif answer_service.value == 8 or answer_service.value == 7:
                                passives_service += 1
                                #passives for business unit
                                total_passives += 1
                            elif 1 <= answer_service.value <= 6:
                                detractors_service += 1
                                #detractors for business unit
                                total_detractors += 1

                    getcontext().prec = 5

                    if not promoters_service == 0:
                        promoters_percent_service = Decimal(promoters_service*100)/Decimal(len(total_answers_by_service))

                    if not passives_service == 0:
                        passives_percent_service = Decimal(passives_service*100)/Decimal(len(total_answers_by_service))

                    if not detractors_service == 0:
                        detractors_percent_service  = Decimal(detractors_service*100)/Decimal(len(total_answers_by_service))

                    if promoters_percent_service != 0 and passives_percent_service != 0 and detractors_percent_service != 0:
                        #xindex_service = ((Decimal(promoters_percent_service-detractors_percent_service))/(Decimal(promoters_percent_service+passives_percent_service+detractors_percent_service)))*Decimal(100)
                        xindex_service = Decimal(promoters_percent_service-detractors_percent_service)

                    r = lambda: random.randint(0, 255)

                    services_data.append(
                        {
                            #xindex for moment
                            'xindex_service': xindex_service,
                            #info
                            'service_id': s_bu_s.id_service.id,
                            'service_name': s_bu_s.id_service.name,
                            #data
                            'promoters': promoters_percent_service,
                            'passives': passives_percent_service,
                            'detractors': detractors_percent_service,
                            #extra
                            'color': ('#%02X%02X%02X' % (r(), r(), r()))
                        }
                    )
            except SubsidiaryBusinessUnit.DoesNotExist:
                pass

    #Calculate the business unit data
    getcontext().prec = 5

    if total_promoters != 0 and total_surveyed != 0:
        promoters_percent = Decimal(total_promoters*100)/Decimal(total_surveyed)

    if total_passives != 0 and total_surveyed != 0:
        passives_percent = Decimal(total_passives*100)/Decimal(total_surveyed)

    if total_detractors != 0 and total_surveyed != 0:
        detractors_percent = Decimal(total_detractors*100)/Decimal(total_surveyed)

    if promoters_percent != 0 and passives_percent != 0 and detractors_percent != 0:
        #xindex_service = ((Decimal(promoters_percent-detractors_percent))/(Decimal(promoters_percent+passives_percent+detractors_percent)))*Decimal(100)
        xindex_business_unit = Decimal(promoters_percent-detractors_percent)

    ##############
    last_xindex = 0
    #create subsidiary ids array
    ids_subs = []
    for subs in subsidiary:
        ids_subs.append(subs.id)
    if c_d.month == 01:
        historical = Cumulative_Report.objects.filter(
            id_subsidiary__in=ids_subs, id_business_unit=business_unit,
            id_service=None, id_moment=None, id_attribute=None,
            date__year=datetime.date.today().year-1, date__month=12
        ).order_by('date')
    else:
        historical = Cumulative_Report.objects.filter(
            id_subsidiary__in=ids_subs, id_business_unit=business_unit,
            id_service=None, id_moment=None, id_attribute=None,
            date__year=datetime.date.today().year, date__month=c_d.month-1
        ).order_by('date')
    #comparing xindex
    comparing_xindex = 0
    for hist in historical:
        #print 'This is the subsidiary: '+hist.id_subsidiary.name+' and this is the business unit: '+hist.id_business_unit.name+' with his xindex: '+str(hist.grade)+' and the date is: '+str(hist.date)
        comparing_xindex += hist.grade
    if len(historical) > 0:
        comparing_xindex = comparing_xindex/len(historical)
    else:
        comparing_xindex = 0

    print comparing_xindex
    #############

    historical_months = []
    if len(historical) > 0:
        if c_d.month == 01:
            historical_months.append(
                {
                    'month': str(c_d.year-1)+'-'+str(12),
                    'value': comparing_xindex
                }
            )
        else:
            historical_months.append(
                {
                    'month': str(c_d.year)+'-'+str(c_d.month-1),
                    'value': comparing_xindex
                }
            )

    getcontext().prec = 5

    #current data
    current_date = datetime.date.today()
    current_data = {'month': str(current_date.year)+'-'+str(current_date.month), 'value': xindex_business_unit}

    #compare the xindex last month with the current xindex month
    if len(historical_months) < 3:
        if len(historical_months) == 2:
            last_month = historical_months[1]
        elif len(historical_months) == 1:
            last_month = historical_months[0]
        elif len(historical_months) == 0:
            #create an object of the last month
            if current_date.month == 01:
                month = 12
                year = current_date.year - 1
            else:
                month = current_date.month - 1
                year = current_date.year
            last_month = {
                'month': str(year)+'-'+str(month),
                'value': Decimal(0)
            }
            #historical_months.append(last_month)
    else:
        last_month = historical_months[2]

    if last_month['value'] > current_data['value']:
        xindex_diff = last_month['value'] - current_data['value']
        diff_type = 'negative'
    else:
        diff_type = 'positive'
        xindex_diff = current_data['value'] - last_month['value']

    print '############################'
    print 'This is the business unit xindex: '+str(xindex_business_unit)
    print 'This is the zone:'
    if isinstance(zone, Zone):
        print str(zone.name)
    else:
        for z in zone:
            print str(z.name)

    for s in subsidiary:
        print str(s.name)
    print historical_months
    print '############################'


    #calculate prom from the services
    for service in services_data:
        pass

    template_vars = {
        #data for business unit
        'xindex_business_unit': xindex_business_unit,
        'historical_months': historical_months,
        'current_data': current_data,
        'comparison': {'xindex_diff': xindex_diff, 'diff_type': diff_type},
        #data for relation?
        'survey_is_designed': survey_is_designed,
        #current list values
        'current_zone': zone,
        'current_subsidiary': subsidiary,
        'current_business_unit': business_unit,
        #services data
        'services_data': services_data,
        #lists
        'zones': zones_list,
        'subsidiaries': subsidiaries_list,
        'business_units': business_units_list,
    }
    request_context = RequestContext(request, template_vars)
    return render(request, 'reports/by-group/business-unit-report-by-group.html', request_context)
