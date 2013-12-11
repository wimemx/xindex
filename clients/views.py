import csv
import json
import os
import short_url
from django.shortcuts import render_to_response, HttpResponse, \
    HttpResponseRedirect, get_object_or_404
from django.template.context import RequestContext
from django.utils import simplejson
from django.contrib.auth.decorators import login_required, user_passes_test

from xindex.models import Subsidiary, Zone, SubsidiaryBusinessUnit, \
    sbu_service, Client, Company, ClientActivity, BusinessUnit, Service, \
    Survey, Question, Answer
from clients.functions import mailing, addClientFromCSV, addClientActivity, \
    addActivity


@login_required(login_url='/signin/')
def client_list(request):

    template_vars = {}
    request_context = RequestContext(request, template_vars)
    return render_to_response("clients/client_list.html", request_context)


@login_required(login_url='/signin/')
#@user_passes_test(lambda u: u.is_superuser)
def getClientsInJson(request):
    clients = {'clients': []}

    clientQuery = Client.objects.filter(active=True)

    for eachClient in clientQuery:

        clients['clients'].append(
            {
                "first_name": eachClient.first_name,
                "last_name": eachClient.last_name,
                "email": eachClient.email,
                "company": eachClient.company.name,
                "state": eachClient.state,
                "city": eachClient.city,
                "rating": eachClient.rating,
                "actions": eachClient.id
            }
        )

    return HttpResponse(simplejson.dumps(clients))


@login_required(login_url='/signin/')
def add_client(request):

    if request.POST:
        company = Company.objects.get(pk=request.POST['client_company'])

        new_client = Client.objects.create(
            first_name=request.POST['client_name'],
            last_name=request.POST['client_surname'],
            sex=request.POST['client_sex'],
            #date_of_birth=request.POST['client_date'],
            email=request.POST['client_email'],
            phone=request.POST['client_phone'],
            company=company,)

        new_client.save()
        return HttpResponseRedirect('/clients/')

    else:
        companies = Company.objects.filter(active=True)[:1]
        zones = Zone.objects.filter(active=True)
        subsidiaries = Subsidiary.objects.filter(zone=zones[0], active=True)
        businessUnits = SubsidiaryBusinessUnit.objects.filter(
            id_subsidiary__id=subsidiaries[0].id)
        sbu_services = sbu_service.objects.filter(
            id_subsidiaryBU__id_subsidiary__id=businessUnits[0].id_subsidiary.id
        )
        template_vars = {'companies': companies,
                         'zones': zones,
                         'zone': zones[0],
                         'subsidiaries': subsidiaries,
                         'businessUnits': businessUnits,
                         'sbu_services': sbu_services}
        request_context = RequestContext(request, template_vars)
        return render_to_response("clients/add_client.html", request_context)


@login_required(login_url='/signin/')
def remove_client(request,  client_id):

    client = Client.objects.get(pk=client_id)
    client.active = False
    client.save()

    return HttpResponse('Si')


@login_required(login_url='/signin/')
def edit_client(request, client_id):

    client = Client.objects.get(pk=client_id)

    if request.POST:
        company = Company.objects.get(pk=request.POST['client_company'])

        client.name = request.POST['client_name']
        client.first_name = request.POST['client_name']
        client.last_name = request.POST['client_surname']
        client.sex = request.POST['client_sex']
        client.email = request.POST['client_email']
        #client.date_of_birth = request.POST['client_date']
        client.phone = request.POST['client_phone']
        client.company = company
        client.save()

        return HttpResponseRedirect('/clients/')
    else:

        companies = Company.objects.filter(active=True)

        template_vars = {'id': client.id,
                         'name': client.first_name,
                         'surname': client.last_name,
                         'email': client.email,
                         'phone': client.phone,
                         #'date': client.date_of_birth,
                         'sex': client.sex,
                         'company': client.company,
                         'companies': companies}

        request_context = RequestContext(request, template_vars)
        return render_to_response("clients/edit_client.html", request_context)


'''
@login_required(login_url='/signin/')
def csv_read_prueba(request):

    fileToAdd = open("/home/osvaldomg/Documentos/clients.csv")

    reader = csv.reader(fileToAdd, delimiter=',', quotechar='|')
    for eachRow in reader:

        clientData = Client.objects.create(
            name=eachRow[1],
            first_name=eachRow[2],
            last_name=eachRow[3],
            sex=eachRow[4],
            date_of_birth=eachRow[5],
            email=eachRow[6],
            phone=eachRow[7],
            state=eachRow[8],
            city=eachRow[9],
            company=Company.objects.get(name=eachRow[10])
        )

        clientData.save()
    return HttpResponseRedirect('/clients/')
'''


