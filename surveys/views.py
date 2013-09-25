# -*- encoding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, render_to_response
from django.template.context import RequestContext
from django.http import HttpResponse, Http404, HttpResponseRedirect
from xindex.models import Survey, Question_Attributes
from django.utils import simplejson
from xindex.forms import SurveyForm
from xindex.models import Xindex_User


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
                survey = Survey(user=xindex_user,
                                name=form.cleaned_data['name'], step=step)
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
        print 'Next step: ' + next_step
        print 'Id survey: ' + survey_id
        survey_id = int(survey_id)
        survey = Survey.objects.get(pk=survey_id)
        if int(next_step) == 2 and action == 'next':
            template_vars = {
                'survey_title': survey.name,
                'survey_id': survey.id,
                'next_step': str(int(next_step)+1)
            }
            request_context = RequestContext(request, template_vars)
            return render_to_response('surveys/add-step-2.html',
                                      request_context)
        if int(next_step) == 3 and action == 'next':
            template_vars = {
                'survey_title': survey.name,
                'survey_id': survey.id,
                'next_step': str(int(next_step)+1)
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