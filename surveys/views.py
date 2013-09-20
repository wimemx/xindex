from django.shortcuts import render, get_object_or_404, render_to_response
from django.template.context import RequestContext
from django.http import HttpResponse, Http404, HttpResponseRedirect
from xindex.models import Survey, Question_Attributes
from django.utils import simplejson
from xindex.forms import SurveyForm


def index(request):
    surveys = {'surveys': []}
    survey_query = Survey.objects.all().order_by('-active')
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
                "status": each_survey.active,
                "counter_question": counter_question,
                "counter_attribute": counter_attributes
            }
        )
    template_vars = {"title": "Surveys",
                     "surveys": surveys,
                     "order_name": "name",
                     "order_status": "status",
                     "order_date": "date"}
    request_context = RequestContext(request, template_vars)
    return render(request, 'surveys/index.html', request_context)


def indexOrder(request, order_type):
    surveys = {'surveys': []}
    survey_query = Survey.objects.all().order_by(order_type)
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
                "status": each_survey.active,
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
            return render_to_response('surveys/add-step-1.html');

    else:
        return HttpResponseRedirect('/surveys/add')

def save(request, action, next_step, survey_id=False):

    if survey_id == 'empty':
        if request.POST:
            form = SurveyForm(request.POST)
            if form.is_valid():
                survey = form.save()
            else:
                print 'El formulario no es valido'

    #name = request.GET['survey-name']
    print request.POST
    return HttpResponse('response')

    template_vars = {
        'survey_title': ''
    }

