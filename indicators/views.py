from django.shortcuts import render, get_object_or_404, render_to_response
from django.template.context import RequestContext
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.core.urlresolvers import reverse
from xindex.models import Attributes, Question
from xindex.forms import AttributesForm
from django.utils import simplejson
from xindex.models import Moment

def index(request):
    indicators = Attributes.objects.all().order_by('-date')
    template_vars = {"title": "Indicators",
                     "indicators": indicators}
    request_context = RequestContext(request, template_vars)
    return render(request, 'indicators/index.html', request_context)


def add(request):
    if request.POST:
        formulario = AttributesForm(request.POST or None)
        if formulario.is_valid():

            attribute_saved = formulario.save()

            moments = request.POST.getlist('moments')

            for moment in moments:
                try:
                    m = Moment.objects.get(id=moment)
                    m.attributes.add(attribute_saved)
                except Moment.DoesNotExist:
                    m = False

            return HttpResponse('Si')
        else:
            return HttpResponse('No')
    else:
        formulario = AttributesForm()
        template_vars = {
            "titulo": "Add attribute",
            "message": "",
            "formulario": formulario
        }
        request_context = RequestContext(request, template_vars)
        return render_to_response("indicators/add.html", request_context)


def update(request, indicator_id):
    attribute = Attributes.objects.get(pk=indicator_id)

    if request.POST:
        form = AttributesForm(request.POST, instance=attribute)
        if form.is_valid():
            print("formulario valido")
            attribute_modified = form.save()

            moments_asociated = request.POST.getlist('moments')

            ma_a = []

            for ma in moments_asociated:
                momen = Moment.objects.get(id=ma)
                momen.attributes.add(attribute_modified)
                ma_a.append(ma)

            moments_no_asociated = Moment.objects.exclude(id__in=ma_a)

            for mna in moments_no_asociated:
                m = Moment.objects.get(id=mna.id)
                m.attributes.remove(attribute_modified)

            #moments_no_asociated = Moment.objects.exclude(id=moments_asociated)
            """
            for moment in moments:
                try:
                    m = Moment.objects.get(id=moment)
                    m.attributes.add(attribute_saved)
                except Moment.DoesNotExist:
                    m = False
            """


            #return HttpResponse("el momento de ha editado")
            return HttpResponse('Si')
    else:
        print 'entro'
        momentos = Moment.objects.filter(attributes__id=attribute.id)
        print momentos
        form = AttributesForm(instance=attribute, initial={'moments': momentos})
        template_vars = {
            "formulario": form,
            "attribute_id": indicator_id}
        request_context = RequestContext(request, template_vars)
        return render(request, "indicators/edit.html", request_context)


def remove(request, indicator_id):
    try:
        attribute = Attributes.objects.get(id=indicator_id)
    except Attributes.DoesNotExist:
        attribute = False

    if attribute:
        try:
            attribute.active = False
            attribute.save()
            message = "Deleted attribute"
            template_vars = {
                "titulo": "Attributes",
                "message": message
            }
            request_context = RequestContext(request, template_vars)
            #return render_to_response("services/index.html", request_context)
            return HttpResponse('Si')

        except:
            message = "Cant delete"
            template_vars = {
                "titulo": "Attributes",
                "message": message
            }
            request_context = RequestContext(request, template_vars)
            #return render_to_response("services/index.html", request_context)
            return HttpResponse('No')
    else:
        message = "Problem to find this service"
        template_vars = {
            "titulo": "Attribute",
            "message": message
        }
        request_context = RequestContext(request, template_vars)
        #return render_to_response("services/index.html", request_context)
        return HttpResponseRedirect('/indicators/')


def details(request, indicator_id):
    try:
        attribute_details = Attributes.objects.get(pk=indicator_id)
        #status = str(attribute_details.active)
    except Attributes.DoesNotExist:
        raise Http404

    template_vars = {
        'titulo': 'Attribute Details',
        'attribute_details': attribute_details
    }
    request_context = RequestContext(request, template_vars)
    return render_to_response('indicators/details.html', request_context)


def getSInJson(request):
    attributes = {'attributes': []}
    attribute_query = Attributes.objects.filter(active=True).order_by('-date')
    question_attribute_query = [1]
        #Question_Attributes.objects.filter(active=True)

    for each_attribute in attribute_query:

        attributes['attributes'].append(
            {
                "name": each_attribute.name,
                "description": each_attribute.description,
                #"type": each_attribute.type,
                #"min_value": each_attribute.min_value,
                #"max_value": each_attribute.max_value,
                "threshold": each_attribute.threshold,
                #"weight": each_attribute.weight,
                #"questions": counter_question,
                "attribute_id": each_attribute.id
            }
        )
    return HttpResponse(simplejson.dumps(attributes))