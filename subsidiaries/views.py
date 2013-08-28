# Create your views here.
from django.shortcuts import render_to_response
from xindex.models import Subsidiary
from django.http import HttpResponseRedirect, HttpResponse
from subsidiaries.forms import SubsidiaryForm, UpdateForm
from django.template.context import RequestContext

def index(request, message = ''):
    print "Entrando a la vista"
    all_subsidiaries = Subsidiary.objects.all().order_by('-name')
    print all_subsidiaries
    return render_to_response('subsidiaries/index.html',
                              {
                                  'all_subsidiaries': all_subsidiaries,
                                  'message': message
                              })

def new(request):
    return render_to_response(
        'subsidiaries/new.html',
        {
            'action': 'add',
            'button': 'Agregar'
        }
    )

def add(request):
    if request.POST:
        formulario = SubsidiaryForm(request.POST or None)
        if formulario.is_valid():
            print "Formulario valido"
            formulario.save()

            template_vars = {
                "titulo": "Subsidiarias",
                "message": "Se ha dado de alta la subsidiaria",
                "formulario": formulario
            }
            request_context = RequestContext(request, template_vars)
            #return render_to_response("subsidiaries/index.html", request_context)
            return HttpResponseRedirect('/subsidiaries')
        else:
            return HttpResponse("El formulario no es valido %s.")
    else:
        formulario = SubsidiaryForm()
        template_vars = {
            "titulo": "Agregar subsidiaria",
            "message": "",
            "formulario": formulario
        }
        request_context = RequestContext(request, template_vars)
        return render_to_response("subsidiaries/add.html", request_context)


def edit(request, subsidiary_id):
    try:
        sub = Subsidiary.objects.get(id=subsidiary_id)
    except Subsidiary.DoesNotExist:
        sub = False

    print sub.name
    print sub.business_unit
    if sub:
        #formulario = UpdateForm(initial={'id': sub.id,'name': sub.name, 'business_unit': [1,2]})

        if request.POST:
            formulario = SubsidiaryForm(request.POST or None, instance=sub)
            if formulario.is_valid():
                formulario.save()
                template_vars = {
                    "titulo": "Subsidiarias",
                    "message": "Se ha modificado la subsidiaria"
                }
                request_context = RequestContext(request, template_vars)
                return HttpResponseRedirect('/subsidiaries/')
        else:
            formulario = SubsidiaryForm(request.POST or None, instance=sub)
            template_vars = {
                "titulo": "Editar subsidiaria",
                "message": "",
                "formulario": formulario
            }
            request_context = RequestContext(request, template_vars)
            return render_to_response("subsidiaries/update.html", request_context)
    else:
        message = "No se ha podido encontrar la subsidiaria"
        return HttpResponse(message+"%s." % subsidiary_id)



"""
def add(request):
    name = request.POST["name"]
    subsidiaria = Subsidiary(
        name = name
    )
    subsidiaria.save()
    return index(request, message='Se agrego la subsidiaria')

def details(request, subsidiary_id):
    try:
        sub = Subsidiary.objects.get(id=subsidiary_id)
    except:
        sub = False

    if sub:
         if request.method == 'POST':
            form = Name_Form(request.POST, instance=a)
         if form.is_valid():
            j = form.save( commit=False )
            j.save()
         else:
            form = Name_Form( instance = a )
            return render_to_response('subsidiaries/add.html', {'formulario':})


def add(request):

    if request.method=='POST':
        formulario = NuevaSubsidiaria(request.POST)
        if formulario.is_valid():
            return render_to_response('subsidiaries/add.html', {'formulario':formulario})
    else:
        formulario = NuevaSubsidiaria()
        return render_to_response('subsidiaries/add.html', {'formulario':formulario})

def edit(request, subsidiary_id):
    try:
        sub = Subsidiary.objects.get(id=subsidiary_id)
    except:
        sub = False

    if sub:
        return render_to_response(
            'subsidiaries/new.html',
            {
                'action': 'update/'+ subsidiary_id,
                'sub': sub,
                'button': 'Modificar'
            }
        )
"""
def remove(request, subsidiary_id):

    try:
        sub = Subsidiary.objects.get(id=subsidiary_id)
    except Subsidiary.DoesNotExist:
        sub = False

    if sub:
        try:
            sub.delete()
            message="Se ha eliminado la subsidiaria"
            template_vars = {
                "titulo": "Subsidiarias",
                "message": "Se ha eliminado la subsidiaria"
            }
            request_context = RequestContext(request, template_vars)
            #return render_to_response("subsidiaries/index.html", request_context)
            return HttpResponseRedirect('/subsidiaries')

        except:
            message = "No se pudo eliminar"
            template_vars = {
                "titulo": "Subsidiarias",
                "message": message
            }
            request_context = RequestContext(request, template_vars)
            #return render_to_response("subsidiaries/index.html", request_context)
            return HttpResponse('No se ha podido eliminar la subsidiaria')
    else:
        message = "No se ha encontrado la subsidiaria "
        template_vars = {
            "titulo": "Subsidiarias",
            "message": message
        }
        request_context = RequestContext(request, template_vars)
        #return render_to_response("subsidiaries/index.html", request_context)
        return HttpResponseRedirect('/services')