@login_required(login_url='/signin/')
def csv_read(request):

    if request.method == 'POST':
        clients = request.POST.getlist("newClient")
        activity = request.POST.getlist("id_activity")

        for eachClient in clients:
            clientData = str(eachClient).split("},")

            for eachClientData in clientData:
                if eachClientData[-1] != "}":
                    eachClientData += "}"

                modelField = json.loads(eachClientData)["name"]
                fieldData = json.loads(eachClientData)["value"]

                if modelField == "email":
                    if Client.objects.filter(email=fieldData).exists():
                        if activity:
                            client = Client.objects.get(email=fieldData)
                            addActivity(client, activity)
                    else:
                        if activity:
                            addClientActivity(eachClient, activity)
                        else:
                            addClientFromCSV(eachClient)

    return HttpResponse("Yes")


    '''
    if request.POST:

        path = os.path.join(
            os.path.dirname(__file__), '..',
            'templates/static/csv/').replace('\\', '/')

        path += str(request.FILES['client_csv'])

        fileToUp = request.FILES['client_csv']
        handle_uploaded_file(path, fileToUp)

        fileToAdd = open(path)

        reader = csv.reader(fileToAdd, delimiter=',', quotechar='|')

        print reader
        counterLoop = 0
        for eachRow in reader:
            if counterLoop == 0:
                counterLoop += 1
                continue
            subsidiary = Subsidiary.objects.get(name=eachRow[7], active=True)

            if Client.objects.filter(email=eachRow[4]).exists():
                print '=====EL CLIENTE YA EXISTE====='

            else:
                clientData = Client.objects.create(
                    first_name=eachRow[1],
                    last_name=eachRow[2],
                    sex=eachRow[3],
                    email=eachRow[4],
                    phone=eachRow[5],
                    company=subsidiary.company
                )

                clientData.save()

                activityData = ClientActivity.objects.create(
                    client=clientData,
                    date=eachRow[6],
                    subsidiary=subsidiary,
                    business_unit=BusinessUnit.objects.get(name=eachRow[8],
                                                           active=True),
                    service=Service.objects.get(name=eachRow[9], active=True)
                )
                activityData.save()

                url = short_url.encode_url(clientData.id)
                print url

        fileToAdd.close()
        if fileToAdd.closed:
            os.remove(path)

        return HttpResponseRedirect('/clients/')

    else:

        template_vars = {}
        request_context = RequestContext(request, template_vars)
        return render_to_response("clients/add_csv.html", request_context)
    '''


