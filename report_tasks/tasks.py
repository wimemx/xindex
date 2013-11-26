from celery import task
from django.http import HttpResponse
from celery.schedules import crontab
from celery.task import periodic_task
from decimal import *
from xindex.models import *
from xindex.models import Moment
import datetime


#Report for Jan, Mar, Apr, May, Jun, Jul, Aug, Sep, Oct, Nov and Dec
@periodic_task(run_every=crontab(minute="01",
                                 hour="08", day_of_month="30",
                                 month_of_year="1,3,4,5,6,7,8,9,10,11,12"))


def save_report_by_month(request):
    xindex_attribute = Decimal(0)
    xindex_moment = Decimal(0)
    xindex_service = Decimal(0)
    xindex_business_unit = Decimal(0)
    xindex_subsidiary = Decimal(0)
    xindex_zone = Decimal(0)
    xindex_company = Decimal(0)

    xindex_company = get_xindex_company()

    for company in Company.objects.filter(active=True):
        for zone in company.zone.filter(active=True):
            print '-----------------------------------------'
            xindex_zone = get_xindex_zone(zone)
            print 'La '+zone.name+' tiene un nivel de satisfaccion del '+str(xindex_zone)+'%'
            for subsidiary in zone.subsidiary_set.filter(active=True):
                print '______________________________________________'
                xindex_subsidiary = get_xindex_subsidiary(subsidiary)
                print 'La '+subsidiary.name+' tiene un nivel de satisfaccion del '+str(xindex_subsidiary)+'%'
                for s_bu in SubsidiaryBusinessUnit.objects.filter(id_subsidiary=subsidiary):
                    print '.....................................................'
                    xindex_business_unit = get_xindex_business_unit(subsidiary, s_bu.id_business_unit)
                    print 'La '+s_bu.id_business_unit.name+' tiene un nivel de satisfaccion del '+str(xindex_business_unit)+'%'
                    for s_bu_s in sbu_service.objects.filter(id_subsidiaryBU=s_bu):
                        print '<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<'
                        xindex_service = get_xindex_service(subsidiary, s_bu.id_business_unit, s_bu_s.id_service)
                        print 'El servicio:  '+s_bu_s.id_service.name+' tiene un nivel de satisfaccion del '+str(xindex_service)+'%'
                        for s_bu_s_m in sbu_service_moment.objects.filter(id_sbu_service=s_bu_s):
                            xindex_moment = get_xindex_moment(subsidiary, s_bu.id_business_unit, s_bu_s.id_service, s_bu_s_m.id_moment)
                            print 'El momento:  '+s_bu_s_m.id_moment.name+' tiene un nivel de satisfaccion del '+str(xindex_moment)+'%'
                        print '<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<'
                    print '.....................................................'
                print '______________________________________________'
            print '-----------------------------------------'

    return HttpResponse('The xindex company is: '+str(xindex_company)+'%')


#Report for Feb
@periodic_task(run_every=crontab(minute="01",
                                 hour="08",
                                 day_of_month="28",
                                 month_of_year="2"))
def save_report_by_month_feb():
    print 'Saving report by month feb'



def get_xindex_company():
    #----- Save xindex for COMPANY ------#
    #data for company
    xindex_company = 0
    promoters_percent = 0
    passives_percent = 0
    detractors_percent = 0

    #Get data for zone subsidiaries
    total_promoters = 0
    total_passives = 0
    total_detractors = 0
    total_surveyed = 0
    total_company_answers = []
    for company in Company.objects.filter(active=True):
        for zone in company.zone.filter(active=True):
            for subsidiary in zone.subsidiary_set.filter(active=True):
                for s_bu in SubsidiaryBusinessUnit.objects.filter(id_subsidiary=subsidiary):
                    for s_bu_s in sbu_service.objects.filter(id_subsidiaryBU=s_bu):
                        for s_bu_s_m in sbu_service_moment.objects.filter(id_sbu_service=s_bu_s):
                            for s_bu_s_m_a in sbu_service_moment_attribute.objects.filter(id_sbu_service_moment=s_bu_s_m):
                                for s_bu_s_m_a_q in s_bu_s_m_a.question_sbu_s_m_a_set.all():
                                    attrib_answers = Answer.objects.filter(question=s_bu_s_m_a_q.question_id)

                                    for answer in attrib_answers:
                                        client = Client.objects.get(pk=int(answer.client.id))
                                        try:
                                            client_activity = ClientActivity.objects.get(client=client, subsidiary=subsidiary)
                                            #Get the current date
                                            current_date = datetime.date.today()
                                            if current_date.year == answer.date.year and current_date.month == answer.date.month:
                                                total_company_answers.append(answer)
                                        except ClientActivity.DoesNotExist:
                                            pass

    if not len(total_company_answers) == 0:
        for answer_company in total_company_answers:
            #total answers for company
            total_surveyed += 1
            if answer_company.value == 10 or answer_company.value == 9:
                #promoters for company
                total_promoters += 1
            elif answer_company.value == 8 or answer_company.value == 7:
                #passives for company
                total_passives += 1
            elif 1 <= answer_company.value <= 6:
                #detractors for company
                total_detractors += 1

    #Calculate the company data
    getcontext().prec = 5

    if total_promoters != 0 and total_surveyed != 0:
        promoters_percent = Decimal(total_promoters*100)/Decimal(total_surveyed)

    if total_passives != 0 and total_surveyed != 0:
        passives_percent = Decimal(total_passives*100)/Decimal(total_surveyed)

    if total_detractors != 0 and total_surveyed != 0:
        detractors_percent = Decimal(total_detractors*100)/Decimal(total_surveyed)

    if promoters_percent != 0 and passives_percent != 0 and detractors_percent != 0:
        xindex_company = Decimal(promoters_percent-detractors_percent)

    return xindex_company

    #------------------------------------#


