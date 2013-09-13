from django.shortcuts import render, get_object_or_404
from django.template.context import RequestContext
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.core.urlresolvers import reverse
from xindex.models import Moment
from xindex.forms import MomentForm
from xindex.models import Service

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

def add(request, service_id):
    print("Entrando al metodo")
    if request.method=='POST':
        print "Si se envio por post"
        form = MomentForm(request.POST)
        if form.is_valid():
            id_return = form.save()
            print id_return.id
            service = Service.objects.get(id=service_id)
            service.moments.add(id_return)
            return HttpResponse("El Momento de contacto se ha dado de alta!")
            #return HttpResponseRedirect('/moments')
        else:
            return HttpResponse("Verifique los campos y vuelva a intentar!")
    else:
        form = MomentForm()
        return render(request, "moments/add.html", {"formulario": form,
                                                    "service_id": service_id})

    #request_context = RequestContext(request)

    #return render(request, "moments/add.html", {"formulario": form})

def edit(request, moment_id):
    print("Entrando edit")
    moment = Moment.objects.get(pk=moment_id)
    if request.method=='POST':
        print("POST")
        form = MomentForm(request.POST, instance=moment)
        if form.is_valid():
            print("formulario valido")
            form.save()
            #return HttpResponse("el momento de ha editado")
            return HttpResponseRedirect('/services/')
    else:
        form = MomentForm(instance=moment)

    return render(request, "moments/edit.html", {"formulario": form,
                                                 "moment_id": moment_id})


def remove(request, service_id, moment_id):
    moment = Moment.objects.get(pk=moment_id)
    service = Service.objects.get(pk=service_id)
    service.moments.remove(moment)
    service.save()
    return HttpResponseRedirect("/services/details/"+service_id)