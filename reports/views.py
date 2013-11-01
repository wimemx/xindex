from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, render_to_response
from django.template.context import RequestContext
from django.http import HttpResponse, Http404, HttpResponseRedirect
from xindex.models import Company
from xindex.models import Xindex_User
from xindex.models import Service
from xindex.models import Question_Attributes
from xindex.models import Question
from xindex.models import Option
from xindex.models import Moment
from xindex.models import Attributes
from decimal import *


def index(request):

    template_vars = {
        'title': ''
    }
    request_context = RequestContext(request, template_vars)
    return render(request, 'reports/index.html', request_context)


def report_by_moment(request):
    moment_xindex = Decimal(0)
    services = []
    moments = []
    data_attribute = []
    xindex_user = Xindex_User.objects.get(pk=request.user.id)
    companies = xindex_user.company_set.all()

    #Get services
    for company in companies:
        for subsidiary in company.subsidiary_set.all():
            for business_unit in subsidiary.businessunit_set.all():
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

    if request.POST:
        service = Service.objects.get(pk=int(request.POST['service']))
        moment = Moment.objects.get(pk=int(request.POST['select_touch_point']))
    else:
        service = services[1]
        moment = service.moments.all()[:1].get()

    #Get the relations of the moment
    relations_maq = Question_Attributes.objects.filter(moment_id=moment.id)
    for relation in relations_maq.all():
        prom = 0
        total_encuestados = len(relation.question_id.answer_set.all())
        for answer in relation.question_id.answer_set.all():
            prom += answer.value

    #Get promoters, passives and detractors by attribute
    total_promoters = 0
    total_passives = 0
    total_detractors = 0
    total_answers = 0
    for relation in relations_maq.all():
        total_surveyed = len(relation.question_id.answer_set.all())
        attribute = relation.attribute_id
        promoters_9 = 0
        promoters_10 = 0
        passives = 0
        detractors = 0
        for answer in relation.question_id.answer_set.all():
            total_answers += 1
            if answer.value == 10:
                promoters_10 += 1
                total_promoters += 1
            elif answer.value == 9:
                promoters_9 += 1
                total_promoters += 1
            elif answer.value == 8 or answer.value == 7:
                passives += 1
                total_passives +=1
            elif 1 <= answer.value <= 6:
                detractors += 1
                total_detractors += 1

        getcontext().prec = 5

        promoters_10_percent = Decimal(promoters_10*100)/Decimal(total_surveyed)
        promoters_9_percent = Decimal(promoters_9*100)/Decimal(total_surveyed)
        passives_percent = Decimal(passives*100)/Decimal(total_surveyed)
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

    #TODO: Get the historical data for this moment from the new model (create model)
    historical_months = [
        {'month': '2013-07', 'value': Decimal(45.67)},
        {'month': '2013-08', 'value': Decimal(56.78)},
        {'month': '2013-09', 'value': Decimal(59.51)}
    ]

    getcontext().prec = 5
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



    template_vars = {
        'title': '',
        'moment_xindex': moment_xindex,
        'moments': moments,
        'services': services,
        'current_service': service,
        'current_moment': moment,
        'historical_months': historical_months,
        'current_data': current_data,
        'comparison': {'xindex_diff': xindex_diff, 'diff_type': diff_type},
        'data_attribute': data_attribute
    }
    request_context = RequestContext(request, template_vars)
    return render(request, 'reports/moment-report.html', request_context)