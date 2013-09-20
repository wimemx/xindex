from django.shortcuts import render, get_object_or_404, render_to_response
from django.template.context import RequestContext
from django.http import HttpResponse, Http404, HttpResponseRedirect
from xindex.models import Survey, Question_Attributes
from django.utils import simplejson


def index(request):
    surveys = {'surveys': []}
    survey_query = Survey.objects.all().order_by('-date')
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
                "name": each_survey.name,
                "date": each_survey.date,
                "counter_question": counter_question,
                "counter_attribute": counter_attributes
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
