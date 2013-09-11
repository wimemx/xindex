from django.shortcuts import render, get_object_or_404
from django.template.context import RequestContext
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.core.urlresolvers import reverse
from xindex.models import Moment
from xindex.forms import MomentForm

def index(request):
    moments = Moment.objects.all().order_by('-date')
    template_vars = {"title": "Moments",
                     "moments": moments}
    request_context = RequestContext(request, template_vars)
    return render(request, 'moments/index.html', request_context)

def detail(request, moment_id):
    try:
        moment = Moment.objects.get(pk=moment_id)
    except Moment.DoesNotExist:
        raise Http404
    return render(request, 'moments/detail.html', {'moment': moment})

def add(request):
    if request.method=='POST':
        form = MomentForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/moments')
    else:
        form = MomentForm()

    request_context = RequestContext(request)
    return render(request, "moments/add.html", {"formulario": form})

def edit(request, moment_id):
    moment = Moment.objects.get(pk=moment_id)
    if request.method=='POST':
        form = MomentForm(request.POST, instance=moment)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/moments')
    else:
        form = MomentForm(instance=moment)

    return render(request, "moments/add.html", {"formulario": form})
