from random import sample
from xindex.models import ClientActivity, BusinessUnit, Service


def randomClient(business_id, service_id):
    businessUnit = BusinessUnit.objects.get(pk=business_id)
    service = Service.objects.get(pk=service_id)

    myClientActivity = ClientActivity.objects.filter(
        business_unit=businessUnit, service=service
    ).order_by('?').exclude(status="A").exclude(status="D")[0]

    if myClientActivity.status == "NA":

        print "================"
        print "SIN RESPONDER"
        return myClientActivity
    else:
        print "================"
        print "RESPONDIDO"
        randomClient()