def get_xindex_zone(zone):
    #data for zone
    xindex_zone = 0
    promoters_percent = 0
    passives_percent = 0
    detractors_percent = 0

    total_promoters = 0
    total_passives = 0
    total_detractors = 0
    total_surveyed = 0
    total_zone_answers = []

    for subsidiary in zone.subsidiary_set.filter(active=True):
        for s_bu in SubsidiaryBusinessUnit.objects.filter(id_subsidiary=subsidiary):
            for s_bu_s in sbu_service.objects.filter(id_subsidiaryBU=s_bu):
                for s_bu_s_m in sbu_service_moment.objects.filter(id_sbu_service=s_bu_s):
                    for s_bu_s_m_a in sbu_service_moment_attribute.objects.filter(id_sbu_service_moment=s_bu_s_m):
                        for s_bu_s_m_a_q in s_bu_s_m_a.question_sbu_s_m_a_set.all():
                            attrib_answers = Answer.objects.filter(question=s_bu_s_m_a_q.question_id)

                            for answer in attrib_answers:
                                client = Client.objects.get(pk=int(answer.client.id))
                                try:
                                    client_activity = ClientActivity.objects.get(client=client, subsidiary=subsidiary)
                                    current_date = datetime.date.today()
                                    if current_date.year == client_activity.date.year and current_date.month == client_activity.date.month and client_activity.subsidiary == subsidiary and client_activity.subsidiary.zone == zone:
                                        total_zone_answers.append(answer)
                                except ClientActivity.DoesNotExist:
                                    pass

    if not len(total_zone_answers) == 0:
        for answer_zone in total_zone_answers:
            #total answers for zone
            if answer_zone.value > 0:
                total_surveyed += 1
            if answer_zone.value == 10 or answer_zone.value == 9:
                #promoters for zone
                total_promoters += 1
            elif answer_zone.value == 8 or answer_zone.value == 7:
                #passives for zone
                total_passives += 1
            elif 1 <= answer_zone.value <= 6:
                #detractors for zone
                total_detractors += 1

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

    return xindex_zone


def get_xindex_subsidiary(subsidiary):
    #data for subsidiary
    xindex_subsidiary = 0
    promoters_percent = 0
    passives_percent = 0
    detractors_percent = 0

    total_promoters = 0
    total_passives = 0
    total_detractors = 0
    total_surveyed = 0
    total_subsidiary_answers = []

    for s_bu in SubsidiaryBusinessUnit.objects.filter(id_subsidiary=subsidiary):
        for s_bu_s in sbu_service.objects.filter(id_subsidiaryBU=s_bu):
            for s_bu_s_m in sbu_service_moment.objects.filter(id_sbu_service=s_bu_s):
                for s_bu_s_m_a in sbu_service_moment_attribute.objects.filter(id_sbu_service_moment=s_bu_s_m):
                    for s_bu_s_m_a_q in s_bu_s_m_a.question_sbu_s_m_a_set.filter(active=True):
                        attrib_answers = Answer.objects.filter(question=s_bu_s_m_a_q.question_id)

                        for answer in attrib_answers:
                            client = Client.objects.get(pk=int(answer.client.id))
                            try:
                                client_activity = ClientActivity.objects.get(client=client, subsidiary=subsidiary)
                                current_date = datetime.date.today()
                                if client_activity.subsidiary == subsidiary and answer.date.year == current_date.year and answer.date.month == current_date.month:
                                    total_subsidiary_answers.append(answer)
                            except ClientActivity.DoesNotExist:
                                pass

    if not len(total_subsidiary_answers) == 0:
        for subsidiary_answer in total_subsidiary_answers:
            #total answers for subsidiary
            if subsidiary_answer.value > 0:
                total_surveyed += 1
            if subsidiary_answer.value == 10 or subsidiary_answer.value == 9:
                #promoters for subsidiary
                total_promoters += 1
            elif subsidiary_answer.value == 8 or subsidiary_answer.value == 7:
                #passives for subsidiary
                total_passives += 1
            elif 1 <= subsidiary_answer.value <= 6:
                #detractors for subsidiary
                total_detractors += 1

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

    return xindex_subsidiary


