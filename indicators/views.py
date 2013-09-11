from django.shortcuts import render, get_object_or_404
from django.template.context import RequestContext
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.core.urlresolvers import reverse
from xindex.models import Indicator
from xindex.forms import IndicatorForm

def index(request):
    indicators = Indicator.objects.all().order_by('-date')
    template_vars = {"title": "Indicators",
                     "indicators":indicators}
    request_context = RequestContext(request, template_vars)
    return render(request, 'indicators/index.html', request_context)

def detail(request, indicator_id):
    try:
        indicator=Indicator.objects.get(pk=indicator_id)
    except Indicator.DoesNotExist:
        raise Http404
    return render(request, 'indicators/detail.html', {'owner':indicator})

def add(request):
    if request.method=='POST':
        form = IndicatorForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/indicators')
    else:
        form = IndicatorForm()
        request_context = RequestContext(request)
    return render(request, "indicators/add.html", {"formulario": form})

def edit(request, indicator_id):
    indicator = Indicator.objects.get(pk=indicator_id)
    if request.method=="POST":
        form = IndicatorForm(request.POST, instance=indicator)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/indicators')
    else:
        form = IndicatorForm(instance=indicator)
    return render(request, "indicators/add.html",{"formulario": form})
