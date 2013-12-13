from xindex.models import Service
from xindex.models import Subsidiary
from xindex.models import Answer, Client, ClientActivity
from xindex.models import SubsidiaryBusinessUnit, BusinessUnit
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

def get_moment_xindex_by_group(subsidiary, business_unit, service, moment):
    #Get data for moment
    total_promoters = 0
    total_passives = 0
    total_detractors = 0
    total_surveyed = 0
    promoters_percent = 0
    passives_percent = 0
    detractors_percent = 0
    xindex = 0
    total_answers = []
    c_d = datetime.date.today()

    if isinstance(subsidiary, Subsidiary):
        if isinstance(business_unit, BusinessUnit):
            #relation between subsidiary and business unit
            s_bu = SubsidiaryBusinessUnit.objects.get(id_subsidiary=subsidiary, id_business_unit=business_unit)
            for s_bu_s in sbu_service.objects.filter(id_subsidiaryBU=s_bu, id_service=service):
                #All moments for this service
                if len(sbu_service_moment.objects.filter(id_sbu_service=s_bu_s)) == 0:
                    survey_is_designed = False
                for s_bu_s_m in sbu_service_moment.objects.filter(id_sbu_service=s_bu_s, id_moment=moment):
                    #All attributes for all moments

                    for s_bu_s_m_a in sbu_service_moment_attribute.objects.filter(id_sbu_service_moment=s_bu_s_m):
                        for s_bu_s_m_a_q in s_bu_s_m_a.question_sbu_s_m_a_set.all():
                            attrib_answers = Answer.objects.filter(question=s_bu_s_m_a_q.question_id)

                            for answer in attrib_answers:
                                client = Client.objects.get(pk=int(answer.client.id))
                                if answer.client_activity is not None:
                                    try:
                                        client_activity = ClientActivity.objects.get(client=client, subsidiary=subsidiary, business_unit=business_unit, service=service, pk=answer.client_activity.id)
                                        if answer.date.year == c_d.year and answer.date.month == c_d.month and client_activity.subsidiary == subsidiary and client_activity.business_unit == business_unit:
                                            total_answers.append(answer)
                                    except ClientActivity.DoesNotExist:
                                        pass

        else:
            #relation between subsidiary and business unit
            for bu in business_unit:
                try:
                    s_bu = SubsidiaryBusinessUnit.objects.get(id_subsidiary=subsidiary, id_business_unit=bu)
                    for s_bu_s in sbu_service.objects.filter(id_subsidiaryBU=s_bu, id_service=service):
                        #All moments for this service
                        if len(sbu_service_moment.objects.filter(id_sbu_service=s_bu_s)) == 0:
                            survey_is_designed = False
                        for s_bu_s_m in sbu_service_moment.objects.filter(id_sbu_service=s_bu_s, id_moment=moment):
                            #All attributes for all moments
                            for s_bu_s_m_a in sbu_service_moment_attribute.objects.filter(id_sbu_service_moment=s_bu_s_m):
                                for s_bu_s_m_a_q in s_bu_s_m_a.question_sbu_s_m_a_set.all():
                                    attrib_answers = Answer.objects.filter(question=s_bu_s_m_a_q.question_id)

                                    for answer in attrib_answers:
                                        client = Client.objects.get(pk=int(answer.client.id))
                                        if answer.client_activity is not None:
                                            try:
                                                client_activity = ClientActivity.objects.get(client=client, subsidiary=subsidiary, business_unit=bu, service=service, pk=answer.client_activity.id)
                                                if answer.date.year == c_d.year and answer.date.month == c_d.month and client_activity.subsidiary == subsidiary and client_activity.business_unit == bu:
                                                    total_answers.append(answer)
                                            except ClientActivity.DoesNotExist:
                                                pass
                except SubsidiaryBusinessUnit.DoesNotExist:
                    pass
    else:
        if isinstance(business_unit, BusinessUnit):
            for subsi in subsidiary:
                try:
                    s_bu = SubsidiaryBusinessUnit.objects.get(id_subsidiary=subsi, id_business_unit=business_unit)
                    for s_bu_s in sbu_service.objects.filter(id_subsidiaryBU=s_bu, id_service=service):
                        #All moments for this service
                        if len(sbu_service_moment.objects.filter(id_sbu_service=s_bu_s)) == 0:
                            survey_is_designed = False
                        for s_bu_s_m in sbu_service_moment.objects.filter(id_sbu_service=s_bu_s, id_moment=moment):
                            #All attributes for all moments
                            for s_bu_s_m_a in sbu_service_moment_attribute.objects.filter(id_sbu_service_moment=s_bu_s_m):
                                for s_bu_s_m_a_q in s_bu_s_m_a.question_sbu_s_m_a_set.all():
                                    attrib_answers = Answer.objects.filter(question=s_bu_s_m_a_q.question_id)

                                    for answer in attrib_answers:
                                        client = Client.objects.get(pk=int(answer.client.id))
                                        if answer.client_activity is not None:
                                            try:
                                                client_activity = ClientActivity.objects.get(client=client, subsidiary=subsi, business_unit=business_unit, service=service, pk=answer.client_activity.id)
                                                if answer.date.year == c_d.year and answer.date.month == c_d.month and client_activity.subsidiary == subsi and client_activity.business_unit == business_unit:
                                                    total_answers.append(answer)
                                            except ClientActivity.DoesNotExist:
                                                pass
                except SubsidiaryBusinessUnit.DoesNotExist:
                    pass
        else:
            for subsid in subsidiary:
                for buss_uni in business_unit:
                    try:
                        s_bu = SubsidiaryBusinessUnit.objects.get(id_subsidiary=subsid, id_business_unit=buss_uni)
                        for s_bu_s in sbu_service.objects.filter(id_subsidiaryBU=s_bu, id_service=service):
                            #All moments for this service
                            if len(sbu_service_moment.objects.filter(id_sbu_service=s_bu_s)) == 0:
                                survey_is_designed = False
                            for s_bu_s_m in sbu_service_moment.objects.filter(id_sbu_service=s_bu_s, id_moment=moment):
                                #All attributes for all moments
                                for s_bu_s_m_a in sbu_service_moment_attribute.objects.filter(id_sbu_service_moment=s_bu_s_m):
                                    for s_bu_s_m_a_q in s_bu_s_m_a.question_sbu_s_m_a_set.all():
                                        attrib_answers = Answer.objects.filter(question=s_bu_s_m_a_q.question_id)

                                        for answer in attrib_answers:
                                            client = Client.objects.get(pk=int(answer.client.id))
                                            if answer.client_activity is not None:
                                                try:
                                                    client_activity = ClientActivity.objects.get(client=client, subsidiary=subsid, business_unit=buss_uni, service=service, pk=answer.client_activity.id)
                                                    if answer.date.year == c_d.year and answer.date.month == c_d.month and client_activity.subsidiary == subsid and client_activity.business_unit == buss_uni:
                                                        total_answers.append(answer)
                                                except ClientActivity.DoesNotExist:
                                                    pass

                    except SubsidiaryBusinessUnit.DoesNotExist:
                        pass

    if not len(total_answers) == 0:
        for answer in total_answers:
            #total answers
            if answer > 0:
                total_surveyed += 1
            if answer.value == 10 or answer.value == 9:
                total_promoters += 1
            elif answer.value == 8 or answer.value == 7:
                total_passives += 1
            elif 1 <= answer.value <= 6:
                total_detractors += 1

    getcontext().prec = 5

    if total_answers != 0 and total_promoters != 0:
        promoters_percent = Decimal(total_promoters*100)/Decimal(len(total_answers))
    if total_answers != 0 and total_passives != 0:
        passives_percent = Decimal(total_passives*100)/Decimal(len(total_answers))
    if total_answers != 0 and total_detractors != 0:
        detractors_percent = Decimal(total_detractors*100)/Decimal(len(total_answers))

    if not total_answers == 0:
        xindex = Decimal(promoters_percent-detractors_percent)

    r = lambda: random.randint(0, 255)

    moment_object = {
        #xindex for moment
        'xindex_moment': xindex,
        #info
        'moment_id': moment.id,
        'moment_name': moment.name,
        #data
        'promoters': promoters_percent,
        'passives': passives_percent,
        'detractors': detractors_percent,
        #extra
        'color': ('#%02X%02X%02X' % (r(), r(), r()))
    }

    return moment_object