def get_xindex_business_unit(subsidiary, business_unit):
    #data for business unit
    xindex_business_unit = 0
    promoters_percent = 0
    passives_percent = 0
    detractors_percent = 0

    #Get data for business unit
    total_promoters = 0
    total_passives = 0
    total_detractors = 0
    total_surveyed = 0
    total_business_unit_answers = []
    #relation between subsidiary and business unit
    s_bu = SubsidiaryBusinessUnit.objects.get(id_subsidiary=subsidiary, id_business_unit=business_unit)
    for s_bu_s in sbu_service.objects.filter(id_subsidiaryBU=s_bu):
        for s_bu_s_m in sbu_service_moment.objects.filter(id_sbu_service=s_bu_s).order_by('id_moment'):
            for s_bu_s_m_a in sbu_service_moment_attribute.objects.filter(id_sbu_service_moment=s_bu_s_m):
                for s_bu_s_m_a_q in s_bu_s_m_a.question_sbu_s_m_a_set.all():
                    attrib_answers = Answer.objects.filter(question=s_bu_s_m_a_q.question_id)

                    for answer in attrib_answers:
                        client = Client.objects.get(pk=int(answer.client.id))
                        try:
                            client_activity = ClientActivity.objects.get(client=client, subsidiary=subsidiary, business_unit=business_unit)
                            current_date = datetime.date.today()
                            if client_activity.subsidiary == subsidiary and client_activity.business_unit == business_unit and answer.date.year == current_date.year and answer.date.month == current_date.month:
                                total_business_unit_answers.append(answer)
                        except ClientActivity.DoesNotExist:
                            pass

    if not len(total_business_unit_answers) == 0:
        for business_unit_answer in total_business_unit_answers:
            if business_unit_answer.value > 0:
                total_surveyed += 1
            if business_unit_answer.value == 10 or business_unit_answer.value == 9:
                #promoters for business unit
                total_promoters += 1
            elif business_unit_answer.value == 8 or business_unit_answer.value == 7:
                #passives for business unit
                total_passives += 1
            elif 1 <= business_unit_answer.value <= 6:
                #detractors for business unit
                total_detractors += 1

    #Calculate the business unit data
    getcontext().prec = 5

    if total_promoters != 0 and total_surveyed != 0:
        promoters_percent = Decimal(total_promoters*100)/Decimal(total_surveyed)

    if total_passives != 0 and total_surveyed != 0:
        passives_percent = Decimal(total_passives*100)/Decimal(total_surveyed)

    if total_detractors != 0 and total_surveyed != 0:
        detractors_percent = Decimal(total_detractors*100)/Decimal(total_surveyed)

    if promoters_percent != 0 and passives_percent != 0 and detractors_percent != 0:
        xindex_business_unit = Decimal(promoters_percent-detractors_percent)

    return xindex_business_unit


