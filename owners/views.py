from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.template.context import RequestContext
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.core.urlresolvers import reverse
from xindex.models import Owner
from xindex.forms import OwnerForm


@login_required(login_url='/signin/')
def index(request):
    owners = Owner.objects.all().order_by('-date')
    template_vars = {"title": "Owners",
                     "owners":owners}
    request_context = RequestContext(request, template_vars)
    return render(request, 'owners/index.html', request_context)


@login_required(login_url='/signin/')
def detail(request, owner_id):
    try:
        owner=Owner.objects.get(pk=owner_id)
    except Owner.DoesNotExist:
        raise Http404
    return render(request, 'owners/detail.html', {'owner':owner})


@login_required(login_url='/signin/')
def add(request):
    if request.method=='POST':
        form = OwnerForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/owners')
    else:
        form = OwnerForm()
        request_context = RequestContext(request)
    return render(request, "owners/add.html", {"formulario": form})


@login_required(login_url='/signin/')
def edit(request, owner_id):
    owner = Owner.objects.get(pk=owner_id)
    if request.method=="POST":
        form = OwnerForm(request.POST, instance=owner)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/owners')
    else:
        form = OwnerForm(instance=owner)

    return render(request, "owners/add.html", {"formulario":form})