from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from xindex.models import Company_Type
from django.http import HttpResponse, Http404, HttpResponseRedirect
from xindex.forms import CompanyTypeForm


@login_required(login_url='/signin/')
def index(request):
    all_company_type = Company_Type.objects.all().filter(active=True).\
        order_by('-date')

    template_vars = {"titulo": "Company Types",
                     "company_types": all_company_type}
    request_context = RequestContext(request, template_vars)
    return render_to_response("company_types/company_types.html",
                              request_context)


@login_required(login_url='/signin/')
def add(request):
    if request.method=='POST':
        formulario = CompanyTypeForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect('/company_types')
    else:
        formulario = CompanyTypeForm()

    request_context = RequestContext(request)
    return render_to_response("company_types/new_company_type.html",
                              {"formulario": formulario, "Add": "Add",
                               "reset": "reset"},
                              request_context)


@login_required(login_url='/signin/')
def edit(request, company_type_id):
    company_type = Company_Type.objects.get(pk=company_type_id)
    if request.method=='POST':
        formulario = CompanyTypeForm(request.POST, instance=company_type)
        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect('/company_types')
    else:
        formulario = CompanyTypeForm(instance=company_type)

    request_context = RequestContext(request)
    return render_to_response("company_types/new_company_type.html",
                              {"formulario": formulario,
                               "Add": "Save",
                               "reset": "button",
                               "onclick": "javascript:history.go(-1)"},
                              request_context)


@login_required(login_url='/signin/')
def remove(request, company_type_id):
    company_type = Company_Type.objects.get(pk=company_type_id)
    company_type.active = False
    company_type.save()
    return HttpResponseRedirect('/company_types')


@login_required(login_url='/signin/')
def detail(request, company_type_id):
    try:
        company_type = Company_Type.objects.get(pk=company_type_id)
        status = str(company_type.active)
    except Company_Type.DoesNotExist:
        raise Http404
    return render_to_response('company_types/detail.html',
                              {'company_type': company_type,
                               'status': status})
