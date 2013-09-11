from django.shortcuts import render, get_object_or_404
from django.template.context import RequestContext
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.core.urlresolvers import reverse
from xindex.models import Attribute
from xindex.forms import AttributeForm

def index(request):
    attributes = Attribute.objects.all().order_by('-date')
    template_vars = {"title": "Attributes",
                     "attributes": attributes}
    request_context = RequestContext(request, template_vars)
    return render(request, "attributes/index.html", request_context)

def detail(request, attribute_id):
    try:
        attribute=Attribute.objects.get(pk=attribute_id)
    except Attribute.DoesNotExist:
        raise Http404
    return render(request, 'attributes/detail.html', {"attribute":attribute})

def add(request):
    if request.method=='POST':
        form = AttributeForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/attributes')
    else:
        form = AttributeForm()
    return render(request, "attributes/add.html", {"formulario":form})

def edit(request, attribute_id):
    attribute = Attribute.objects.get(pk=attribute_id)
    if request.method == "POST":
        form = AttributeForm(request.POST, instance=attribute)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/attributes')
    else:
        form = AttributeForm(instance=attribute)
    return render(request, "attributes/add.html", {"formulario":form})