def get_last_month_service_xindex(subsidiary, business_unit, service):
    #Get data for service
    total_promoters = 0
    total_passives = 0
    total_detractors = 0
    total_surveyed = 0
    total_answers = []
    promoters_percent = 0
    passives_percent = 0
    detractors_percent = 0
    xindex_service = 0

    c_d = datetime.date.today()
    last_month = c_d.month-1
    year = c_d.year
    if c_d.month == 01:
        last_month = 12
        year = c_d.year-1


    if isinstance(subsidiary, Subsidiary):
        if isinstance(business_unit, BusinessUnit):
            #relation between subsidiary and business unit
            s_bu = SubsidiaryBusinessUnit.objects.get(id_subsidiary=subsidiary, id_business_unit=business_unit)
            for s_bu_s in sbu_service.objects.filter(id_subsidiaryBU=s_bu, id_service=service):
                #All moments for this service
                if len(sbu_service_moment.objects.filter(id_sbu_service=s_bu_s)) == 0:
                    survey_is_designed = False
                for s_bu_s_m in sbu_service_moment.objects.filter(id_sbu_service=s_bu_s).order_by('id_moment'):
                    #All attributes for all moments

                    for s_bu_s_m_a in sbu_service_moment_attribute.objects.filter(id_sbu_service_moment=s_bu_s_m):
                        for s_bu_s_m_a_q in s_bu_s_m_a.question_sbu_s_m_a_set.all():
                            attrib_answers = Answer.objects.filter(question=s_bu_s_m_a_q.question_id)

                            for answer in attrib_answers:
                                client = Client.objects.get(pk=int(answer.client.id))
                                if answer.client_activity is not None:
                                    try:
                                        client_activity = ClientActivity.objects.get(client=client, subsidiary=subsidiary, business_unit=business_unit, service=service, pk=answer.client_activity.id)
                                        if answer.date.year == year and answer.date.month == last_month and client_activity.subsidiary == subsidiary and client_activity.business_unit == business_unit:
                                            total_answers.append(answer)
                                    except ClientActivity.DoesNotExist:
                                        pass
        else:
            #relation between subsidiary and business unit
            for bu in business_unit:
                try:
                    s_bu = SubsidiaryBusinessUnit.objects.get(id_subsidiary=subsidiary, id_business_unit=bu)
                    for s_bu_s in sbu_service.objects.filter(id_subsidiaryBU=s_bu, id_service=service):
                        #All moments for this service
                        if len(sbu_service_moment.objects.filter(id_sbu_service=s_bu_s)) == 0:
                            survey_is_designed = False
                        for s_bu_s_m in sbu_service_moment.objects.filter(id_sbu_service=s_bu_s).order_by('id_moment'):
                            #All attributes for all moments
                            for s_bu_s_m_a in sbu_service_moment_attribute.objects.filter(id_sbu_service_moment=s_bu_s_m):
                                for s_bu_s_m_a_q in s_bu_s_m_a.question_sbu_s_m_a_set.all():
                                    attrib_answers = Answer.objects.filter(question=s_bu_s_m_a_q.question_id)

                                    for answer in attrib_answers:
                                        client = Client.objects.get(pk=int(answer.client.id))
                                        if answer.client_activity is not None:
                                            try:
                                                client_activity = ClientActivity.objects.get(client=client, subsidiary=subsidiary, business_unit=bu, service=service, pk=answer.client_activity.id)
                                                if answer.date.year == year and answer.date.month == last_month and client_activity.subsidiary == subsidiary and client_activity.business_unit == bu:
                                                    total_answers.append(answer)
                                            except ClientActivity.DoesNotExist:
                                                pass
                except SubsidiaryBusinessUnit.DoesNotExist:
                    pass
    else:
        if isinstance(business_unit, BusinessUnit):
            for subsi in subsidiary:
                try:
                    s_bu = SubsidiaryBusinessUnit.objects.get(id_subsidiary=subsi, id_business_unit=business_unit)
                    for s_bu_s in sbu_service.objects.filter(id_subsidiaryBU=s_bu, id_service=service):
                        #All moments for this service
                        if len(sbu_service_moment.objects.filter(id_sbu_service=s_bu_s)) == 0:
                            survey_is_designed = False
                        for s_bu_s_m in sbu_service_moment.objects.filter(id_sbu_service=s_bu_s).order_by('id_moment'):
                            #All attributes for all moments
                            for s_bu_s_m_a in sbu_service_moment_attribute.objects.filter(id_sbu_service_moment=s_bu_s_m):
                                for s_bu_s_m_a_q in s_bu_s_m_a.question_sbu_s_m_a_set.all():
                                    attrib_answers = Answer.objects.filter(question=s_bu_s_m_a_q.question_id)

                                    for answer in attrib_answers:
                                        client = Client.objects.get(pk=int(answer.client.id))
                                        if answer.client_activity is not None:
                                            try:
                                                client_activity = ClientActivity.objects.get(client=client, subsidiary=subsi, business_unit=business_unit, service=service, pk=answer.client_activity.id)
                                                if answer.date.year == year and answer.date.month == last_month and client_activity.subsidiary == subsi and client_activity.business_unit == business_unit:
                                                    total_answers.append(answer)
                                            except ClientActivity.DoesNotExist:
                                                pass
                except SubsidiaryBusinessUnit.DoesNotExist:
                    pass
        else:
            for subsid in subsidiary:
                for buss_uni in business_unit:
                    try:
                        s_bu = SubsidiaryBusinessUnit.objects.get(id_subsidiary=subsid, id_business_unit=buss_uni)
                        for s_bu_s in sbu_service.objects.filter(id_subsidiaryBU=s_bu, id_service=service):
                            #All moments for this service
                            if len(sbu_service_moment.objects.filter(id_sbu_service=s_bu_s)) == 0:
                                survey_is_designed = False
                            for s_bu_s_m in sbu_service_moment.objects.filter(id_sbu_service=s_bu_s).order_by('id_moment'):
                                #All attributes for all moments
                                for s_bu_s_m_a in sbu_service_moment_attribute.objects.filter(id_sbu_service_moment=s_bu_s_m):
                                    for s_bu_s_m_a_q in s_bu_s_m_a.question_sbu_s_m_a_set.all():
                                        attrib_answers = Answer.objects.filter(question=s_bu_s_m_a_q.question_id)

                                        for answer in attrib_answers:
                                            client = Client.objects.get(pk=int(answer.client.id))
                                            if answer.client_activity is not None:
                                                try:
                                                    client_activity = ClientActivity.objects.get(client=client, subsidiary=subsid, business_unit=buss_uni, service=service, pk=answer.client_activity.id)
                                                    if answer.date.year == year and answer.date.month == last_month and client_activity.subsid == subsidiary and client_activity.business_unit == buss_uni:
                                                        total_answers.append(answer)
                                                except ClientActivity.DoesNotExist:
                                                    pass

                    except SubsidiaryBusinessUnit.DoesNotExist:
                        pass

    if not len(total_answers) == 0:
        for answer in total_answers:
            if answer > 0:
                total_surveyed += 1
            if answer.value == 10 or answer.value == 9:
                total_promoters += 1
            elif answer.value == 8 or answer.value == 7:
                total_passives += 1
            elif 1 <= answer.value <= 6:
                total_detractors += 1

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

    return {
        'month': str(year)+'-'+str(last_month),
        'value': xindex_service
    }


