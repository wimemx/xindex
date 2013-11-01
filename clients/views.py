from django.shortcuts import render_to_response, HttpResponse, \
    HttpResponseRedirect, get_object_or_404
from django.template.context import RequestContext
from django.utils import simplejson
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User

from xindex.models import Client, Company


@login_required(login_url='/signin/')
def client_list(request):

    template_vars = {}
    request_context = RequestContext(request, template_vars)
    return render_to_response("clients/client_list.html", request_context)


@login_required(login_url='/signin/')
#@user_passes_test(lambda u: u.is_superuser)
def getClientsInJson(request):
    clients = {'clients': []}

    clientQuery = Client.objects.filter(active=True)

    for eachClient in clientQuery:

        clients['clients'].append(
            {
                "first_name": eachClient.first_name,
                "last_name": eachClient.last_name,
                "email": eachClient.email,
                "actions": eachClient.id
            }
        )

    return HttpResponse(simplejson.dumps(clients))


@login_required(login_url='/signin/')
def add_client(request):

    if request.POST:
        company = Company.objects.get(pk=request.POST['client_company'])

        new_client = Client.objects.create(
            name=request.POST['client_name'],
            first_name=request.POST['client_name'],
            last_name=request.POST['client_surname'],
            sex=request.POST['client_sex'],
            date_of_birth=request.POST['client_date'],
            email=request.POST['client_email'],
            phone=request.POST['client_phone'],
            company=company,)

        new_client.save()
        return HttpResponseRedirect('/clients/')

    else:
        companies = Company.objects.filter(active=True)

        template_vars = {'companies': companies}
        request_context = RequestContext(request, template_vars)
        return render_to_response("clients/add_client.html", request_context)


@login_required(login_url='/signin/')
def remove_client(request,  client_id):

    client = Client.objects.get(pk=client_id)
    client.active = False
    client.save()

    return HttpResponse('Si')


@login_required(login_url='/signin/')
def edit_client(request, client_id):

    client = Client.objects.get(pk=client_id)

    if request.POST:
        company = Company.objects.get(pk=request.POST['client_company'])

        client.name = request.POST['client_name']
        client.first_name = request.POST['client_name']
        client.last_name = request.POST['client_surname']
        client.sex = request.POST['client_sex']
        client.email = request.POST['client_email']
        client.date_of_birth = request.POST['client_date']
        client.phone = request.POST['client_phone']
        client.company = company
        client.save()

        return HttpResponseRedirect('/clients/')
    else:

        companies = Company.objects.filter(active=True)

        template_vars = {'id': client.id,
                         'name': client.first_name,
                         'surname': client.last_name,
                         'email': client.email,
                         'phone': client.phone,
                         'date': client.date_of_birth,
                         'sex': client.sex,
                         'company': client.company,
                         'companies': companies}
        print template_vars
        request_context = RequestContext(request, template_vars)
        return render_to_response("clients/edit_client.html", request_context)