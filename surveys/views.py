from django.shortcuts import render, get_object_or_404, render_to_response
from django.template.context import RequestContext
from django.http import HttpResponse, Http404, HttpResponseRedirect
from xindex.models import Survey
from django.utils import simplejson


def index(request):
    surveys = Survey.objects.all().order_by('-date')
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