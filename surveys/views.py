from django.shortcuts import render, get_object_or_404, render_to_response
from django.template.context import RequestContext
from django.http import HttpResponse, Http404, HttpResponseRedirect
from xindex.models import Survey
from django.utils import simplejson

def getJson(request):
    survey = {'surveys': []}
    survey_query = Survey.objects.filter(active=True).order_by('-date')

    for each_survey in survey_query:
        survey['attributes'].append(
            {
                "name": each_survey.name,
                "description": each_survey.description,
                "threshold": each_survey.threshold,
                "attribute_id": each_survey.id
            }
        )
    return HttpResponse(simplejson.dumps(survey))