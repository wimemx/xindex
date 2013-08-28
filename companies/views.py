from django.shortcuts import render_to_response
from django.template.context import RequestContext
from xindex.models import Company
from django.http import HttpResponse, Http404, HttpResponseRedirect
from xindex.forms import CompanyForm


def index(request):
    all_companies = Company.objects.all().filter(active=True).order_by('-date')
    template_vars = {"titulo": "Companies",
                     "companies": all_companies}
    request_context = RequestContext(request, template_vars)
    return render_to_response("companies/companies.html", request_context)

def add(request):
    if request.method=='POST':
        formulario = CompanyForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect('/companies')
    else:
        formulario = CompanyForm()

    request_context = RequestContext(request)
    return render_to_response("companies/new_company.html", {"formulario": formulario,
                                                             "Add": "Add",
                                                             "reset": "reset"},
                              request_context)
'''
def add(request):
    error = ""
    if request.method == 'POST':
        formulario = CompanyForm(request.POST)
        if formulario.is_valid():
            try:
                company = Company(name=formulario.cleaned_data["name"],
                                  types=formulario.cleaned_data["types"],
                                  parent_company=formulario.cleaned_data["parent_company"],
                                  about=formulario.cleaned_data["about"],
                                  address=formulario.cleaned_data["address"],
                                  rfc=formulario.cleaned_data["address"],
                                  phone=formulario.cleaned_data["phone"],
                                  status=formulario.cleaned_data["status"],
                                  zone=formulario.cleaned_data["zone"])
                company.save()
                return HttpResponseRedirect('/add')
            except ValueError:
                error = "Debes completar el formulario"
    else:
        formulario = CompanyForm()
    template_vars = {"formulario": formulario,
                     "error": error}
    request_context = RequestContext(request, template_vars)
    return render_to_response("new_company.html", request_context)
'''


def edit(request, company_id):
    #return HttpResponse("You're editing Company %s." % company_id)
    company = Company.objects.get(pk=company_id)
    if request.method=='POST':
        formulario = CompanyForm(request.POST, instance=company)
        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect('/companies')
    else:
        formulario = CompanyForm(instance=company)

    request_context = RequestContext(request)
    return render_to_response("companies/new_company.html", {"formulario": formulario,
                                                             "Add":"Save",
                                                             "reset": "button",
                                                             "onclick": "javascript:history.go(-1)"},
                              request_context)


def remove(request, company_id):
    #return HttpResponse("You're about to remove Company %s." % company_id)
    company = Company.objects.get(pk=company_id)
    #company.delete()
    company.active = False
    company.save()
    return HttpResponseRedirect('/companies')


def detail(request, company_id):
    try:
        company = Company.objects.get(pk=company_id)
        status = str(company.active)
    except Company.DoesNotExist:
        raise Http404
    return render_to_response('companies/detail.html', {'company': company,
                                                        'status': status})
