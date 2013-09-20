from django.shortcuts import render, get_object_or_404, render_to_response
from django.template.context import RequestContext
from django.http import HttpResponse, Http404, HttpResponseRedirect
from xindex.models import Survey
from django.utils import simplejson


def index(request):
    surveys = {'surveys': []}
    survey_query = Survey.objects.all().order_by('-date')

    for each_survey in survey_query:
        counter_question = 0
        for each_question in each_survey.questions.all():
            counter_question += 1

        surveys['surveys'].append(
            {
                "name": each_survey.name,
                "date": each_survey.date,
                "counter": counter_question
            }
        )
    template_vars = {"title": "Surveys",
                     "surveys": surveys}
    request_context = RequestContext(request, template_vars)
    return render(request, 'surveys/index.html', request_context)


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
    template_vars = {
        'title': 'Agregar Encuesta'
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
            return render_to_response('surveys/add-step-1.html');

    else:
        return HttpResponseRedirect('/surveys/add')