def get_xindex_service(subsidiary, business_unit, service):
    #data for service
    xindex_service = 0
    promoters_percent = 0
    passives_percent = 0
    detractors_percent = 0

    #Get data for service
    total_promoters = 0
    total_passives = 0
    total_detractors = 0
    total_surveyed = 0
    total_service_answers = []

    #relation between subsidiary and business unit
    s_bu = SubsidiaryBusinessUnit.objects.get(id_subsidiary=subsidiary, id_business_unit=business_unit)
    print s_bu.alias
    for s_bu_s in sbu_service.objects.filter(id_subsidiaryBU=s_bu, id_service=service):
        for s_bu_s_m in sbu_service_moment.objects.filter(id_sbu_service=s_bu_s):
            for s_bu_s_m_a in sbu_service_moment_attribute.objects.filter(id_sbu_service_moment=s_bu_s_m):
                for s_bu_s_m_a_q in s_bu_s_m_a.question_sbu_s_m_a_set.all():
                    attrib_answers = Answer.objects.filter(question=s_bu_s_m_a_q.question_id)

                    for answer in attrib_answers:
                        client = Client.objects.get(pk=int(answer.client.id))
                        try:
                            client_activity = ClientActivity.objects.get(client=client, subsidiary=subsidiary, business_unit=business_unit, service=service)
                            current_date = datetime.date.today()
                            if client_activity.subsidiary == subsidiary and client_activity.business_unit == business_unit and client_activity.service == service and answer.date.year == current_date.year and answer.date.month == current_date.month:
                                total_service_answers.append(answer)
                        except ClientActivity.DoesNotExist:
                            pass

    for service_answer in total_service_answers:
        if service_answer.value > 0:
            total_surveyed += 1
        if service_answer.value == 10 or service_answer.value == 9:
            #promoters for service
            total_promoters += 1
        elif service_answer.value == 8 or service_answer.value == 7:
            #passives for service
            total_passives += 1
        elif 1 <= service_answer.value <= 6:
            #detractors for service
            total_detractors += 1

    #print total_surveyed
    #Calculate the service data
    getcontext().prec = 5

    if total_promoters != 0 and total_surveyed != 0:
        promoters_percent = Decimal(total_promoters*100)/Decimal(total_surveyed)

    if total_passives != 0 and total_surveyed != 0:
        passives_percent = Decimal(total_passives*100)/Decimal(total_surveyed)

    if total_detractors != 0 and total_surveyed != 0:
        detractors_percent = Decimal(total_detractors*100)/Decimal(total_surveyed)

    if promoters_percent != 0 or detractors_percent != 0:
        xindex_service = Decimal(promoters_percent-detractors_percent)

    return xindex_service


def get_xindex_moment(subsidiary, businessUnit, service, moment):
    moment_xindex = Decimal(0)
    promoters_percent = 0
    passives_percent = 0
    detractors_percent = 0

    total_promoters = 0
    total_passives = 0
    total_detractors = 0
    total_answers = 0
    answers_list = []
    for child_subsidiary_bu in SubsidiaryBusinessUnit.objects.filter(id_subsidiary=subsidiary, id_business_unit=businessUnit):
        for child_sbu_service in sbu_service.objects.filter(id_subsidiaryBU=child_subsidiary_bu, id_service=service):
            for child_sbu_s_moment in sbu_service_moment.objects.filter(id_sbu_service=child_sbu_service, id_moment=moment):
                for child_sbu_s_m_a in sbu_service_moment_attribute.objects.filter(id_sbu_service_moment=child_sbu_s_moment):
                    for relation_q_s_bu_s_m_a in child_sbu_s_m_a.question_sbu_s_m_a_set.all():
                        question_answers = Answer.objects.filter(question_id=relation_q_s_bu_s_m_a.question_id)
                        for a in question_answers:
                            client = Client.objects.get(pk=a.client_id)
                            try:
                                client_activity = ClientActivity.objects.get(client=client, subsidiary=subsidiary, business_unit=businessUnit, service=service)
                                current_date = datetime.date.today()
                                if a.date.year == current_date.year and a.date.month == current_date.month:
                                    answers_list.append(a)
                            except ClientActivity.DoesNotExist:
                                pass
    #for answer in Answer.objects.filter(question_id=relation_q_s_bu_s_m_a.question_id, client_id__subsidiary=subsidiary):
    for answer in answers_list:
        if answer.value > 0:
            total_answers += 1
        if answer.value == 10 or answer.value == 9:
            total_promoters += 1
        elif answer.value == 8 or answer.value == 7:
            total_passives += 1
        elif 1 <= answer.value <= 6:
            total_detractors += 1

    if total_promoters != 0 and total_answers != 0:
        promoters_percent = Decimal(total_promoters*100)/Decimal(total_answers)

    if total_passives != 0 and total_answers != 0:
        passives_percent = Decimal(total_passives*100)/Decimal(total_answers)

    if total_detractors != 0 and total_answers != 0:
        detractors_percent = Decimal(total_detractors*100)/Decimal(total_answers)

    if promoters_percent != 0 or detractors_percent != 0:
        moment_xindex = Decimal(promoters_percent-detractors_percent)

    return moment_xindex