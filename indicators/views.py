from django.shortcuts import render, get_object_or_404, render_to_response
from django.template.context import RequestContext
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.core.urlresolvers import reverse
from xindex.models import Attributes
from xindex.forms import AttributesForm
from django.utils import simplejson


def index(request):
    indicators = Attributes.objects.all().order_by('-date')
    template_vars = {"title": "Indicators",
                     "indicators": indicators}
    request_context = RequestContext(request, template_vars)
    return render(request, 'indicators/index.html', request_context)


def add(request):
    if request.POST:
        formulario = AttributesForm(request.POST or None, request.FILES)
        if formulario.is_valid():
            formulario.save()
            template_vars = {
                "titulo": "Attribute",
                "message": "Added Attribute",
                "formulario": formulario
            }
            request_context = RequestContext(request, template_vars)
            #return render_to_response("services/index.html", request_context)
            return HttpResponseRedirect('/indicators/')
        else:
            template_vars = {
                "titulo": "Add attribute",
                "message": "",
                "formulario": formulario
            }
            request_context = RequestContext(request, template_vars)
            return render_to_response("indicators/add.html", request_context)
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
    try:
        attribute = Attributes.objects.get(pk=indicator_id)
    except Attributes.DoesNotExist:
        attribute = False

    if attribute:
        if request.POST:
            formulario = AttributesForm(request.POST or None, request.FILES,
                                        instance=attribute)
            if formulario.is_valid():
                formulario.save()
                template_vars = {
                    "titulo": "Attributes",
                    "message": "Attributes"
                }
                request_context = RequestContext(request, template_vars)
                return HttpResponseRedirect('/indicators/')
            else:
                template_vars = {
                    "titulo": "Edit attribute",
                    "message": "",
                    "formulario": formulario
                }
                request_context = RequestContext(request, template_vars)
                return render_to_response("indicators/update.html",
                                          request_context)
        else:
            formulario = AttributesForm(instance=attribute)
            template_vars = {
                "titulo": "Edit attribute",
                "message": "",
                "formulario": formulario
            }
            request_context = RequestContext(request, template_vars)
            return render_to_response("indicators/add.html", request_context)
    return HttpResponseRedirect('/indicators/')


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
            return HttpResponseRedirect('/indicators/')

        except:
            message = "Cant delete"
            template_vars = {
                "titulo": "Attributes",
                "message": message
            }
            request_context = RequestContext(request, template_vars)
            #return render_to_response("services/index.html", request_context)
            return HttpResponseRedirect('/indicators/')
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
    attribute = {'attributes': []}
    attribute_query = Attributes.objects.filter(active=True).order_by('-date')

    for each_attribute in attribute_query:

        counter_question = 0
        for each_question in each_attribute.questions.all():
            counter_question += 1

        attribute['attributes'].append(
            {
                "name": each_attribute.name,
                "description": each_attribute.description,
                #"type": each_attribute.type,
                "min_value": each_attribute.min_value,
                "max_value": each_attribute.max_value,
                "threshold": each_attribute.threshold,
                "weight": each_attribute.weight,
                "questions": counter_question,
                "attribute_id": each_attribute.id
            }
        )
    return HttpResponse(simplejson.dumps(attribute))