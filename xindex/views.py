# Create your views here.
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.template.context import RequestContext
import re
from django.db.models import Q
from models import Survey, Question_Attributes


def index(request):
    template_vars = {
        #vars
    }
    request_context = RequestContext(request, template_vars)
    return render_to_response("xindex/index.html", request_context)


def normalize_query(query_string,
                    findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
                    normspace=re.compile(r'\s{2,}').sub):
    ''' Splits the query string in invidual keywords, getting rid of unecessary spaces
        and grouping quoted words together.
        Example:

        >>> normalize_query('  some random  words "with   quotes  " and   spaces')
        ['some', 'random', 'words', 'with quotes', 'and', 'spaces']

    '''
    return [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)]


def get_query(query_string, search_fields):
    ''' Returns a query, that is a combination of Q objects. That combination
        aims to search keywords within a model by testing the given search fields.

    '''
    query = None # Query to search for every search term
    terms = normalize_query(query_string)
    for term in terms:
        or_query = None # Query to search for a given term in each field
        for field_name in search_fields:
            q = Q(**{"%s__icontains" % field_name: term})
            if or_query is None:
                or_query = q
            else:
                or_query = or_query | q
        if query is None:
            query = or_query
        else:
            query = query & or_query
    return query


def search(request):
    surveys = {'surveys': []}
    query_string = ''
    found_entries = None
    question_attribute_query = Question_Attributes.objects.all()

    if ('q' in request.GET) and request.GET['q'].strip():
        query_string = request.GET['q']

        entry_query = get_query(query_string, ['name',])

        found_entries = Survey.objects.filter(entry_query).order_by('name')

    for each_survey in found_entries:
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
                "status": each_survey.active,
                "counter_question": counter_question,
                "counter_attribute": counter_attributes
            }
        )
    template_vars = {"title": "Surveys",
                     "found_entries": surveys,
                     "order_name": "name",
                     "order_status": "status",
                     "order_date": "date",
                     "query_string": query_string}
    request_context = RequestContext(request, template_vars)
    return render_to_response('surveys/index.html', request_context)
    '''
    return render_to_response('surveys/index.html',
                              {'query_string': query_string,
                               'found_entries': found_entries},
                              context_instance=RequestContext(request))
                                  '''