def handle_uploaded_file(destination, f):
    with open(destination, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


@login_required(login_url='/signin/')
def getAnswersByClient(request, client_id):
    client = Client.objects.get(pk=client_id)
    clientActivity = ClientActivity.objects.filter(client__id=client.id)

    template_vars = {
        "client": client,
        "activities": clientActivity
    }
    request_context = RequestContext(request, template_vars)
    return render_to_response("clients/details.html", request_context)


@login_required(login_url='/signin/')
#@user_passes_test(lambda u: u.is_superuser)
def getClientActivityInJson(request, client_id):
    activity = {'activity': []}

    clientActivity = ClientActivity.objects.filter(
        client__id=client_id
    )

    for eachActivity in clientActivity:

        activity['activity'].append(
            {
                "id": eachActivity.id,
                "date": str(eachActivity.date),
                "subsidiary": eachActivity.subsidiary.name,
                "rating": eachActivity.client.rating,
                "status": eachActivity.status
            }
        )

    return HttpResponse(simplejson.dumps(activity))


@login_required(login_url='/signin/')
def activity_answers(request, activity_id):
    errors = []
    try:
        activity = ClientActivity.objects.get(pk=int(activity_id))
        client = Client.objects.get(pk=activity.client_id)

        if activity.survey_id is not None:
            survey = Survey.objects.get(pk=activity.survey_id)
            configuration = json.loads(survey.configuration)

            #get the company name
            companies = survey.user.company_set.all()

            for company in companies:
                company_name = company.name
                company_address = company.address
                company_email = company.email
                company_phone = company.phone

            setup = {
                'blocks': [],
                'question_styles': False
            }

            for key, values in configuration.items():
                if key == 'blocks':
                    for block in values:
                        questions = []
                        for q in block['questions']:
                            if 'db_id' in q:

                                try:
                                    question = Question.objects.get(
                                        pk=q['db_id'])
                                    options = question.option_set.filter(
                                        active=True).order_by('id')

                                    moment_title = False
                                    attribute_title = False
                                    #end check

                                    options_o = []
                                    for option in options:
                                        options_o.append(
                                            {
                                                'id_option': option.id,
                                                'text': option.label,
                                                'option': option
                                            }
                                        )
                                    if 'question_style' in q:
                                        style = q['question_style']
                                    else:
                                        style = False

                                    if question.type.name == 'Matrix':
                                        sub_questions = question.question_set.filter(
                                            active=True).order_by('id')
                                    else:
                                        sub_questions = False
                                    try:
                                        answer = Answer.objects.get(question=question, client=client)
                                    except Answer.DoesNotExist:
                                        answer = False

                                    questions.append(
                                        {
                                            'question': question,
                                            'answer': answer,
                                            'sub_questions': sub_questions,
                                            'moment_title': moment_title,
                                            'attribute_title': attribute_title,
                                            'question_style': style,
                                            'survey_question_id': q['question_survey_id'],
                                            'question_content_id': q['question_content_id'],
                                            'db_question_id': q['db_id'],
                                            'question_title': question.title,
                                            'question_type': question.type.id,
                                            'question_type_name': question.type.name,
                                            'question_options': options_o
                                        }
                                    )
                                except Question.DoesNotExist:
                                    question = None

                        if 'block_description' in block:
                            block_description = block['block_description']
                        else:
                            block_description = ''
                        if 'style' in block:
                            style = block['style']
                        else:
                            style = ''
                        if 'block_moment_associated_id' in block:
                            block_moment_associated_id = block['block_moment_associated_id']
                        else:
                            block_moment_associated_id = False
                        if 'block_type' in block:
                            block_type = block['block_type']
                        else:
                            block_type = 'questions_block'

                        setup['blocks'].append(
                            {
                                'block_id': block['block_id'],
                                'block_default_class': block['class_default'],
                                'block_description': block_description,
                                'style': style,
                                'questions': questions,
                                'block_moment_associated_id': block_moment_associated_id,
                                'block_type': block_type
                            }
                        )
                if key == 'blocks_style':
                    setup['blocks_style'] = values
                if key == 'questions_style':
                    setup['questions_style'] = values
                if key == 'block_border_color':
                    setup['block_border_color'] = values
                if key == 'block_border_style':
                    setup['block_border_style'] = values
                if key == 'block_border_width':
                    setup['block_border_width'] = values
                if key == 'block_background_color':
                    setup['block_background_color'] = values
                if key == 'block_box_shadow':
                    setup['block_box_shadow'] = values
                if survey.picture:
                    setup['survey_picture'] = survey.picture
            client = Client.objects.get(pk=activity.client_id)
            template_vars = {
                'survey_title': survey.name,
                'survey_id': survey.id,
                'company_name': company_name,
                'company_address': company_address,
                'company_email': company_email,
                'company_phone': company_phone,
                'client_id': activity.client_id,
                'client_name': client.first_name+' '+client.last_name,
                'setup': setup
            }
        else:
            errors.append(
                {
                    'error_type': 'Encuesta',
                    'error_message': 'La encuesta ha sido borrada'
                }
            )
            template_vars = {
                'errors': errors
            }

    except ClientActivity.DoesNotExist:
        errors.append(
            {
                'error_type': 'Actividad del cliente',
                'error_message': 'No se ha podido encontrar la actividad'
            }
        )

        template_vars = {
            'errors': errors
        }

    request_context = RequestContext(request, template_vars)
    return render_to_response("clients/activity_answers.html", request_context)


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


def getServicesInJson(request, business_id):

    servicesToJson = {'services': []}

    sbuService = sbu_service.objects.filter(
        id_subsidiaryBU__id_business_unit=business_id
    )

    if sbuService:
        for eachService in sbuService:
            services = Service.objects.get(
                pk=eachService.id_service.id,
                active=True
            )

            servicesToJson['services'].append(
                {
                    "name": services.name,
                    "id": services.id
                }
            )

    return HttpResponse(simplejson.dumps(servicesToJson))


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