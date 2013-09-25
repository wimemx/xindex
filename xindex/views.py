# Create your views here.
from django.contrib.auth import authenticate, login as login_auth, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.template.context import RequestContext
import re
from django.db.models import Q
from models import Survey, Question_Attributes

@login_required(login_url='/signin/')
def index(request):
    template_vars = {
        #vars
    }
    request_context = RequestContext(request, template_vars)
    return render_to_response("xindex/index.html", request_context)


def signin(request):
    template_vars = {
        #vars
    }
    request_context = RequestContext(request, template_vars)
    return render_to_response("access/signin.html", request_context)


def signup(request):
    template_vars = {
        #vars
    }
    request_context = RequestContext(request, template_vars)
    return render_to_response("access/signup.html", request_context)


def login(request):
    error = username = password = ''
    #Si ya esta logeado el usuario, lo redirigimos a nuestra pagina de inicio
    if request.user.is_authenticated():
        return HttpResponseRedirect("/xindex/")
    #recibimos el post del formulario
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                #loggeamos al usuario y lo redirigimos a la pagina de inicio
                login_auth(request, user)
                return HttpResponseRedirect("/xindex/")
            else:
                error = "Tu cuenta ha sido desactivada, por favor ponte en " \
                        "contacto con tu administrador"
                return HttpResponseRedirect("/signin/")
        else:
            error = "Tu nombre de usuario o contrase&ntilde;a son incorrectos."
    variables = dict(username=username, password=password, error=error)
    variables_template = RequestContext(request, variables)
    return render_to_response("access/signin.html", variables_template)


@login_required(login_url='/signin/')
def log_out(request):
    logout(request)
    return HttpResponseRedirect('/signin/')


def normalize_query(query_string,
                    findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
                    normspace=re.compile(r'\s{2,}').sub):

    return [normspace(' ',
                      (t[0] or t[1]).strip()) for t in findterms(query_string)]


def get_query(query_string, search_fields):
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

    query_string = request.GET['q']

    if query_string == '':
        found_entries = Survey.objects.all().order_by('name')

    else:
        if ('q' in request.GET) and request.GET['q'].strip():
            entry_query = get_query(query_string, ['name', ])
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