def get_last_month_moment_xindex(subsidiary, business_unit, service, moment):
    total_promoters = 0
    total_passives = 0
    total_detractors = 0
    total_answers = 0
    answers_list = []

    c_d = datetime.date.today()
    last_month = c_d.month-1
    year = c_d.year
    if c_d.month == 01:
        last_month = 12
        year = c_d.year-1

    if isinstance(subsidiary, Subsidiary):
        if isinstance(business_unit, BusinessUnit):
            if isinstance(service, Service):
                #subsidiary IS an instance, business unit IS an instance and service IS an instance
                for child_subsidiary_bu in SubsidiaryBusinessUnit.objects.filter(id_subsidiary=subsidiary, id_business_unit=business_unit):
                    for child_sbu_service in sbu_service.objects.filter(id_subsidiaryBU=child_subsidiary_bu, id_service=service):
                        for child_sbu_s_moment in sbu_service_moment.objects.filter(id_sbu_service=child_sbu_service, id_moment=moment):
                            for child_sbu_s_m_a in sbu_service_moment_attribute.objects.filter(id_sbu_service_moment=child_sbu_s_moment).order_by('id_attribute'):
                                for relation_q_s_bu_s_m_a in child_sbu_s_m_a.question_sbu_s_m_a_set.all():
                                    question_answers = Answer.objects.filter(question_id=relation_q_s_bu_s_m_a.question_id)

                                    for a in question_answers:
                                        client = Client.objects.get(pk=a.client_id)
                                        if a.client_activity is not None:
                                            try:
                                                client_activity = ClientActivity.objects.get(client=client, subsidiary=subsidiary, business_unit=business_unit, service=service, pk=a.client_activity.id)
                                                c_d = datetime.date.today()
                                                if a.date.year == year and a.date.month == last_month and client_activity.subsidiary == subsidiary and client_activity.business_unit == business_unit:
                                                    answers_list.append(a)
                                            except ClientActivity.DoesNotExist:
                                                pass
            else:
                #subsidiary IS an instance, business unit IS an instance and service IS NOT an instance
                for child_subsidiary_bu in SubsidiaryBusinessUnit.objects.filter(id_subsidiary=subsidiary, id_business_unit=business_unit):
                    for serv in service:
                        for child_sbu_service in sbu_service.objects.filter(id_subsidiaryBU=child_subsidiary_bu, id_service=serv):
                            for child_sbu_s_moment in sbu_service_moment.objects.filter(id_sbu_service=child_sbu_service, id_moment=moment):
                                for child_sbu_s_m_a in sbu_service_moment_attribute.objects.filter(id_sbu_service_moment=child_sbu_s_moment):
                                    for relation_q_s_bu_s_m_a in child_sbu_s_m_a.question_sbu_s_m_a_set.all():
                                        question_answers = Answer.objects.filter(question_id=relation_q_s_bu_s_m_a.question_id)

                                        for a in question_answers:
                                            client = Client.objects.get(pk=a.client_id)
                                            if a.client_activity is not None:
                                                try:
                                                    client_activity = ClientActivity.objects.get(client=client, subsidiary=subsidiary, business_unit=business_unit, service=service, pk=a.client_activity.id)
                                                    c_d = datetime.date.today()
                                                    if a.date.year == year and a.date.month == last_month and client_activity.subsidiary == subsidiary and client_activity.business_unit == business_unit:
                                                        answers_list.append(a)
                                                except ClientActivity.DoesNotExist:
                                                    pass
        else:
            if isinstance(service, Service):
                #subsidiary IS an instance, business unit IS NOT an instance and service IS an instance
                for bu_un in business_unit:
                    for child_subsidiary_bu in SubsidiaryBusinessUnit.objects.filter(id_subsidiary=subsidiary, id_business_unit=bu_un):
                        for child_sbu_service in sbu_service.objects.filter(id_subsidiaryBU=child_subsidiary_bu, id_service=service):
                            for child_sbu_s_moment in sbu_service_moment.objects.filter(id_sbu_service=child_sbu_service, id_moment=moment):
                                for child_sbu_s_m_a in sbu_service_moment_attribute.objects.filter(id_sbu_service_moment=child_sbu_s_moment).order_by('id_attribute'):
                                    for relation_q_s_bu_s_m_a in child_sbu_s_m_a.question_sbu_s_m_a_set.all():
                                        question_answers = Answer.objects.filter(question_id=relation_q_s_bu_s_m_a.question_id)

                                        for a in question_answers:
                                            client = Client.objects.get(pk=a.client_id)
                                            if a.client_activity is not None:
                                                try:
                                                    client_activity = ClientActivity.objects.get(client=client, subsidiary=subsidiary, business_unit=bu_un, service=service, pk=a.client_activity.id)
                                                    c_d = datetime.date.today()
                                                    if a.date.year == year and a.date.month == last_month and client_activity.subsidiary == subsidiary and client_activity.business_unit == bu_un:
                                                        answers_list.append(a)
                                                except ClientActivity.DoesNotExist:
                                                    pass
            else:
                #subsidiary IS an instance, business unit IS NOT an instance and service IS NOT an instance
                for bu_un in business_unit:
                    for child_subsidiary_bu in SubsidiaryBusinessUnit.objects.filter(id_subsidiary=subsidiary, id_business_unit=bu_un):
                        for serv in service:
                            for child_sbu_service in sbu_service.objects.filter(id_subsidiaryBU=child_subsidiary_bu, id_service=serv):
                                for child_sbu_s_moment in sbu_service_moment.objects.filter(id_sbu_service=child_sbu_service, id_moment=moment):
                                    for child_sbu_s_m_a in sbu_service_moment_attribute.objects.filter(id_sbu_service_moment=child_sbu_s_moment).order_by('id_attribute'):
                                        for relation_q_s_bu_s_m_a in child_sbu_s_m_a.question_sbu_s_m_a_set.all():
                                            question_answers = Answer.objects.filter(question_id=relation_q_s_bu_s_m_a.question_id)

                                            for a in question_answers:
                                                client = Client.objects.get(pk=a.client_id)
                                                if a.client_activity is not None:
                                                    try:
                                                        client_activity = ClientActivity.objects.get(client=client, subsidiary=subsidiary, business_unit=bu_un, service=service, pk=a.client_activity.id)
                                                        c_d = datetime.date.today()
                                                        if a.date.year == year and a.date.month == last_month and client_activity.subsidiary == subsidiary and client_activity.business_unit == bu_un:
                                                            answers_list.append(a)
                                                    except ClientActivity.DoesNotExist:
                                                        pass
    else:
        if isinstance(business_unit, BusinessUnit):
            if isinstance(service, Service):
                #subsidiary IS NOT an instance, business unit IS an instance and service IS an instance
                for subsid in subsidiary:
                    for child_subsidiary_bu in SubsidiaryBusinessUnit.objects.filter(id_subsidiary=subsid, id_business_unit=business_unit):
                        for child_sbu_service in sbu_service.objects.filter(id_subsidiaryBU=child_subsidiary_bu, id_service=service):
                            for child_sbu_s_moment in sbu_service_moment.objects.filter(id_sbu_service=child_sbu_service, id_moment=moment):
                                for child_sbu_s_m_a in sbu_service_moment_attribute.objects.filter(id_sbu_service_moment=child_sbu_s_moment).order_by('id_attribute'):
                                    for relation_q_s_bu_s_m_a in child_sbu_s_m_a.question_sbu_s_m_a_set.all():
                                        question_answers = Answer.objects.filter(question_id=relation_q_s_bu_s_m_a.question_id)

                                        for a in question_answers:
                                            client = Client.objects.get(pk=a.client_id)
                                            if a.client_activity is not None:
                                                try:
                                                    client_activity = ClientActivity.objects.get(client=client, subsidiary=subsidiary, business_unit=business_unit, service=service, pk=a.client_activity.id)
                                                    c_d = datetime.date.today()
                                                    if a.date.year == year and a.date.month == last_month and client_activity.subsidiary == subsidiary and client_activity.business_unit == business_unit:
                                                        answers_list.append(a)
                                                except ClientActivity.DoesNotExist:
                                                    pass
            else:
                #subsidiary IS NOT an instance, business unit IS an instance and service IS NOT an instance
                for subsid in subsidiary:
                    for child_subsidiary_bu in SubsidiaryBusinessUnit.objects.filter(id_subsidiary=subsid, id_business_unit=business_unit):
                        for serv in service:
                            for child_sbu_service in sbu_service.objects.filter(id_subsidiaryBU=child_subsidiary_bu, id_service=serv):
                                for child_sbu_s_moment in sbu_service_moment.objects.filter(id_sbu_service=child_sbu_service, id_moment=moment):
                                    for child_sbu_s_m_a in sbu_service_moment_attribute.objects.filter(id_sbu_service_moment=child_sbu_s_moment).order_by('id_attribute'):
                                        for relation_q_s_bu_s_m_a in child_sbu_s_m_a.question_sbu_s_m_a_set.all():
                                            question_answers = Answer.objects.filter(question_id=relation_q_s_bu_s_m_a.question_id)

                                            for a in question_answers:
                                                client = Client.objects.get(pk=a.client_id)
                                                if a.client_activity is not None:
                                                    try:
                                                        client_activity = ClientActivity.objects.get(client=client, subsidiary=subsidiary, business_unit=business_unit, service=service, pk=a.client_activity.id)
                                                        c_d = datetime.date.today()
                                                        if a.date.year == year and a.date.month == last_month and client_activity.subsidiary == subsidiary and client_activity.business_unit == business_unit:
                                                            answers_list.append(a)
                                                    except ClientActivity.DoesNotExist:
                                                        pass
        else:
            if isinstance(service, Service):
                #subsidiary IS NOT an instance, business unit IS NOT an instance and service IS an instance
                for subsid in subsidiary:
                    for bu_un in business_unit:
                        for child_subsidiary_bu in SubsidiaryBusinessUnit.objects.filter(id_subsidiary=subsid, id_business_unit=bu_un):
                            for child_sbu_service in sbu_service.objects.filter(id_subsidiaryBU=child_subsidiary_bu, id_service=service):
                                for child_sbu_s_moment in sbu_service_moment.objects.filter(id_sbu_service=child_sbu_service, id_moment=moment):
                                    for child_sbu_s_m_a in sbu_service_moment_attribute.objects.filter(id_sbu_service_moment=child_sbu_s_moment).order_by('id_attribute'):
                                        for relation_q_s_bu_s_m_a in child_sbu_s_m_a.question_sbu_s_m_a_set.all():
                                            question_answers = Answer.objects.filter(question_id=relation_q_s_bu_s_m_a.question_id)

                                            for a in question_answers:
                                                client = Client.objects.get(pk=a.client_id)
                                                if a.client_activity is not None:
                                                    try:
                                                        client_activity = ClientActivity.objects.get(client=client, subsidiary=subsidiary, business_unit=bu_un, service=service, pk=a.client_activity.id)
                                                        c_d = datetime.date.today()
                                                        if a.date.year == year and a.date.month == last_month and client_activity.subsidiary == subsidiary and client_activity.business_unit == bu_un:
                                                            answers_list.append(a)
                                                    except ClientActivity.DoesNotExist:
                                                        pass
            else:
                #subsidiary IS NOT an instance, business unit IS NOT an instance and service IS NOT an instance
                for subsid in subsidiary:
                    for bu_un in business_unit:
                        for child_subsidiary_bu in SubsidiaryBusinessUnit.objects.filter(id_subsidiary=subsid, id_business_unit=bu_un):
                            for serv in service:
                                for child_sbu_service in sbu_service.objects.filter(id_subsidiaryBU=child_subsidiary_bu, id_service=serv):
                                    for child_sbu_s_moment in sbu_service_moment.objects.filter(id_sbu_service=child_sbu_service, id_moment=moment):
                                        for child_sbu_s_m_a in sbu_service_moment_attribute.objects.filter(id_sbu_service_moment=child_sbu_s_moment).order_by('id_attribute'):
                                            for relation_q_s_bu_s_m_a in child_sbu_s_m_a.question_sbu_s_m_a_set.all():
                                                question_answers = Answer.objects.filter(question_id=relation_q_s_bu_s_m_a.question_id)

                                                for a in question_answers:
                                                    client = Client.objects.get(pk=a.client_id)
                                                    if a.client_activity is not None:
                                                        try:
                                                            client_activity = ClientActivity.objects.get(client=client, subsidiary=subsidiary, business_unit=bu_un, service=service, pk=a.client_activity.id)
                                                            c_d = datetime.date.today()
                                                            if a.date.year == year and a.date.month == last_month and client_activity.subsidiary == subsidiary and client_activity.business_unit == bu_un:
                                                                answers_list.append(a)
                                                        except ClientActivity.DoesNotExist:
                                                            pass
    if total_promoters == 0 and total_detractors == 0 and total_passives == 0 and total_answers == 0:
        moment_xindex = 0
    else:
        moment_xindex = ((Decimal(total_promoters-total_detractors))/(Decimal(total_promoters+total_passives+total_detractors)))*Decimal(100)

    return {
        'month': str(year)+'-'+str(last_month),
        'value': moment_xindex
    }