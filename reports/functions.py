from xindex.models import Service
from xindex.models import Subsidiary
from xindex.models import Answer, Client, ClientActivity
from xindex.models import SubsidiaryBusinessUnit
from xindex.models import sbu_service, sbu_service_moment, sbu_service_moment_attribute
from decimal import *
import random
import datetime


def get_service_xindex_by_group(subsidiary, business_unit, service):
    #Get data for Service
    total_promoters = 0
    total_passives = 0
    total_detractors = 0
    total_surveyed = 0
    promoters_percent = 0
    passives_percent = 0
    detractors_percent = 0
    xindex = 0
    total_answers_by_service = []
    c_d = datetime.date.today()
    #relation between subsidiary and business unit
    if isinstance(subsidiary, Subsidiary):
        s_bu = SubsidiaryBusinessUnit.objects.get(id_subsidiary=subsidiary, id_business_unit=business_unit)

        for s_bu_s in sbu_service.objects.filter(id_subsidiaryBU=s_bu, id_service=service):
            for s_bu_s_m in sbu_service_moment.objects.filter(id_sbu_service=s_bu_s):
                for s_bu_s_m_a in sbu_service_moment_attribute.objects.filter(id_sbu_service_moment=s_bu_s_m):
                    for s_bu_s_m_a_q in s_bu_s_m_a.question_sbu_s_m_a_set.all():
                        attrib_answers = Answer.objects.filter(question=s_bu_s_m_a_q.question_id)

                        for answer in attrib_answers:
                            client = Client.objects.get(pk=int(answer.client.id))
                            if answer.client_activity is not None:
                                try:
                                    client_activity = ClientActivity.objects.get(client=client, subsidiary=subsidiary, business_unit=business_unit, pk=answer.client_activity.id)
                                    if client_activity.subsidiary == subsidiary and client_activity.business_unit == business_unit and answer.date.year == c_d.year and answer.date.month == c_d.month:
                                        total_answers_by_service.append(answer)
                                except ClientActivity.DoesNotExist:
                                    pass
    else:
        for subsidiary_a in subsidiary:
            try:
                s_bu = SubsidiaryBusinessUnit.objects.get(id_subsidiary=subsidiary_a, id_business_unit=business_unit)
                for s_bu_s in sbu_service.objects.filter(id_subsidiaryBU=s_bu, id_service=service).order_by('id_service'):

                    for s_bu_s_m in sbu_service_moment.objects.filter(id_sbu_service=s_bu_s).order_by('id_moment'):
                        for s_bu_s_m_a in sbu_service_moment_attribute.objects.filter(id_sbu_service_moment=s_bu_s_m):
                            for s_bu_s_m_a_q in s_bu_s_m_a.question_sbu_s_m_a_set.all():
                                attrib_answers = Answer.objects.filter(question=s_bu_s_m_a_q.question_id)

                                for answer in attrib_answers:
                                    client = Client.objects.get(pk=int(answer.client.id))
                                    if answer.client_activity is not None:
                                        try:
                                            client_activity = ClientActivity.objects.get(client=client, subsidiary=subsidiary_a, business_unit=business_unit, pk=answer.client_activity.id)
                                            if client_activity.subsidiary == subsidiary_a and client_activity.business_unit == business_unit and answer.date.year == c_d.year and answer.date.month == c_d.month:
                                                total_answers_by_service.append(answer)
                                        except ClientActivity.DoesNotExist:
                                            pass

            except SubsidiaryBusinessUnit.DoesNotExist:
                pass

    if not len(total_answers_by_service) == 0:
        for answer_service in total_answers_by_service:
            #total answers for service
            if answer_service > 0:
                total_surveyed += 1
            if answer_service.value == 10 or answer_service.value == 9:
                total_promoters += 1
            elif answer_service.value == 8 or answer_service.value == 7:
                total_passives += 1
            elif 1 <= answer_service.value <= 6:
                total_detractors += 1

    getcontext().prec = 5

    if total_answers_by_service != 0 and total_promoters != 0:
        promoters_percent = Decimal(total_promoters*100)/Decimal(len(total_answers_by_service))
    if total_answers_by_service != 0 and total_passives != 0:
        passives_percent = Decimal(total_passives*100)/Decimal(len(total_answers_by_service))
    if total_answers_by_service != 0 and total_detractors != 0:
        detractors_percent = Decimal(total_detractors*100)/Decimal(len(total_answers_by_service))

    if not total_answers_by_service == 0:
        #xindex_service = ((Decimal(promoters_percent_service-detractors_percent_service))/(Decimal(promoters_percent_service+passives_percent_service+detractors_percent_service)))*Decimal(100)
        xindex_service = Decimal(promoters_percent-detractors_percent)

    r = lambda: random.randint(0, 255)

    service = {
        #xindex for moment
        'xindex_service': xindex,
        #info
        'service_id': service.id,
        'service_name': service.name,
        #data
        'promoters': promoters_percent,
        'passives': passives_percent,
        'detractors': detractors_percent,
        #extra
        'color': ('#%02X%02X%02X' % (r(), r(), r()))
    }

    return service