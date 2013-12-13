import json
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.template.context import RequestContext
from services.forms import AddService
from django.utils import simplejson

from xindex.models import Service, BusinessUnit, Subsidiary, Moment, \
    sbu_service, Zone, sbu_service_moment_attribute, SubsidiaryBusinessUnit, \
    sbu_service_moment, Question_sbu_s_m_a, Question, Attributes, Survey


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
            print "================================"
            myMomentCounter.append(eachMoment.id_moment.id)

        myMomentCounter = list(set(myMomentCounter))

        touch_count = 0
        indicator_count = 0
        for eachSetMoment in myMomentCounter:
            touch_count += 1

            myAtributtes = sbu_service_moment_attribute.objects.filter(
                id_sbu_service_moment__id_moment__id=eachSetMoment
            )

            for eachAttribute in myAtributtes:
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

    try:
        service = Service.objects.get(id=service_id)
    except Service.DoesNotExist:
        service = False

    if service:
        if request.POST:
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


    #Counters!
    myMomentCounter = []
    myAttributeCounter = []
    mySurveyCounter = []
    for eachMoment in all_sbuServiceMoment:
        myMomentCounter.append(eachMoment.id_moment.id)

    myMomentCounter = list(set(myMomentCounter))

    touch_count = 0
    indicator_count = 0
    question_count = 0
    survey_count = 0
    for eachSetMoment in myMomentCounter:
        touch_count += 1

        myAtributtes = sbu_service_moment_attribute.objects.filter(
            id_sbu_service_moment__id_moment__id=eachSetMoment
        )

        for eachAttribute in myAtributtes:

            myAttributeCounter.append(eachAttribute)
            myQuestions = Question_sbu_s_m_a.objects.filter(
                sbu_s_m_a_id=eachAttribute
            )

            for eachQuestion in myQuestions:
                question_count += 1


                mySurvey = Survey.objects.filter(
                    questions=eachQuestion.question_id
                )

                for eachSurvey in mySurvey:
                    survey_count +=1
                """
                myQuestionsToSurveys = Question.objects.filter(
                    pk=eachQuestion.question_id
                )

                for eachQuestionToSurvey in myQuestionsToSurveys:
                    mySurveyCounter.append(eachQuestionToSurvey)
                """
    myAttributeCounter = list(set(myAttributeCounter))

    for a in myAttributeCounter:
        indicator_count += 1
    #dd

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

    template_vars = {
        'titulo': 'Detalles',
        'service': momentsInService,
        'service_id': service_id,
        'serviceData': Service.objects.get(pk=service_id),
        'counter_moments': touch_count,
        'counter_attributes': indicator_count,
        'counter_questions': question_count,
        'counter_surveys': survey_count,
        'business_unit': 'business_unit'
    }
    request_context = RequestContext(request, template_vars)
    return render_to_response('services/details.html', request_context)


