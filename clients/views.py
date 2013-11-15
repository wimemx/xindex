import csv
import os
import short_url
from django.shortcuts import render_to_response, HttpResponse, \
    HttpResponseRedirect, get_object_or_404
from django.template.context import RequestContext
from django.utils import simplejson
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User

from xindex.models import Subsidiary
from xindex.models import Client, Company, ClientActivity
from xindex.models import BusinessUnit, Service


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
            #date_of_birth=request.POST['client_date'],
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
        #client.date_of_birth = request.POST['client_date']
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
                         #'date': client.date_of_birth,
                         'sex': client.sex,
                         'company': client.company,
                         'companies': companies}

        request_context = RequestContext(request, template_vars)
        return render_to_response("clients/edit_client.html", request_context)


@login_required(login_url='/signin/')
def csv_read_prueba(request):

    fileToAdd = open("/home/osvaldomg/Documentos/clients.csv")

    reader = csv.reader(fileToAdd, delimiter=',', quotechar='|')
    for eachRow in reader:

        clientData = Client.objects.create(
            name=eachRow[1],
            first_name=eachRow[2],
            last_name=eachRow[3],
            sex=eachRow[4],
            date_of_birth=eachRow[5],
            email=eachRow[6],
            phone=eachRow[7],
            state=eachRow[8],
            city=eachRow[9],
            company=Company.objects.get(name=eachRow[10])
        )

        clientData.save()
    return HttpResponseRedirect('/clients/')

@login_required(login_url='/signin/')
def csv_read(request):

    if request.POST:

        path = os.path.join(
            os.path.dirname(__file__), '..',
            'templates/static/csv/').replace('\\', '/')

        path += str(request.FILES['client_csv'])

        fileToUp = request.FILES['client_csv']
        handle_uploaded_file(path, fileToUp)

        fileToAdd = open(path)

        reader = csv.reader(fileToAdd, delimiter=',', quotechar='|')

        print reader
        counterLoop = 0
        for eachRow in reader:
            if counterLoop == 0:
                counterLoop += 1
                continue
            subsidiary = Subsidiary.objects.get(name=eachRow[7], active=True)

            """
            clientData = Client.objects.create(
                #name=eachRow[1],
                first_name=eachRow[1],
                last_name=eachRow[2],
                sex=eachRow[3],
                #date_of_birth=eachRow[5],
                email=eachRow[4],
                phone=eachRow[5],
                company=subsidiary.company
            )

            clientData.save()
            """

            if Client.objects.filter(email=eachRow[4]).exists():
                myAlreadyExistsClient = Client.objects.get(
                    email=eachRow[4])
                activityData = ClientActivity.objects.create(
                    client=myAlreadyExistsClient,
                    date=eachRow[6],
                    subsidiary=subsidiary,
                    business_unit=BusinessUnit.objects.get(name=eachRow[8],
                                                           active=True),
                    service=Service.objects.get(name=eachRow[9], active=True)
                )
                activityData.save()

            else:
                clientData = Client.objects.create(
                #name=eachRow[1],
                first_name=eachRow[1],
                last_name=eachRow[2],
                sex=eachRow[3],
                #date_of_birth=eachRow[5],
                email=eachRow[4],
                phone=eachRow[5],
                company=subsidiary.company
                )

                clientData.save()

                activityData = ClientActivity.objects.create(
                    client=clientData,
                    date=eachRow[6],
                    subsidiary=subsidiary,
                    business_unit=BusinessUnit.objects.get(name=eachRow[8],
                                                           active=True),
                    service=Service.objects.get(name=eachRow[9], active=True)
                )
                activityData.save()

                url = short_url.encode_url(clientData.id)
                print url

        fileToAdd.close()
        if fileToAdd.closed:
            os.remove(path)

        return HttpResponseRedirect('/clients/')

    else:

        template_vars = {}
        request_context = RequestContext(request, template_vars)
        return render_to_response("clients/add_csv.html", request_context)


def handle_uploaded_file(destination, f):
    with open(destination, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def getAnswersByClient(request):
    print 'Hello World'