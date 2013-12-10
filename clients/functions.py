# coding=utf-8
import json
import mandrill
from datetime import datetime
import short_url
from xindex.models import Client, Company, ClientActivity, Subsidiary, \
    BusinessUnit, Service, Survey

# my MANDRILL API KEY        hzuTlBSxNBabQDBkpTZveA


def mailing(client, survey):
    try:
        mandrill_client = mandrill.Mandrill('hzuTlBSxNBabQDBkpTZveA')

        message = {
            'html': '<h2>Xindex Survey</h2>'
                    + ''
                    + '<a href="http://127.0.0.1:8000/surveys/answer/'
                    + str(survey.id)
                    + '/a6dt3j4kd90/'
                    + str(client.id)
                    + ' ">' +
                    'Responder encuesta'
                    + '</a>',
            'subject': 'Customer Service',
            'from_email': 'team@xindex.com.mx',
            'from_name': 'Xindex Survey',
            'to': [
                {'email': client.email,
                 'name': client.first_name,
                 'type': 'to'}
            ],
            #'headers': {'¿Dudas?': 'info@xindex.com.mx'},
            'important': True,
            'track_opens': True,
            'track_clicks': True,
            'auto_text': None,
            'auto_html': None,
            #'inline_css': None,
            #'url_strip_qs': None,
            #'preserve_recipients': None,
            #'view_content_link': None,
            #'bcc_address': 'bcc_address@example.com',
            'tracking_domain': None,
            'signing_domain': None,
            'return_path_domain': None,
            'merge': True,
            'global_merge_vars': [
                {'content': 'merge1 content',
                 'name': 'GLOBAL MERGE'}],
            'merge_vars': [
                {'rcpt': 'martin_3-3@hotmail.com',
                 'vars': [
                     {'content': 'merge2 content',
                      'name': 'MARTIN ANDRADE'}
                 ]}
            ],
            'tags': ['prueba mailing'],
            #'subaccount': 'usuario-123',
            #'google_analytics_domains': ['example.com'],
            #'google_analytics_campaign': 'message.from_email@example.com',
            #'metadata': {'website': 'www.wime.com'},
            #'recipient_metadata': [
            #    {'rcpt': 'recipient.email@example.com',
            #     'values': {'user_id': 123456}}],
            #'attachments': [
            #    {'content': 'ZXhhbXBsZSBmaWxl',
            #     'name': 'myfile.txt',
            #     'type': 'text/plain'}],
            #'images': [
            #    {'content': 'ZXhhbXBsZSBmaWxl',
            #     'name': 'IMAGECID',
            #     'type': 'image/png'}]
        }
        result = mandrill_client.messages.send(
            message=message,
            async=False)

        print result

    except mandrill.Error, e:

        print 'A mandrill error occurred: %s - %s' % (e.__class__, e)
        raise


def addClientFromCSV(data):

    company = Company.objects.filter(active=True)[:1]
    clientData = str(data).split("},")

    print clientData
    newClient = Client.objects.create(rating=1, company=company[0])

    for eachClientData in clientData:
        if eachClientData[-1] != "}":
            eachClientData += "}"

        modelField = json.loads(eachClientData)["name"]
        fieldData = json.loads(eachClientData)["value"]

        if modelField == "first_name":
            newClient.first_name = fieldData
        if modelField == "last_name":
            newClient.last_name = fieldData
        if modelField == "sex":
            newClient.sex = fieldData
        if modelField == "email":
                newClient.email = fieldData
        if modelField == "phone":
            newClient.phone = fieldData
    newClient.save()
    return newClient.id


def addClientActivity(data, activity):

    id_client = addClientFromCSV(data)
    myClient = Client.objects.get(pk=id_client)
    newActivity = ClientActivity.objects.create(client=myClient)

    for eachActivity in activity:
        activityClient = str(eachActivity).split("},")

        for eachLine in activityClient:
            if eachLine[-1] != "}":
                eachLine += "}"

            modelField = json.loads(eachLine)["name"]
            fieldData = json.loads(eachLine)["value"]

            if modelField == "subsidiary":
                subsidiary = Subsidiary.objects.get(pk=fieldData)
                newActivity.subsidiary = subsidiary

            if modelField == "business_unit":
                business = BusinessUnit.objects.get(pk=fieldData)
                newActivity.business_unit = business

            if modelField == "service":
                service = Service.objects.get(pk=fieldData)
                newActivity.service = service

    newActivity.save()

    url = short_url.encode_url(myClient.id)
    urld = short_url.decode_url(url)

    print url
    print urld

    try:
        survey = Survey.objects.get(
            business_unit_id=newActivity.business_unit,
            service_id=newActivity.service
        )
        newActivity.survey = survey
        newActivity.save()
        mailing(myClient, survey)

    except Survey.DoesNotExist:
        print "NO EXISTE ENCUESTA"


def addActivity(client, activity):

    newActivity = ClientActivity.objects.create(client=client)

    for eachActivity in activity:
        activityClient = str(eachActivity).split("},")

        for eachLine in activityClient:
            if eachLine[-1] != "}":
                eachLine += "}"

            modelField = json.loads(eachLine)["name"]
            fieldData = json.loads(eachLine)["value"]

            if modelField == "subsidiary":
                subsidiary = Subsidiary.objects.get(pk=fieldData)
                newActivity.subsidiary = subsidiary

            if modelField == "business_unit":
                business = BusinessUnit.objects.get(pk=fieldData)
                newActivity.business_unit = business

            if modelField == "service":
                service = Service.objects.get(pk=fieldData)
                newActivity.service = service

    newActivity.save()

    """
    url = short_url.encode_url(client.id)
    urld = short_url.decode_url(url)

    print url
    print urld
    """
    try:
        survey = Survey.objects.get(
            business_unit_id=newActivity.business_unit,
            service_id=newActivity.service
        )
        newActivity.survey = survey
        newActivity.save()
        mailing(client, survey)

    except Survey.DoesNotExist:
        print "NO EXISTE ENCUESTA"