def get_moments(request):
    business_unit = []
    servicesArray = []
    service = []
    momentsArray = []
    momentList = []
    if request.POST:
        if 'zone' in request.POST and 'subsidiary' in request.POST and 'business_unit' in request.POST and 'service' in request.POST:
            if request.POST['zone'] == 'all' or request.POST['subsidiary'] == 'all' or request.POST['business_unit'] == 'all' or request.POST['service'] == 'all':
                if request.POST['zone'] == 'all':
                    zone = Zone.objects.filter(active=True)
                else:
                    zone = Zone.objects.get(pk=int(request.POST['zone']))

                if request.POST['subsidiary'] == 'all':
                    if isinstance(zone, Zone):
                        subsidiary = zone.subsidiary_set.filter(active=True)
                    else:
                        subsidiary = []
                        for z in zone:
                            for s in z.subsidiary_set.filter(active=True):
                                subsidiary.append(s)
                else:
                    subsidiary = Subsidiary.objects.get(pk=int(request.POST['subsidiary']))

                if request.POST['business_unit'] == 'all':
                    if isinstance(subsidiary, Subsidiary):
                        for subsidiary_business_unit in SubsidiaryBusinessUnit.objects.filter(id_subsidiary=subsidiary):
                            coincidences = 0
                            for bu in business_unit:
                                if subsidiary_business_unit.id_business_unit == bu:
                                    coincidences += 1
                            if coincidences == 0:
                                business_unit.append(subsidiary_business_unit.id_business_unit)
                    else:
                        for sub in subsidiary:
                            for subsidiary_business_unit in SubsidiaryBusinessUnit.objects.filter(id_subsidiary=sub):
                                coincidences = 0
                                for bu in business_unit:
                                    if subsidiary_business_unit.id_business_unit == bu:
                                        coincidences += 1
                                if coincidences == 0:
                                    business_unit.append(subsidiary_business_unit.id_business_unit)
                else:
                    business_unit = BusinessUnit.objects.get(pk=int(request.POST['business_unit']))

                if request.POST['service'] == 'all':
                    if isinstance(subsidiary, Subsidiary):
                        if isinstance(business_unit, BusinessUnit):
                            for subsidiary_business_unit in SubsidiaryBusinessUnit.objects.filter(id_subsidiary=subsidiary, id_business_unit=business_unit):
                                for s_bu_s in sbu_service.objects.filter(id_subsidiaryBU=subsidiary_business_unit):
                                    coincidences = 0
                                    for serviceA in service:
                                        if serviceA == s_bu_s.id_service:
                                            coincidences += 1
                                    if coincidences == 0:
                                        service.append(s_bu_s.id_service)
                        else:
                            for bu in business_unit:
                                try:
                                    s_bu = SubsidiaryBusinessUnit.objects.filter(id_subsidiary=subsidiary, id_business_unit=bu)
                                    for subsidiary_business_unit in s_bu:
                                        for s_bu_s in sbu_service.objects.filter(id_subsidiaryBU=subsidiary_business_unit):
                                            coincidences = 0
                                            for serviceA in service:
                                                if serviceA == s_bu_s.id_service:
                                                    coincidences += 1
                                            if coincidences == 0:
                                                service.append(s_bu_s.id_service)
                                except SubsidiaryBusinessUnit.DoesNotExist:
                                    pass
                    else:
                        print request.POST
                        if isinstance(business_unit, BusinessUnit):
                            for subs in subsidiary:
                                try:
                                    s_bu = SubsidiaryBusinessUnit.objects.filter(id_subsidiary=subs, id_business_unit=business_unit)
                                    for subsidiary_business_unit in s_bu:
                                        for s_bu_s in sbu_service.objects.filter(id_subsidiaryBU=subsidiary_business_unit):
                                            coincidences = 0
                                            for serviceA in service:
                                                if serviceA == s_bu_s.id_service:
                                                    coincidences += 1
                                            if coincidences == 0:
                                                service.append(s_bu_s.id_service)
                                except SubsidiaryBusinessUnit.DoesNotExist:
                                    pass
                        else:
                            for subs in subsidiary:
                                for bu_un in business_unit:
                                    try:
                                        s_bu = SubsidiaryBusinessUnit.objects.filter(id_subsidiary=subs, id_business_unit=bu_un)
                                        for subsidiary_business_unit in s_bu:
                                            for s_bu_s in sbu_service.objects.filter(id_subsidiaryBU=subsidiary_business_unit):
                                                coincidences = 0
                                                for serviceA in service:
                                                    if serviceA == s_bu_s.id_service:
                                                        coincidences += 1
                                                if coincidences == 0:
                                                    service.append(s_bu_s.id_service)
                                    except SubsidiaryBusinessUnit.DoesNotExist:
                                        pass
                else:
                    service = Service.objects.get(pk=int(request.POST['service']))

                print service

                if isinstance(subsidiary, Subsidiary):
                    #subsidiary IS an instance
                    if isinstance(business_unit, BusinessUnit):
                        #subsidiary IS an instance and business unit IS an instance
                        if isinstance(service, Service):
                            #subsidiary IS an instance and business unit IS an instance and service IS an instance
                            for subsidiary_business_unit in SubsidiaryBusinessUnit.objects.filter(id_subsidiary=subsidiary, id_business_unit=business_unit):
                                for s_bu_s in sbu_service.objects.filter(id_subsidiaryBU=subsidiary_business_unit, id_service=service):
                                    for s_bu_s_m in sbu_service_moment.objects.filter(id_sbu_service=s_bu_s):
                                        coincidences = 0
                                        for momentA in momentsArray:
                                            if momentA == s_bu_s_m.id_moment:
                                                coincidences += 1
                                        if coincidences == 0:
                                            momentsArray.append(s_bu_s_m.id_moment)
                                            momentList.append(
                                                {
                                                    'moment_id': s_bu_s_m.id_moment.id,
                                                    'moment_name': s_bu_s_m.id_moment.name + ' - ' + s_bu_s_m.alias
                                                }
                                            )
                        else:
                            #subsidiary IS an instance and business unit IS an instance and service IS NOT an instance
                            for subsidiary_business_unit in SubsidiaryBusinessUnit.objects.filter(id_subsidiary=subsidiary, id_business_unit=business_unit):
                                for serv in service:
                                    for s_bu_s in sbu_service.objects.filter(id_subsidiaryBU=subsidiary_business_unit, id_service=serv):
                                        for s_bu_s_m in sbu_service_moment.objects.filter(id_sbu_service=s_bu_s):
                                            coincidences = 0
                                            for momentA in momentsArray:
                                                if momentA == s_bu_s_m.id_moment:
                                                    coincidences += 1
                                            if coincidences == 0:
                                                momentsArray.append(s_bu_s_m.id_moment)
                                                momentList.append(
                                                    {
                                                        'moment_id': s_bu_s_m.id_moment.id,
                                                        'moment_name': s_bu_s_m.id_moment.name + ' - ' + s_bu_s_m.alias
                                                    }
                                                )
                    else:
                        #subsidiary IS an instance and business unit IS NOT an instance
                        if isinstance(service, Service):
                            #subsidiary IS an instance and business unit IS NOT an instance and service IS an instance
                            for bu in business_unit:
                                try:
                                    s_bu = SubsidiaryBusinessUnit.objects.filter(id_subsidiary=subsidiary, id_business_unit=bu)
                                    for subsidiary_business_unit in s_bu:
                                        try:
                                            s_bu_ser = sbu_service.objects.filter(id_subsidiaryBU=subsidiary_business_unit, id_service=service)
                                            for s_bu_s in s_bu_ser:
                                                for s_bu_s_m in sbu_service_moment.objects.filter(id_sbu_service=s_bu_s):
                                                    coincidences = 0
                                                    for momentA in momentsArray:
                                                        if momentA == s_bu_s_m.id_moment:
                                                            coincidences += 1
                                                    if coincidences == 0:
                                                        momentsArray.append(s_bu_s_m.id_moment)
                                                        momentList.append(
                                                            {
                                                                'moment_id': s_bu_s_m.id_moment.id,
                                                                'moment_name': s_bu_s_m.id_moment.name + ' - ' + s_bu_s_m.alias
                                                            }
                                                        )
                                        except sbu_service.DoesNotExist:
                                            pass
                                except SubsidiaryBusinessUnit.DoesNotExist:
                                    pass
                        else:
                            #subsidiary IS an instance and business unit IS NOT an instance and service IS NOT an instance
                            for bu in business_unit:
                                for serv in service:
                                    try:
                                        s_bu = SubsidiaryBusinessUnit.objects.filter(id_subsidiary=subsidiary, id_business_unit=bu)
                                        for subsidiary_business_unit in s_bu:
                                            for s_bu_s in sbu_service.objects.filter(id_subsidiaryBU=subsidiary_business_unit, id_service=serv):
                                                for s_bu_s_m in sbu_service_moment.objects.filter(id_sbu_service=s_bu_s):
                                                    coincidences = 0
                                                    for momentA in momentsArray:
                                                        if momentA == s_bu_s_m.id_moment:
                                                            coincidences += 1
                                                    if coincidences == 0:
                                                        momentsArray.append(s_bu_s_m.id_moment)
                                                        momentList.append(
                                                            {
                                                                'moment_id': s_bu_s_m.id_moment.id,
                                                                'moment_name': s_bu_s_m.id_moment.name + ' - ' + s_bu_s_m.alias
                                                            }
                                                        )
                                    except SubsidiaryBusinessUnit.DoesNotExist:
                                        pass

                else:
                    #subsidiary IS NOT an instance
                    if isinstance(business_unit, BusinessUnit):
                        #subsidiary IS NOT an instance and business unit IS an instance
                        if isinstance(service, Service):
                            #subsidiary IS an instance and business unit IS an instance and service IS an instance
                            for subs in subsidiary:
                                for subsidiary_business_unit in SubsidiaryBusinessUnit.objects.filter(id_subsidiary=subs, id_business_unit=business_unit):
                                    for s_bu_s in sbu_service.objects.filter(id_subsidiaryBU=subsidiary_business_unit, id_service=service):
                                        for s_bu_s_m in sbu_service_moment.objects.filter(id_sbu_service=s_bu_s):
                                            coincidences = 0
                                            for momentA in momentsArray:
                                                if momentA == s_bu_s_m.id_moment:
                                                    coincidences += 1
                                            if coincidences == 0:
                                                momentsArray.append(s_bu_s_m.id_moment)
                                                momentList.append(
                                                    {
                                                        'moment_id': s_bu_s_m.id_moment.id,
                                                        'moment_name': s_bu_s_m.id_moment.name + ' - ' + s_bu_s_m.alias
                                                    }
                                                )
                        else:
                            #subsidiary IS NOT an instance and business unit IS an instance and service IS NOT an instance
                            for subs in subsidiary:
                                for subsidiary_business_unit in SubsidiaryBusinessUnit.objects.filter(id_subsidiary=subs, id_business_unit=business_unit):
                                    for serv in service:
                                        for s_bu_s in sbu_service.objects.filter(id_subsidiaryBU=subsidiary_business_unit, id_service=serv):
                                            for s_bu_s_m in sbu_service_moment.objects.filter(id_sbu_service=s_bu_s):
                                                coincidences = 0
                                                for momentA in momentsArray:
                                                    if momentA == s_bu_s_m.id_moment:
                                                        coincidences += 1
                                                if coincidences == 0:
                                                    momentsArray.append(s_bu_s_m.id_moment)
                                                    momentList.append(
                                                        {
                                                            'moment_id': s_bu_s_m.id_moment.id,
                                                            'moment_name': s_bu_s_m.id_moment.name + ' - ' + s_bu_s_m.alias
                                                        }
                                                    )
                    else:
                        #subsidiary IS NOT an instance and business unit IS NOT an instance
                        if isinstance(service, Service):
                            #subsidiary IS NOT an instance and business unit IS NOT an instance and service IS an instance
                            for subs in subsidiary:
                                for bu in business_unit:
                                    try:
                                        s_bu = SubsidiaryBusinessUnit.objects.filter(id_subsidiary=subs, id_business_unit=bu)
                                        for subsidiary_business_unit in s_bu:
                                            try:
                                                s_bu_ser = sbu_service.objects.filter(id_subsidiaryBU=subsidiary_business_unit, id_service=service)
                                                for s_bu_s in s_bu_ser:
                                                    for s_bu_s_m in sbu_service_moment.objects.filter(id_sbu_service=s_bu_s):
                                                        coincidences = 0
                                                        for momentA in momentsArray:
                                                            if momentA == s_bu_s_m.id_moment:
                                                                coincidences += 1
                                                        if coincidences == 0:
                                                            momentsArray.append(s_bu_s_m.id_moment)
                                                            momentList.append(
                                                                {
                                                                    'moment_id': s_bu_s_m.id_moment.id,
                                                                    'moment_name': s_bu_s_m.id_moment.name + ' - ' + s_bu_s_m.alias
                                                                }
                                                            )
                                            except sbu_service.DoesNotExist:
                                                pass
                                    except SubsidiaryBusinessUnit.DoesNotExist:
                                        pass
                        else:
                            #subsidiary IS NOT an instance and business unit IS NOT an instance and service IS NOT an instance
                            for subs in subsidiary:
                                for bu in business_unit:
                                    for serv in service:
                                        try:
                                            s_bu = SubsidiaryBusinessUnit.objects.filter(id_subsidiary=subs, id_business_unit=bu)
                                            for subsidiary_business_unit in s_bu:
                                                for s_bu_s in sbu_service.objects.filter(id_subsidiaryBU=subsidiary_business_unit, id_service=serv):
                                                    for s_bu_s_m in sbu_service_moment.objects.filter(id_sbu_service=s_bu_s):
                                                        coincidences = 0
                                                        for momentA in momentsArray:
                                                            if momentA == s_bu_s_m.id_moment:
                                                                coincidences += 1
                                                        if coincidences == 0:
                                                            momentsArray.append(s_bu_s_m.id_moment)
                                                            momentList.append(
                                                                {
                                                                    'moment_id': s_bu_s_m.id_moment.id,
                                                                    'moment_name': s_bu_s_m.id_moment.name + ' - ' + s_bu_s_m.alias
                                                                }
                                                            )
                                        except SubsidiaryBusinessUnit.DoesNotExist:
                                            pass

                if len(momentList) == 0:
                        pass
                else:
                    json_response = {
                        'answer': True,
                        'moments': momentList
                    }
                    return HttpResponse(json.dumps(json_response))
            else:
                try:
                    zone = Zone.objects.get(pk=int(request.POST['zone']))
                    subsidiary = zone.subsidiary_set.get(
                        pk=int(request.POST['subsidiary'])
                    )
                    for subsidiary_business_unit in SubsidiaryBusinessUnit.objects.filter(
                            id_subsidiary=subsidiary,
                            id_business_unit=int(request.POST['business_unit'])):

                        for s_bu_s in sbu_service.objects.filter(
                                id_subsidiaryBU=subsidiary_business_unit,
                                id_service=int(request.POST['service'])):

                            for s_bu_s_m in sbu_service_moment.objects.filter(
                                    id_sbu_service=s_bu_s):
                                momentList.append(
                                    {
                                        'moment_id': s_bu_s_m.id_moment.id,
                                        'moment_name': s_bu_s_m.id_moment.name + ' - ' + s_bu_s_m.alias
                                    }
                                )
                    if len(momentList) == 0:
                        pass
                    else:
                        json_response = {
                            'answer': True,
                            'moments': momentList
                        }
                        return HttpResponse(json.dumps(json_response))
                except Zone.DoesNotExist:
                    pass
        else:
            pass


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