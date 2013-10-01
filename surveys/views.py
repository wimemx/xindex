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
                "counter_attribute": counter_attributes
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
                "counter_attribute": counter_attributes
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
                step = int(next_step) - 1
                xindex_user = Xindex_User.objects.get(user__id=request.user.id)

                configuration = {'header_logo': '', 'body': '', 'footer': ''}
                configuration = simplejson.dumps(configuration)

                print configuration

                survey = Survey(user=xindex_user,
                                name=form.cleaned_data['name'], step=step, configuration=configuration)
                survey.save()

                print 'Se ha guardado'

                new_url = '/surveys/save/next/2/'+ str(survey.id)

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
        company = Company.objects.get(staff=xindex_user)

        print company.name
        if int(next_step) == 2 and action == 'next':
            template_vars = {
                'survey_title': survey.name,
                'survey_id': survey.id,
                'next_step': str(int(next_step)+1)
            }
            request_context = RequestContext(request, template_vars)
            return render_to_response('surveys/add-step-2.html',
                                      request_context)

        question_types = Question_Type.objects.all().order_by('name');

        if int(next_step) == 3 and action == 'next':
            configuration = json.loads(survey.configuration)

            setup = {}
            setup['blocks'] = []
            #print simplejson.dumps(configuration)
            for key, values in configuration.items():
                for block in values:
                    questions = []
                    for q in block['questions']:
                        question = Question.objects.get(pk=q['db_id'])
                        options = question.option_set.all().order_by('id')
                        options_o = []
                        for option in options:
                            options_o.append(
                                {
                                    'id_option': option.id,
                                    'text': option.label
                                }
                            )
                        questions.append(
                            {
                                'survey_question_id': q['question_survey_id'],
                                'db_question_id': q['db_id'],
                                'question_title': question.title,
                                'question_type': question.type.id,
                                'question_options': options_o
                            }
                        )
                    setup['blocks'].append(
                        {
                            'block_id': block['block_id'],
                            'block_description': block['block_description'],
                            'questions': questions
                        }
                    )


            print setup

            for block in setup['blocks']:
                print block


            template_vars = {
                'survey_title': survey.name,
                'survey_id': survey.id,
                'next_step': str(int(next_step)+1),
                'question_types': question_types,
                'company_name': company.name,
                'company_address': company.address,
                'company_email': 'atencion@hollidayinn.com',
                'company_phone': company.phone,
                'setup': setup
            }
            request_context = RequestContext(request, template_vars)
            return render_to_response('surveys/add-step-3.html',
                                      request_context)


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
def media_upload(request):
    path = os.path.join(
        os.path.dirname(__file__), '..',
        'templates/media/pictures/').replace('\\', '/')

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