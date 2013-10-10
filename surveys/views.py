# -*- encoding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, render_to_response
from django.template.context import RequestContext
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.utils import simplejson
from xindex.models import Survey, Question_Attributes, Company
from xindex.forms import SurveyForm
from xindex.models import Xindex_User
from xindex.models import Question_Type
import os
import json
from collections import namedtuple
from django.views.decorators.csrf import csrf_exempt
from xindex.models import Question
from xindex.models import Option
from xindex.models import Catalog
from xindex.models import Moment
from xindex.models import Service
from xindex.models import Attributes


@login_required(login_url='/signin/')
def index(request):
    surveys = {'surveys': []}
    survey_query = Survey.objects.filter(active=True).order_by('name')
    question_attribute_query = Question_Attributes.objects.all()

    for each_survey in survey_query:
        counter_question = 0
        counter_attributes = 0

        for each_question in each_survey.questions.all():
            counter_question += 1

            for each_question_attribute in question_attribute_query:
                if each_question == each_question_attribute.question_id:
                    counter_attributes += 1

        surveys['surveys'].append(
            {
                "id": each_survey.id,
                "name": each_survey.name,
                "date": each_survey.date,
                "status": each_survey.available,
                "counter_question": counter_question,
                "counter_attribute": counter_attributes,
                "next_step": each_survey.step
            }
        )
    template_vars = {"title": "Surveys",
                     "surveys": surveys,
                     "order_query": "Nombre"}
    request_context = RequestContext(request, template_vars)
    return render(request, 'surveys/index.html', request_context)


@login_required(login_url='/signin/')
def indexOrder(request, order_type):
    surveys = {'surveys': []}
    survey_query = Survey.objects.filter(active=True).order_by(order_type)
    question_attribute_query = Question_Attributes.objects.all()

    for each_survey in survey_query:
        counter_question = 0
        counter_attributes = 0

        for each_question in each_survey.questions.all():
            counter_question += 1

            for each_question_attribute in question_attribute_query:
                if each_question == each_question_attribute.question_id:
                    counter_attributes += 1

        surveys['surveys'].append(
            {
                "id": each_survey.id,
                "name": each_survey.name,
                "date": each_survey.date,
                "status": each_survey.available,
                "counter_question": counter_question,
                "counter_attribute": counter_attributes,
                "next_step": each_survey.step
            }
        )

    if order_type == 'name':
        order_query = 'Nombre'
    elif order_type == 'available':
        order_query = 'Status'
    elif order_type == 'date':
        order_query = 'Fecha de creación'

    template_vars = {"title": "Surveys",
                     "surveys": surveys,
                     "order_query": order_query}
    request_context = RequestContext(request, template_vars)
    return render(request, 'surveys/index.html', request_context)


@login_required(login_url='/signin/')
def getJson(request):
    survey = {'surveys': []}
    survey_query = Survey.objects.filter(active=True).order_by('-date')

    for each_survey in survey_query:
        survey['surveys'].append(
            {
                "name": each_survey.name
            }
        )
    return HttpResponse(simplejson.dumps(survey))


def addSurvey(request):
    if request.POST:
        a= "paso"
    else:
        form = SurveyForm()
        template_vars = {
            'title': 'Agregar Encuesta',
            "form": form
        }
        request_context = RequestContext(request, template_vars)
        return render_to_response('surveys/add.html', request_context)


def add_step(request, step=1, survey_id=False):
    if survey_id:
        try:
            survey = Survey.objects.get(pk=survey_id)
        except Survey.DoesNotExist:
            survey = False
    else:
        survey = False

    if survey:
        if step == 1:
            template_vars = {
                'survey_title': survey.name,
                'step': survey.id,
                'survey_id': survey_id
            }
            request_context = RequestContext(request, template_vars)
            return render_to_response('surveys/add-step-1.html')

    else:
        return HttpResponseRedirect('/surveys/add')


