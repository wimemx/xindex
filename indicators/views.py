from django.shortcuts import render, get_object_or_404
from django.template.context import RequestContext
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.core.urlresolvers import reverse
from xindex.models import Attributes
from xindex.forms import AttributesForm

def index(request):
    indicators = Attributes.objects.all().order_by('-date')
    template_vars = {"title": "Indicators",
                     "indicators":indicators}
    request_context = RequestContext(request, template_vars)
    return render(request, 'indicators/index.html', request_context)

def detail(request, indicator_id):
    try:
        indicator=Attributes.objects.get(pk=indicator_id)
    except Attributes.DoesNotExist:
        raise Http404
    return render(request, 'indicators/detail.html', {'owner':indicator})

def add(request):
    if request.method=='POST':
        form = AttributesForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/indicators')
    else:
        form = AttributesForm()
        request_context = RequestContext(request)
    return render(request, "indicators/add.html", {"formulario": form})

def edit(request, indicator_id):
    indicator = Attributes.objects.get(pk=indicator_id)
    if request.method=="POST":
        form = AttributesForm(request.POST, instance=indicator)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/indicators')
    else:
        form = AttributesForm(instance=indicator)
    return render(request, "indicators/add.html",{"formulario": form})
