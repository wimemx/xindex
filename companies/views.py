import os
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from xindex.models import Company
from django.http import HttpResponse, Http404, HttpResponseRedirect
from xindex.forms import CompanyForm
from django.utils import simplejson
from xindex.models import Xindex_User
from django.template.loader import render_to_string


@login_required(login_url='/signin/')
def index(request):
    all_companies = Company.objects.all().filter(active=True).order_by('-date')
    template_vars = {"titulo": "Companies",
                     "companies": all_companies}
    request_context = RequestContext(request, template_vars)
    return render_to_response("companies/companies.html", request_context)


@login_required(login_url='/signin/')
def add(request):
    if request.method=='POST':
        formulario = CompanyForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect('/companies')
    else:
        formulario = CompanyForm()

    request_context = RequestContext(request)
    return render_to_response("companies/new_company.html",
                              {"formulario": formulario,
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


@login_required(login_url='/signin/')
def edit(request, company_id):

    company = Company.objects.get(pk=company_id)
    if request.method=='POST':
        formulario = CompanyForm(request.POST, instance=company)
        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect('/companies')
    else:
        formulario = CompanyForm(instance=company)

    request_context = RequestContext(request)
    return render_to_response("companies/new_company.html",
                              {"formulario": formulario,
                               "Add":"Save",
                               "reset": "button",
                               "onclick": "javascript:history.go(-1)"},
                              request_context)


@login_required(login_url='/signin/')
def remove(request, company_id):
    #return HttpResponse("You're about to remove Company %s." % company_id)
    company = Company.objects.get(pk=company_id)
    #company.delete()
    company.active = False
    company.save()
    return HttpResponseRedirect('/companies')


@login_required(login_url='/signin/')
def detail(request, company_id):
    try:
        company = Company.objects.get(pk=company_id)
        status = str(company.active)
    except Company.DoesNotExist:
        raise Http404
    return render_to_response('companies/detail.html', {'company': company,
                                                        'status': status})


@login_required(login_url='/signin/')
def getCInJson(request):
    companies = {'companies': []}

    for c in Company.objects.filter(active=True).order_by('-date'):
        companies['companies'].append(
            {
                "name": c.name,
                "address": c.address,
                "rfc": c.rfc,
                "c_det": c.id,
                "c_up": c.id,
                "c_del": c.id
            }
        )

    return HttpResponse(simplejson.dumps(companies))


@login_required(login_url='/signin/')
def details(request, business_unit_id):
    template_vars = {
        'titulo': 'Detalles'
    }
    try:
        c = Company.objects.get(id=business_unit_id)

        c = False if c.active==False else c
    except Company.DoesNotExist:
        c = False

    template_vars['company'] = c
    request_context = RequestContext(request, template_vars)
    return render_to_response('company/details.html', request_context)


@login_required(login_url='/signin/')
def edit_privacy_notice(request):
    privacy_notice = ''
    xindex_user = Xindex_User.objects.get(user=request.user)
    company = xindex_user.company_set.all()[:1]
    for com in company:
        if com.privacy_notice:
            privacy_notice = com.privacy_notice
    if request.POST:
        print request.POST
        if 'text-area-field' in request.POST:
            xindex_user = Xindex_User.objects.get(user=request.user)
            company = xindex_user.company_set.all()[:1]
            for c in company:
                c.privacy_notice = request.POST['text-area-field']
                c.save()
                privacy_notice = c.privacy_notice
            template_vars = {
                'titulo': 'Aviso de privacidad',
                'answer': 'La informacion ha sido guardada',
                'privacy_notice': privacy_notice
            }
        request_context = RequestContext(request, template_vars)
        return render_to_response('companies/privacy_notice.html', request_context)
    else:
        template_vars = {
            'titulo': 'Aviso de privacidad',
            'privacy_notice': privacy_notice
        }
        request_context = RequestContext(request, template_vars)
        return render_to_response('companies/privacy_notice.html', request_context)


@login_required(login_url='/signin/')
def edit_email_template(request):
    email_template = ''
    xindex_user = Xindex_User.objects.get(user=request.user)
    company = xindex_user.company_set.all()[:1]
    for com in company:
        if com.email_template:
            email_template = com.email_template
    if request.POST:
        print request.POST
        if 'text-area-field' in request.POST:
            xindex_user = Xindex_User.objects.get(user=request.user)
            company = xindex_user.company_set.all()[:1]
            for c in company:
                c.email_template = request.POST['text-area-field']
                c.save()
                email_template = c.email_template
            template_vars = {
                'title': 'Plantilla de Email',
                'answer': 'La informacion ha sido guardada',
                'email_template': email_template
            }
        request_context = RequestContext(request, template_vars)
        return render_to_response('companies/email_template.html', request_context)
    else:
        template_vars = {
            'title': 'Plantilla de Email',
            'email_template': email_template
        }
        request_context = RequestContext(request, template_vars)
        return render_to_response('companies/email_template.html', request_context)


def upload_logo(request, company_id):
    company = Company.objects.get(pk=int(company_id))

    company.logo = str(company.id) + str(request.FILES['file'])
    company.save()

    path = os.path.join(
        os.path.dirname(__file__), '..',
        'templates/static/images/').replace('\\', '/')

    path += str(company.id) + str(request.FILES['file'])
    fileToUp = request.FILES['file']
    handle_uploaded_file(path, fileToUp)
    context = {}
    context = simplejson.dumps(context)
    return HttpResponse(context, mimetype='application/json')

def handle_uploaded_file(destination, f):
    with open(destination, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def load_company_logo(request):
    xindex_user = Xindex_User.objects.get(user=request.user)
    logo_name = 'xindex_logo.png'
    for company in xindex_user.company_set.filter(active=True):
        if company.logo != 'No image':
            logo_name = company.logo
    return render_to_string(logo_name)