def save(request, action, next_step, survey_id=False):
    if survey_id == 'empty':
        if request.POST:
            form = SurveyForm(request.POST)
            if form.is_valid():
                step = int(next_step)
                xindex_user = Xindex_User.objects.get(user__id=request.user.id)

                configuration = {'header_logo': '', 'body': '', 'footer': ''}
                configuration = simplejson.dumps(configuration)

                print configuration

                survey = Survey(user=xindex_user,
                                name=form.cleaned_data['name'],
                                step=step,
                                configuration=configuration)
                survey.save()

                print 'Se ha guardado PASO___' + str(step)

                new_url = '/surveys/save/next/2/'+str(survey.id)

                answer = {'save': True, 'url': new_url}

                print answer

                return HttpResponse(simplejson.dumps(answer))
            else:
                answer = {'save': False,
                          'error': 'El nombre de la encuesta no es valido'}

                return HttpResponse(simplejson.dumps(answer))
    else:
        survey_id = int(survey_id)
        survey = Survey.objects.get(pk=survey_id)
        xindex_user = Xindex_User.objects.get(user__id=request.user.id)
        try:
            company = Company.objects.get(staff=xindex_user)
        except:
            company = False

        if company:
            company_name = company.name
            company_address = company.address
            company_email = 'atencion@hollidayinn.com'
            company_phone = company.phone
        else:
            company_name = 'Default company NAME'
            company_address = 'Default company ADDRESS'
            company_email = 'Default company EMAIL'
            company_phone = 'Default company PHONE'

        if int(next_step) == 2 and action == 'next':
            survey.step = 2
            survey.save()

            template_vars = {
                'survey_title': survey.name,
                'survey_id': survey.id,
                'next_step': str(int(next_step)+1)
            }
            request_context = RequestContext(request, template_vars)
            return render_to_response('surveys/add-step-2.html',
                                      request_context)

        question_types = Question_Type.objects.all().order_by('name')
        if int(next_step) == 3 and action == 'next':
            survey.step = 3
            survey.save()

            configuration = json.loads(survey.configuration)

            setup = {}
            setup['blocks'] = []

            setup['moments'] = []

            setup['attributes'] = []

            user = Xindex_User.objects.get(pk=request.user.id)

            for company in user.company_set.all():
                for subsidiary in company.subsidiary_set.all():
                    for business_unit in subsidiary.businessunit_set.all():
                        for service in business_unit.service.all():
                            for moment in service.moments.all():
                                setup['moments'].append(
                                    {
                                        'moment': moment
                                    }
                                )

            attributes = Attributes.objects.all()

            for attribute in attributes:
                setup['attributes'].append(
                    {
                        'attribute': attribute
                    }
                )



            #print simplejson.dumps(configuration)
            for key, values in configuration.items():
                for block in values:
                    questions = []
                    for q in block['questions']:
                        if 'db_id' in q:

                            try:
                                question = Question.objects.get(pk=q['db_id'])
                                options = question.option_set.all().order_by('id')

                                #Check if question is associated to a moment
                                try:
                                    association = Question_Attributes.objects.get(question_id=question)
                                    if association.moment_id is None:
                                        moment_title = False
                                    else:
                                        moment_title = association.moment_id.name

                                    if association.attribute_id is None:
                                        attribute_title = False
                                    else:
                                        attribute_title = association.attribute_id.name

                                except Question_Attributes.DoesNotExist:
                                    moment_title = False
                                    attribute_title = False
                                #end check

                                print moment_title
                                print attribute_title

                                options_o = []
                                for option in options:
                                    options_o.append(
                                        {
                                            'id_option': option.id,
                                            'text': option.label,
                                            'option': option
                                        }
                                    )
                                questions.append(
                                    {
                                        'question': question,
                                        'moment_title': moment_title,
                                        'attribute_title': attribute_title,
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
                    setup['blocks'].append(
                        {
                            'block_id': block['block_id'],
                            'block_default_class': block['class_default'],
                            'block_description': block_description,
                            'questions': questions
                        }
                    )

            template_vars = {
                'survey_title': survey.name,
                'survey_id': survey.id,
                'next_step': str(int(next_step)+1),
                'question_types': question_types,
                'company_name': company_name,
                'company_address': company_address,
                'company_email': company_email,
                'company_phone': company_phone,
                'setup': setup
            }
            request_context = RequestContext(request, template_vars)
            return render_to_response('surveys/add-step-3.html',
                                      request_context)


def edit(request, survey_id):
    survey = Survey.objects.get(pk=survey_id)
    if request.method == 'POST':
        form = SurveyForm(request.POST, instance=survey)
        if form.is_valid():
            form.save()
            template_vars = {
                'survey_title': survey.name,
                'survey_id': survey.id,
                'next_step': 3
            }
            request_context = RequestContext(request, template_vars)
            return render_to_response('surveys/add-step-2.html',
                                      request_context)
    else:
        form = SurveyForm(instance=survey)

    return render(request, 'surveys/add-step-1.html',
                  {"formulario": form,
                   "survey_id": survey_id})


@login_required(login_url='/signin/')
def available(request, survey_id):

    try:
        survey = Survey.objects.get(pk=survey_id)
    except Survey.DoesNotExist:
        survey = False

    if survey.available:
        survey.available = False
        survey.save()
    else:
        survey.available = True
        survey.save()

    return HttpResponseRedirect('/surveys/')


@login_required(login_url='/signin/')
def media_upload(request, survey_id):
    survey = Survey.objects.get(pk=survey_id)
    survey.picture = str(survey.id) + str(request.FILES['file'])
    survey.save()

    path = os.path.join(
        os.path.dirname(__file__), '..',
        'templates/media/pictures/').replace('\\', '/')

    path += str(survey.id) + str(request.FILES['file'])
    file = request.FILES['file']
    handle_uploaded_file(path, file)
    context = {}
    context = simplejson.dumps(context)
    return HttpResponse(context, mimetype='application/json')


def handle_uploaded_file(destination, f):
    with open(destination, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


'''
def media_upload(request):

   folder = '/entity/'
   if 'event_picture' in request.POST:
       folder = '/event/'
   if 'event_cover_picture' in request.POST:
       folder = '/event/'
   if 'edit_profile' in request.POST:
       folder = '/profile/'
       id_user = request.user.id
       user = models.Profile.objects.get(user=id_user)
       user.picture = str(request.FILES['file'])
       user.save()

   if 'list_picture' in  request.POST:
       folder = '/list/'

   path_extension = str(request.user.id)+folder
   path = os.path.join(
       os.path.dirname(__file__), '..',
       'static/media/users/'+path_extension).replace('\\', '/')

   path += str(request.FILES['file'])
   file = request.FILES['file']
   handle_uploaded_file(path, file)
   context = {}
   context = simplejson.dumps(context)
   return HttpResponse(context, mimetype='application/json')

def handle_uploaded_file(destination, f):
   with open(destination, 'wb+') as destination:
       for chunk in f.chunks():
           destination.write(chunk)

           '''


@csrf_exempt
def save_ajax(request, survey_id):
    if request.is_ajax():
        try:
            data = json.loads(request.body,
                              object_hook=lambda d: namedtuple('X', d.keys())
                                  (*d.values())
            )
            #TODO: Search for types in the table question_type to avoid hardcoding
            try:
                survey = Survey.objects.get(pk=survey_id)
            except Survey.DoesNotExist:
                survey = False

            if survey:
                survey.configuration = request.body
                survey.save()
                json_response = json.dumps(
                    {'answer' : True}
                )
            else:
                json_response = json.dumps(
                    {
                        'answer': False
                    }
                )

            return HttpResponse(json_response,
                                content_type="application/json")
        except ValueError:
            json_response = json.dumps(
                    {'messagesent': "Error - Invalid json"}
            )
            return HttpResponse(json_response,
                                content_type="application/json")
    else:
        raise Http404



def delete_questions(request):
    if request.is_ajax():

        question_ids = json.loads(request.POST.get('ids'))

        print request.POST['survey_id']

        survey = Survey.objects.get(pk=int(request.POST['survey_id']))

        for question in question_ids:
            q = Question.objects.get(pk=int(question['question_id']))
            survey.questions.remove(q)

        json_response = json.dumps(
            {
                'success': True
            }
        )
        return HttpResponse(json_response, content_type="application/json")


def associate_questions_to_moments(request):
    if request.is_ajax():
        question_ids = json.loads(request.POST.get('ids'))

        moment = Moment.objects.get(pk=int(request.POST['moment_id']))
        print moment

        for question in question_ids:
            q = Question.objects.get(pk=int(question['question_id']))
            attribute = Attributes.objects.get(pk=1)

            print question

            try:
                relation = Question_Attributes.objects.get(question_id=q)
            except Question_Attributes.DoesNotExist:
                relation = Question_Attributes()

            relation.moment_id = moment
            relation.question_id = q
            relation.weight = 10
            relation.save()

        json_response = json.dumps(
            {
                'success': True
            }
        )
        return HttpResponse(json_response, content_type="application/json")

def associate_questions_to_attributes(request):

    if request.is_ajax():
        question = Question.objects.get(pk=int(request.POST['question_id']))

        attribute = Attributes.objects.get(pk=int(request.POST['attribute_id']))

        try:
            question_attribute = Question_Attributes.objects.get(question_id=question)
        except Question_Attributes.DoesNotExist:
            question_attribute = Question_Attributes()

        question_attribute.question_id = question
        question_attribute.attribute_id = attribute
        question_attribute.weight = 10
        question_attribute.save()

        print question_attribute

        json_response = json.dumps(
            {
                'success': True
            }
        )

        return HttpResponse(json_response, content_type="application/json")

#Questions Section


def create_matrix(request, data):
    type = int(data.type)
    title = data.title
    cols = data.cols
    rows = data.rows
    survey_id = int(data.survey_id)
    add_catalog = data.add_catalog

    if add_catalog:
        catalog_question = Question()
        catalog_question.user = Xindex_User.objects.get(pk=request.user.id)
        catalog_question.type = Question_Type.objects.get(pk=type)
        catalog_question.title = title
        catalog_question.save()

        catalog = Catalog()
        catalog.user = Xindex_User.objects.get(pk=request.user.id)
        catalog.question = catalog_question

        catalog.save()

        for subquestion in rows:
            q = Question(user=Xindex_User.objects.get(pk=1),
                         title=subquestion.label,
                         type=Question_Type.objects.get(pk=type),
                         parent_question=catalog_question)
            q.save()

            catalog_child = Catalog()
            catalog_child.user = Xindex_User.objects.get(pk=request.user.id)
            catalog_child.question = q
            catalog_child.save()

            i = 1
            for option in cols:
                new_option = Option(question=q, label=option.label,
                                value = i, order = i)
                new_option.save()
                i += 1

        catalog = Catalog()
        catalog.user = Xindex_User.objects.get(pk=request.user.id)
        catalog.question = catalog_question

        catalog.save()

    question = Question()
    question.user = Xindex_User.objects.get(pk=request.user.id)
    question.type = Question_Type.objects.get(pk=type)
    question.title = title
    question.save()

    createAssociationQAM(question, data.moment_id, data.attribute_id)

    for subquestion in rows:
        q = Question(user=Xindex_User.objects.get(pk=1),
                     title=subquestion.label,
                     type=Question_Type.objects.get(pk=type),
                     parent_question=question)
        q.save()
        i = 1
        for option in cols:
            new_option = Option(question=q, label=option.label,
                            value = i, order = i)
            new_option.save()
            i += 1


    try:
        survey = Survey.objects.get(pk=survey_id)
    except Survey.DoesNotExist:
        survey = False

    if survey:
        survey.questions.add(question)

    json_response = json.dumps(
        {
            'question_added': True,
            'question_id': question.id
        }
    )

    return HttpResponse(json_response, content_type="application/json")


def create_multiple_choice(request, data):
    print data
    type = int(data.type)
    title = data.title
    options = data.options
    survey_id = int(data.survey_id)
    add_catalog = data.add_catalog

    if add_catalog:
        catalog_question = Question()
        catalog_question.user = Xindex_User.objects.get(pk=request.user.id)
        catalog_question.type = Question_Type.objects.get(pk=type)
        catalog_question.title = title
        catalog_question.save()

        i = 1
        for option in options:
            new_option = Option(question=catalog_question, label=option.label,
                            value = i, order = i)
            new_option.save()
            i += 1

            print new_option

        catalog = Catalog()
        catalog.user = Xindex_User.objects.get(pk=request.user.id)
        catalog.question = catalog_question

        catalog.save()

        print catalog



    question = Question()
    question.user = Xindex_User.objects.get(pk=request.user.id)
    question.type = Question_Type.objects.get(pk=type)
    question.title = title
    question.save()

    createAssociationQAM(question, data.moment_id, data.attribute_id)

    try:
        survey = Survey.objects.get(pk=survey_id)
    except Survey.DoesNotExist:
        survey = False

    if survey:
        survey.questions.add(question)

    '''type = int(request.POST["type"])
    title = request.POST["title"]
    options = request.POST.getlist('options')'''

    i = 1
    for option in options:
        new_option = Option(question=question, label=option.label,
                        value = i, order = i)
        new_option.save()
        i += 1

    json_response = json.dumps(
        {
            'question_added': True,
            'question_id': question.id
        }
    )
    return HttpResponse(json_response, content_type="application/json")


def create_open_question(request, data):
    type = int(data.type)
    title = data.title
    survey_id = int(data.survey_id)
    add_catalog = data.add_catalog

    if add_catalog:
        catalog_question = Question()
        catalog_question.user = Xindex_User.objects.get(pk=request.user.id)
        catalog_question.type = Question_Type.objects.get(pk=type)
        catalog_question.title = title
        catalog_question.save()

        catalog = Catalog()
        catalog.user = Xindex_User.objects.get(pk=request.user.id)
        catalog.question = catalog_question

        catalog.save()

    question = Question()
    question.user = Xindex_User.objects.get(pk=request.user.id)
    question.type = Question_Type.objects.get(pk=type)
    question.title = title
    question.save()

    createAssociationQAM(question, data.moment_id, data.attribute_id)

    try:
        survey = Survey.objects.get(pk=survey_id)
    except Survey.DoesNotExist:
        survey = False

    if survey:
        survey.questions.add(question)

    json_response = json.dumps(
        {
            'question_added': True,
            'question_id': question.id
        }
    )
    return HttpResponse(json_response, content_type="application/json")


def create_range_question(request, data):
    print "Entra a funciona crear pregunta de rango"

    type = int(data.type)
    title = data.title
    start_number = int(float(data.options.start_number))
    end_number = int(float(data.options.end_number))
    survey_id = int(data.survey_id)
    add_catalog = data.add_catalog

    if start_number < 0 or end_number > 20:
        json_response = json.dumps(
                    {'messagesent' : "Error - Limits are not valid for range"}
            )
        return HttpResponse(json_response, content_type="application/json",
                            status=400)


    if add_catalog:
        catalog_question = Question()
        catalog_question.user = Xindex_User.objects.get(pk=request.user.id)
        catalog_question.type = Question_Type.objects.get(pk=type)
        catalog_question.title = title
        catalog_question.save()

        new_option = Option(question=catalog_question, label=data.options.start_label,
                        value = start_number, order = start_number)
        new_option.save()

        start_number += 1

        for i in range(start_number, end_number):
            new_option = Option(question=catalog_question, label="",
                        value = i, order = i)
            new_option.save()

        new_option = Option(question=catalog_question, label=data.options.end_label,
                            value = end_number, order = end_number)
        new_option.save()

        catalog = Catalog()
        catalog.user = Xindex_User.objects.get(pk=request.user.id)
        catalog.question = catalog_question

        catalog.save()

    question = Question()
    question.user = Xindex_User.objects.get(pk=request.user.id)
    question.type = Question_Type.objects.get(pk=type)
    question.title = title
    question.save()

    createAssociationQAM(question, data.moment_id, data.attribute_id)

    new_option = Option(question=question, label=data.options.start_label,
                        value = start_number, order = start_number)
    new_option.save()

    start_number += 1

    for i in range(start_number, end_number):
        new_option = Option(question=question, label="",
                    value = i, order = i)
        new_option.save()

    new_option = Option(question=question, label=data.options.end_label,
                        value = end_number, order = end_number)
    new_option.save()


    try:
        survey = Survey.objects.get(pk=survey_id)
    except Survey.DoesNotExist:
        survey = False

    if survey:
        survey.questions.add(question)

    json_response = json.dumps(
        {
            'question_added' : True,
            'question_id': question.id
        }
    )
    return HttpResponse(json_response, content_type="application/json")


def create_true_and_false(request, data):
    type = int(data.type)
    title = data.title
    options = ['False', 'True']
    survey_id = int(data.survey_id)
    add_catalog = data.add_catalog

    if add_catalog:
        catalog_question = Question()
        catalog_question.user = Xindex_User.objects.get(pk=request.user.id)
        catalog_question.type = Question_Type.objects.get(pk=type)
        catalog_question.title = title
        catalog_question.save()

        for i in range(len(options)):
            new_option = Option(question=catalog_question, label=options[i],
                                value=i + 1, order=i + 1)
            new_option.save()

        catalog = Catalog()
        catalog.user = Xindex_User.objects.get(pk=request.user.id)
        catalog.question = catalog_question

        catalog.save()

    question = Question()
    question.user = Xindex_User.objects.get(pk=request.user.id)
    question.type = Question_Type.objects.get(pk=type)
    question.title = title
    question.save()

    createAssociationQAM(question, data.moment_id, data.attribute_id)

    try:
        survey = Survey.objects.get(pk=survey_id)
    except Survey.DoesNotExist:
        survey = False

    if survey:
        survey.questions.add(question)


    for i in range(len(options)):
        new_option = Option(question=question, label=options[i],
                            value=i + 1, order=i + 1)
        new_option.save()

    json_response = json.dumps(
        {
            'question_added' : True,
            'question_id': question.id
        }
    )
    return HttpResponse(json_response, content_type="application/json")

#TODO: Fix this; DO NOT use in production
@csrf_exempt
def add_ajax(request):
    if request.is_ajax():
        try:
            data = json.loads(request.body,
                              object_hook=lambda d: namedtuple('X', d.keys())
                                  (*d.values())
            )
            #TODO: Search for types in the table question_type to avoid hardcoding
            if data.type_name == "matrix":
                return create_matrix(request, data)
            elif data.type_name == "multiple_choice":
                print(data)
                return create_multiple_choice(request, data)
            elif data.type_name == "open_question":
                return create_open_question(request, data)
            elif data.type_name == "range":
                return create_range_question(request, data)
            elif data.type_name == "true_and_false":
                return create_true_and_false(request, data)

            #If the type of question is not defined, throw an error
            json_response = json.dumps(
                    {'messagesent' : "Error - Not a valid type of question"}
            )
            return HttpResponse(json_response,
                                content_type="application/json",
                                status=400)
        except ValueError:
            json_response = json.dumps(
                    {'messagesent': "Error - Invalid json"}
            )
            return HttpResponse(json_response,
                                content_type="application/json",
                                status=400)
    else:
        raise Http404


def deployment(request, action, next_step, survey_id=False):
    survey_id = int(survey_id)
    survey = Survey.objects.get(pk=survey_id)
    xindex_user = Xindex_User.objects.get(user__id=request.user.id)
    try:
        company = Company.objects.get(staff=xindex_user)

    except:
        company = False

    if company:
        company_name = company.name
        company_address = company.address
        company_email = 'atencion@hollidayinn.com'
        company_phone = company.phone
    else:
        company_name = 'Default company NAME'
        company_address = 'Default company ADDRESS'
        company_email = 'Default company EMAIL'
        company_phone = 'Default company PHONE'

    if int(next_step) == 2 and action == 'next':
        survey.step = 2
        survey.save()

        template_vars = {
            'survey_title': survey.name,
            'survey_id': survey.id,
            'next_step': str(int(next_step) + 1)
        }
        request_context = RequestContext(request, template_vars)
        return render_to_response('surveys/add-step-2.html',
                                  request_context)

    question_types = Question_Type.objects.all().order_by('name')
    if int(next_step) == 4 and action == 'next':

        configuration = json.loads(survey.configuration)

        setup = {}

        setup['blocks'] = []

        setup['moments'] = []

        user = Xindex_User.objects.get(pk=request.user.id)

        for company in user.company_set.all():
            for subsidiary in company.subsidiary_set.all():
                for business_unit in subsidiary.businessunit_set.all():
                    for service in business_unit.service.all():
                        for moment in service.moments.all():
                            setup['moments'].append(
                                {
                                    'moment': moment
                                }
                            )

        #print simplejson.dumps(configuration)
        for key, values in configuration.items():
            for block in values:
                questions = []
                for q in block['questions']:
                    print 'verificando q exista el campo'
                    if 'db_id' in q:

                        try:
                            question = Question.objects.get(pk=q['db_id'])
                            options = question.option_set.all().order_by('id')
                            options_o = []
                            for option in options:
                                options_o.append(
                                    {
                                        'id_option': option.id,
                                        'text': option.label,
                                        'option': option
                                    }
                                )
                            questions.append(
                                {
                                    'question': question,
                                    'survey_question_id': q[
                                        'question_survey_id'],
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
                setup['blocks'].append(
                    {
                        'block_id': block['block_id'],
                        'block_default_class': block['class_default'],
                        'block_description': block_description,
                        'questions': questions
                    }
                )

        for block in setup['blocks']:
            print block

        template_vars = {
            'survey_title': survey.name,
            'survey_id': survey.id,
            'next_step': str(int(next_step) + 1),
            'question_types': question_types,
            'company_name': company_name,
            'company_address': company_address,
            'company_email': company_email,
            'company_phone': company_phone,
            'setup': setup
        }
        request_context = RequestContext(request, template_vars)
        return render_to_response('surveys/deployment.html',
                                  request_context)


def edit(request, question_id):
    if request.is_ajax:
        question_types = Question_Type.objects.all().order_by('name')
        question = get_object_or_404(Question, pk=question_id)

        #TODO: Refactor using the factory
        if question.type.name == "Matrix":
            #We get the pattern of the options based on the first child
            rows = Question.objects.filter(parent_question=question).order_by('id')
            options = rows[0].option_set.all().order_by('id')
            return render_to_response('questions/edit.html',
                                      {'question': question,
                                       'question_types': question_types,
                                       'rows': rows,
                                       'options': options})
        elif question.type.name == "Multiple Choice":
            options = question.option_set.all().order_by('id')
            """
            return render_to_response('questions/edit.html',
                                      {'question': question,
                                       'question_types': question_types,
                                       'options': options})
            """
            question_json = {}
            question_json['question_type_id'] = question.type.id
            question_json['question_type_name'] = question.type.name
            question_json['question_title'] = question.title
            question_json['question_options'] = []
            question_json['question_types'] = []

            #Get Question Association
            try:
                question_association = Question_Attributes.objects.get(question_id__id=question_id)
                if question_association.moment_id is None:
                    moment_id = False
                    moment_name = False
                else:
                    moment_id = question_association.moment_id.id
                    moment_name = question_association.moment_id.name
                if question_association.attribute_id is None:
                    attribute_id = False
                    attribute_name = False
                else:
                    attribute_id = question_association.attribute_id.id
                    attribute_name = question_association.attribute_id.name

            except Question_Attributes.DoesNotExist:
                moment_id = False
                moment_name = False
                attribute_id = False
                attribute_name = False

            question_json['question_moment_id'] = moment_id
            question_json['question_moment_name'] = moment_name
            question_json['question_attribute_id'] = attribute_id
            question_json['question_attribute_name'] = attribute_name



            for option in options:
                if option.active:
                    question_json['question_options'].append(
                        {
                            'option_id': option.id,
                            'option_label': option.label
                        }
                    )
            for question_type in question_types:
                question_json['question_types'].append(
                    {
                        'question_type_id': question_type.id,
                        'question_type_name': question_type.name
                    }
                )


            return HttpResponse(json.dumps(question_json),
                                    content_type="application/json")

        elif question.type.name == "Open question" or question.type.name == "True and False":
            return render_to_response('questions/edit.html',
                                      {'question': question,
                                       'question_types': question_types})
        elif question.type.name == "Range":
            options = question.option_set.filter(active=True).order_by('id')
            first, last = options[0], options.reverse()[0]
            return render_to_response('questions/edit.html',
                                      {'question': question,
                                       'question_types': question_types,
                                       'options': options,
                                       'first': first,
                                       'last': last})

        #If question has an undefined type (weird) return nothing
        return render_to_response('questions/edit.html',
                                  {'question': question,
                                   'question_types': question_types})


def update_matrix(question, data):
    cols = data.cols
    rows = data.rows

    questions = Question.objects.filter(parent_question=question).order_by('id')

    #Set all subquestions to innactive
    Question.objects.filter(parent_question=question).update(active=False)
    #as well as the options for each question
    for q in questions:
        #Set all options for this question as innactive
        q.option_set.all().update(active=False)

    #Assuming the order in data is correct
    for subquestion in rows:
        if hasattr(subquestion, 'id'):
            q = questions.get(pk=subquestion.id)
            q.title = subquestion.label
            q.active = True
            q.save()

            options = q.option_set.all().order_by('id')
            #assuming both objects are in order
            i = 0
            for option in cols:
                try:
                    opt = options[i]
                    if opt:
                        opt.label = option.label
                        opt.active = True
                        opt.save()
                    i += 1
                except IndexError:
                    #It is a new Option
                    new_option = Option(question=q, label=option.label,
                            value = i, order = i)
                    new_option.save()
        else:
            #The subquestion is new
            q = Question(user=Xindex_User.objects.get(pk=1),
                         title=subquestion.label,
                         type=Question_Type.objects.get(pk=question.type.id),
                         parent_question=question)
            q.save()

            #There must be at leat one
            cols = questions[0].option_set.all().order_by('id')
            for option in cols:
                new_option = Option(question=q, label=option.label,
                                    value=option.value, order=option.order)
                new_option.save()

        #At the end, for each question that has been 'removed' (active = False)
        #We should also delete its options
        deleted_questions = Question.objects.filter(parent_question=question,
                                                    active=False)
        for d_question in deleted_questions:
            d_question.option_set.all().update(active=False)


    json_response = json.dumps(
        {'messagesent': "Question edited successfully!"}
    )
    return HttpResponse(json_response, content_type="application/json")

def update_multiple_choice(question, data):
    options = data.options

    #Set all options to innactive
    Option.objects.filter(question=question).update(active=False)
    current_options = question.option_set.all().order_by('id');

    #Assuming the order in data is correct
    i = 0
    for option in options:
        if hasattr(option, 'id'):
            opt = current_options.get(pk=option.id)
            opt.label = option.label
            opt.active = True
            opt.save()
            i += 1

        else:
            #It is a new Option
            new_option = Option(question=question, label=option.label,
                    value = i, order = i)
            new_option.save()

    if data.moment_id or data.attribute_id:
        try:
            q_a_m = Question_Attributes.objects.get(question_id=question)
        except Question_Attributes.DoesNotExist:
            q_a_m = Question_Attributes()
            q_a_m.question_id = question

        print q_a_m

        if data.moment_id:
            q_a_m.moment_id = Moment.objects.get(pk=data.moment_id)
        else:
            q_a_m.moment_id = None



        if data.attribute_id:
            q_a_m.attribute_id = Attributes.objects.get(pk=data.attribute_id)
        else:
            q_a_m.attribute_id = None

        q_a_m.weight = 10

        q_a_m.save()

    if not data.moment_id and not data.attribute_id:
        try:
            q_a_m = Question_Attributes.objects.get(question_id=question)
            q_a_m.delete()
        except Question_Attributes.DoesNotExist:
            q_a_m = None

    json_response = json.dumps(
        {
            'updated': True
        }
    )
    return HttpResponse(json_response, content_type="application/json")

def update_open_question(question, data):
    question.title = data.title
    question.save()
    json_response = json.dumps(
        {'messagesent': "Question edited successfully!"}
    )
    return HttpResponse(json_response, content_type="application/json")
def update_range_question(question, data):
    start_number = int(float(data.options.start_number))
    end_number = int(float(data.options.end_number))

    if start_number < 0 or end_number > 20:
        json_response = json.dumps(
                    {'messagesent': "Error - Limits are not valid for range"}
            )
        return HttpResponse(json_response, content_type="application/json",
                            status=400)

    #Set all options to innactive
    Option.objects.filter(question=question).update(active=False)
    current_options = question.option_set.all().order_by('id')

    #Setting the first value
    first_option = current_options[start_number]
    first_option.label = data.options.start_label
    first_option.value = start_number
    first_option.order = start_number
    first_option.active = True
    first_option.save()

    #Assuming the order in data is correct
    start_number += 1
    for i in range(start_number, end_number):
        try:
            updated_option = current_options[i]
            updated_option.label = ''
            updated_option.value = i
            updated_option.order = i
            updated_option.active = True
            updated_option.save()
        except IndexError:
            #It is a new Option
            new_option = Option(question=question, label="",
                                value=i, order=i)
            new_option.save()

    #Setting the last value
    try:
        #It's already within the limit
        lastOption = current_options[end_number]
        lastOption.label = data.options.end_label
        lastOption.value = end_number
        lastOption.order = end_number
        lastOption.active = True
        lastOption.save()
    except IndexError:
        #Needs to be created
        lastOption = Option(question=question, label=data.options.end_label,
                            value=end_number, order=end_number)
        lastOption.save()


    json_response = json.dumps(
        {'messagesent': "Question edited successfully!"}
    )
    return HttpResponse(json_response, content_type="application/json")
def update_true_and_false(question, data):
    question.title = data.title
    question.save()
    json_response = json.dumps(
        {'messagesent': "Question edited successfully!"}
    )
    return HttpResponse(json_response, content_type="application/json")






#TODO: Fix this; DO NOT use in production
@csrf_exempt
def edit_ajax(request, question_id):
    if request.is_ajax():
        try:
            data = json.loads(request.body,
                              object_hook=lambda d: namedtuple('X', d.keys())
                                  (*d.values())
            )

            print data

            q_id = int(question_id)
            question = Question.objects.get(pk=q_id)
            question.title = data.title
            question.save()

            #TODO: Search for types in the table question_type to avoid hardcoding
            if question.type.name == "Matrix":
                return update_matrix(question, data)
            elif question.type.name == "Multiple Choice":
                print 'entra al metodo'
                return update_multiple_choice(question, data)
            elif question.type.name == "Open question":
                return update_open_question(question, data)
            elif question.type.name == "Range":
                return update_range_question(question, data)
            elif question.type.name == "True and False":
                return update_true_and_false(question, data)

            #If the type of question is not defined, throw an error
            json_response = json.dumps(
                    {'messagesent': "Error - Not a valid type of question"}
            )
            return HttpResponse(json_response, content_type="application/json",
                                status=400)
        except ValueError:
            json_response = json.dumps(
                    {'messagesent': "Error - Invalid json"}
            )
            return HttpResponse(json_response, content_type="application/json",
                                status=400)
    else:
        raise Http404

def createAssociationQAM(question, moment_id, attribute_id):
    if moment_id or attribute_id:
        q_a_m = Question_Attributes()
        q_a_m.question_id = question

        if moment_id:
            q_a_m.moment_id = Moment.objects.get(pk=moment_id)
        else:
            q_a_m.moment_id = None

        if attribute_id:
            q_a_m.attribute_id = Attributes.objects.get(pk=attribute_id)
        else:
            q_a_m.attribute_id = None

        q_a_m.weight = 10

        q_a_m.save()
